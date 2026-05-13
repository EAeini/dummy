#!/usr/bin/env python3
"""Wärmepumpen-Auslegung und Wirtschaftlichkeitsreport.

Das Tool erstellt eine überschlägige Vorplanung für eine R290/Propan
Luft-Wasser-Wärmepumpe für drei Familienhäuser. Es ersetzt keine Heizlast nach
DIN EN 12831, hilft aber bei frühen Varianten- und Budgetentscheidungen.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any
import json


@dataclass(frozen=True)
class HeatPumpInput:
    project_name: str = "Drei Familienhäuser"
    houses: int = 3
    refrigerant: str = "R290 / Propan"
    heat_pump_type: str = "Luft-Wasser-Wärmepumpe"
    insulation_cm: float = 18.0
    windows: str = "Dreifachverglasung"
    annual_heat_demand_kwh: float = 17_000.0
    design_full_load_hours: float = 1_800.0
    domestic_hot_water_share: float = 0.18
    target_flow_temperature_c: float = 45.0
    seasonal_cop: float = 3.3
    electricity_price_eur_per_kwh: float = 0.32
    old_heating_price_eur_per_kwh: float = 0.12
    old_heating_efficiency: float = 0.90
    investment_gross_eur: float = 67_500.0
    subsidy_rate: float = 0.35
    maintenance_heat_pump_eur_per_year: float = 450.0
    maintenance_old_heating_eur_per_year: float = 750.0
    planning_reserve: float = 0.20
    lifetime_years: int = 20


@dataclass(frozen=True)
class HeatPumpResult:
    heat_output_kw: float
    recommended_capacity_kw: float
    heating_demand_kwh: float
    hot_water_demand_kwh: float
    electricity_kwh_per_year: float
    heat_pump_energy_cost_eur_per_year: float
    heat_pump_total_running_cost_eur_per_year: float
    old_heating_cost_eur_per_year: float
    old_heating_total_running_cost_eur_per_year: float
    subsidy_eur: float
    net_investment_eur: float
    annual_savings_eur: float
    simple_roi_years: float | None
    lifetime_cashflow_eur: float


def load_input(path: Path | None) -> HeatPumpInput:
    """Load optional JSON input and merge it with defaults."""
    defaults: dict[str, Any] = asdict(HeatPumpInput())
    if path is None:
        return HeatPumpInput()
    data = json.loads(path.read_text(encoding="utf-8"))
    unknown = sorted(set(data) - set(defaults))
    if unknown:
        raise ValueError(f"Unbekannte Eingabefelder: {', '.join(unknown)}")
    defaults.update(data)
    return HeatPumpInput(**defaults)


def calculate(inp: HeatPumpInput) -> HeatPumpResult:
    if inp.annual_heat_demand_kwh <= 0:
        raise ValueError("annual_heat_demand_kwh muss größer 0 sein")
    if inp.seasonal_cop <= 0:
        raise ValueError("seasonal_cop muss größer 0 sein")
    if inp.design_full_load_hours <= 0:
        raise ValueError("design_full_load_hours muss größer 0 sein")
    if not 0 <= inp.subsidy_rate <= 0.70:
        raise ValueError("subsidy_rate muss zwischen 0 und 0.70 liegen")

    hot_water = inp.annual_heat_demand_kwh * inp.domestic_hot_water_share
    heating = inp.annual_heat_demand_kwh - hot_water
    heat_output = inp.annual_heat_demand_kwh / inp.design_full_load_hours
    capacity = heat_output * (1 + inp.planning_reserve)
    electricity = inp.annual_heat_demand_kwh / inp.seasonal_cop
    hp_energy_cost = electricity * inp.electricity_price_eur_per_kwh
    hp_total_cost = hp_energy_cost + inp.maintenance_heat_pump_eur_per_year
    old_energy_input = inp.annual_heat_demand_kwh / inp.old_heating_efficiency
    old_energy_cost = old_energy_input * inp.old_heating_price_eur_per_kwh
    old_total_cost = old_energy_cost + inp.maintenance_old_heating_eur_per_year
    subsidy = inp.investment_gross_eur * inp.subsidy_rate
    net_investment = inp.investment_gross_eur - subsidy
    annual_savings = old_total_cost - hp_total_cost
    roi = net_investment / annual_savings if annual_savings > 0 else None
    lifetime_cashflow = annual_savings * inp.lifetime_years - net_investment

    return HeatPumpResult(
        heat_output_kw=heat_output,
        recommended_capacity_kw=capacity,
        heating_demand_kwh=heating,
        hot_water_demand_kwh=hot_water,
        electricity_kwh_per_year=electricity,
        heat_pump_energy_cost_eur_per_year=hp_energy_cost,
        heat_pump_total_running_cost_eur_per_year=hp_total_cost,
        old_heating_cost_eur_per_year=old_energy_cost,
        old_heating_total_running_cost_eur_per_year=old_total_cost,
        subsidy_eur=subsidy,
        net_investment_eur=net_investment,
        annual_savings_eur=annual_savings,
        simple_roi_years=roi,
        lifetime_cashflow_eur=lifetime_cashflow,
    )


def eur(value: float) -> str:
    return f"{value:,.0f} €".replace(",", ".")


def num(value: float, digits: int = 1) -> str:
    return f"{value:,.{digits}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def render_report(inp: HeatPumpInput, result: HeatPumpResult) -> str:
    roi = "nicht erreicht" if result.simple_roi_years is None else f"{num(result.simple_roi_years, 1)} Jahre"
    return f"""# Auslegungsreport Wärmepumpe – {inp.project_name}

Erstellt am: {date.today().isoformat()}

## 1. Eingabedaten

| Parameter | Wert |
| --- | ---: |
| Gebäudeanzahl | {inp.houses} |
| Wärmepumpentyp | {inp.heat_pump_type} |
| Kältemittel | {inp.refrigerant} |
| Dämmung | {num(inp.insulation_cm, 0)} cm |
| Fenster | {inp.windows} |
| Jahreswärmebedarf | {num(inp.annual_heat_demand_kwh, 0)} kWh/a |
| Auslegungs-Vollbenutzungsstunden | {num(inp.design_full_load_hours, 0)} h/a |
| Warmwasseranteil | {num(inp.domestic_hot_water_share * 100, 0)} % |
| Ziel-Vorlauftemperatur | {num(inp.target_flow_temperature_c, 0)} °C |
| angesetzter saisonaler COP / JAZ | {num(inp.seasonal_cop, 2)} |
| Strompreis | {num(inp.electricity_price_eur_per_kwh, 2)} €/kWh |
| Vergleichspreis Altanlage | {num(inp.old_heating_price_eur_per_kwh, 2)} €/kWh |
| Bruttoinvestition | {eur(inp.investment_gross_eur)} |
| Förder-/Zuschussquote | {num(inp.subsidy_rate * 100, 0)} % |

> Hinweis: Falls mit „17.000 kW“ eine Leistung gemeint war, sind die Eingaben nicht plausibel. Für Wohngebäude wird der Jahresbedarf üblicherweise in kWh/a angegeben; dieser Report interpretiert den Wert als 17.000 kWh/a.

## 2. Dimensionierung

| Ergebnis | Wert |
| --- | ---: |
| Raumheizung | {num(result.heating_demand_kwh, 0)} kWh/a |
| Trinkwarmwasser | {num(result.hot_water_demand_kwh, 0)} kWh/a |
| überschlägige Heizleistung ohne Reserve | {num(result.heat_output_kw, 1)} kW |
| empfohlene WP-Leistung inkl. Reserve | {num(result.recommended_capacity_kw, 1)} kW |
| jährlicher WP-Strombedarf | {num(result.electricity_kwh_per_year, 0)} kWh/a |

Empfehlung: Für drei Häuser ist hydraulisch meist eine Kaskade aus 2 Modulen sinnvoller als ein einzelnes Großgerät, z. B. zwei R290-Luft-Wasser-Geräte mit zusammen rund {num(result.recommended_capacity_kw, 1)} kW. Dadurch bleiben Redundanz, Teillastbetrieb und Wartbarkeit besser.

## 3. COP-/JAZ-Bewertung

Der angesetzte COP ist ein saisonaler Planwert (JAZ) von **{num(inp.seasonal_cop, 2)}**. Bei Luft-Wasser-Wärmepumpen sinkt die Effizienz mit höherer Vorlauftemperatur und niedriger Außentemperatur. Für 45 °C Vorlauf ist der Wert als konservative Vorplanung geeignet; nach Herstellerdaten und Heizlastberechnung muss er projektspezifisch verifiziert werden.

Sensitivität:

| JAZ | Strombedarf | Stromkosten/a |
| ---: | ---: | ---: |
| 2,8 | {num(inp.annual_heat_demand_kwh / 2.8, 0)} kWh | {eur(inp.annual_heat_demand_kwh / 2.8 * inp.electricity_price_eur_per_kwh)} |
| 3,3 | {num(inp.annual_heat_demand_kwh / 3.3, 0)} kWh | {eur(inp.annual_heat_demand_kwh / 3.3 * inp.electricity_price_eur_per_kwh)} |
| 3,8 | {num(inp.annual_heat_demand_kwh / 3.8, 0)} kWh | {eur(inp.annual_heat_demand_kwh / 3.8 * inp.electricity_price_eur_per_kwh)} |

## 4. Kosten und ROI

| Position | Wert |
| --- | ---: |
| Investition brutto | {eur(inp.investment_gross_eur)} |
| angenommener Zuschuss | {eur(result.subsidy_eur)} |
| Nettoinvestition | {eur(result.net_investment_eur)} |
| WP-Energiekosten/a | {eur(result.heat_pump_energy_cost_eur_per_year)} |
| WP-Gesamtkosten Betrieb/a | {eur(result.heat_pump_total_running_cost_eur_per_year)} |
| Altanlage Betrieb/a | {eur(result.old_heating_total_running_cost_eur_per_year)} |
| jährliche Einsparung | {eur(result.annual_savings_eur)} |
| einfacher ROI | {roi} |
| Cashflow über {inp.lifetime_years} Jahre | {eur(result.lifetime_cashflow_eur)} |

## 5. Baukomponenten

- R290-Luft-Wasser-Wärmepumpe bzw. Kaskade mit zusammen ca. {num(result.recommended_capacity_kw, 1)} kW Heizleistung.
- Außenaufstellung mit Schallschutz, Kondensatablauf, Fundament/Konsolen und Sicherheitsabständen für Propan.
- Pufferspeicher oder hydraulische Weiche nach Herstellerhydraulik.
- Trinkwarmwasserspeicher oder Frischwasserstation, ausgelegt auf {inp.houses} Häuser.
- Hocheffizienzpumpen, Misch-/Umschaltventile, Schmutz-/Magnetitabscheider, Entlüfter, Ausdehnungsgefäß.
- Niedertemperatur-Wärmeverteilung: größere Heizflächen oder Fußbodenheizung prüfen, Ziel Vorlauf ≤ {num(inp.target_flow_temperature_c, 0)} °C.
- Regelung mit witterungsgeführter Heizkurve, Wärmemengenzähler und separatem Stromzähler.
- Elektroanschluss, Absicherung, optional PV-Einbindung und Energiemanagement.

## 6. Datengrundlagen

- [Fraunhofer ISE, Wärmepumpenfeldtest im Bestand](https://www.ise.fraunhofer.de/de/presse-und-medien/news/2024/waermepumpenfeldstest-zwischenergebnisse-bestaetigen-effizienten-betrieb-auch-im-altbau.html): Außenluft-Wärmepumpen mit mittlerer JAZ 3,3 und Bandbreite 2,4–4,0.
- [KfW Heizungsförderung 458](https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestehende-Immobilie/F%C3%B6rderprodukte/Heizungsf%C3%B6rderung-f%C3%BCr-Privatpersonen-Wohngeb%C3%A4ude-%28458%29/): Wärmepumpen erhalten 30 % Grundförderung; Effizienzbonus 5 % ist u. a. bei natürlichem Kältemittel möglich; insgesamt maximal 70 % Zuschuss.
- [co2online Wärmepumpen-Kosten](https://www.co2online.de/modernisieren-und-bauen/waermepumpe/): Luftwärmepumpen ca. 22.500 € je Einfamilienhaus inklusive Speicher, Wärmemengenzähler und Pumpe; Wartung grob 150 €/a je Einfamilienhaus.

## 7. Nächste Planungsschritte

1. Heizlast nach DIN EN 12831 je Gebäude und Nutzungseinheit berechnen.
2. Heizflächen prüfen: Raumweise Leistung bei 35–45 °C Vorlauf nachweisen.
3. Herstellergerät auswählen und COP/SCOP bei konkreten Betriebspunkten bestätigen.
4. Schall-, Aufstell-, Brandschutz- und Propan-Sicherheitskonzept erstellen.
5. Förderfähigkeit und Zuschusshöhe vor Beauftragung verbindlich prüfen.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Erstellt einen Wärmepumpen-Auslegungsreport als Markdown.")
    parser.add_argument("--input", type=Path, help="Optionale JSON-Datei mit Eingabewerten.")
    parser.add_argument("--output", type=Path, default=Path("waermepumpe_report.md"), help="Ausgabedatei.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    inp = load_input(args.input)
    result = calculate(inp)
    args.output.write_text(render_report(inp, result), encoding="utf-8")
    print(f"Report geschrieben: {args.output}")


if __name__ == "__main__":
    main()
