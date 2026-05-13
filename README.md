# Wärmepumpen-Auslegung

Dieses Repository enthält ein kleines Python-Tool zur überschlägigen Auslegung einer R290/Propan-Luft-Wasser-Wärmepumpe für drei Familienhäuser. Es erstellt einen Markdown-Report mit:

- Eingabedaten und Plausibilitätshinweis
- COP-/JAZ-Bewertung inklusive Sensitivität
- Investitions-, Betriebs- und ROI-Rechnung
- empfohlener Leistung und Baukomponenten
- nächsten Planungsschritten

> Wichtig: Die Berechnung ersetzt keine Heizlastberechnung nach DIN EN 12831 und keine Fachplanung. Der im Beispiel genannte Wert `17000` wird als Jahreswärmebedarf in `kWh/a` interpretiert, nicht als Leistung in `kW`.

## Nutzung

Standardreport erzeugen:

```bash
python3 heatpump_report.py
```

Report mit Beispiel-Eingabedaten erzeugen:

```bash
python3 heatpump_report.py --input example_input.json --output waermepumpe_report.md
```

## Eingabedaten anpassen

Die Datei `example_input.json` kann kopiert und angepasst werden. Unterstützte Felder sind unter anderem:

| Feld | Bedeutung | Beispiel |
| --- | --- | ---: |
| `houses` | Anzahl der Gebäude | `3` |
| `annual_heat_demand_kwh` | Jahreswärmebedarf gesamt | `17000` |
| `seasonal_cop` | saisonaler COP / JAZ | `3.3` |
| `electricity_price_eur_per_kwh` | Wärmepumpen-Strompreis | `0.32` |
| `old_heating_price_eur_per_kwh` | Vergleichspreis der Altanlage | `0.12` |
| `investment_gross_eur` | Bruttoinvestition | `67500` |
| `subsidy_rate` | angenommene Zuschussquote | `0.35` |

## Annahmen im Standardfall

- R290/Propan als natürliches Kältemittel
- Luft-Wasser-Wärmepumpe
- 18 cm Dämmung und Dreifachverglasung
- 17.000 kWh/a Jahreswärmebedarf für alle drei Häuser zusammen
- 1.800 Vollbenutzungsstunden zur überschlägigen Leistungsableitung
- 20 % Planungsreserve
- JAZ 3,3 als konservativer Vorplanungswert
- 20 Jahre Betrachtungszeitraum

## Datengrundlagen

Die Defaultwerte sind bewusst überschlägig und sollten durch lokale Angebote und eine Fachplanung ersetzt werden. Als Orientierungsquellen wurden genutzt:

- [Fraunhofer ISE](https://www.ise.fraunhofer.de/de/presse-und-medien/news/2024/waermepumpenfeldstest-zwischenergebnisse-bestaetigen-effizienten-betrieb-auch-im-altbau.html): Feldtest mit mittlerer JAZ 3,3 für ausgewertete Außenluft-Wärmepumpen im Bestand.
- [KfW Programm 458](https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestehende-Immobilie/F%C3%B6rderprodukte/Heizungsf%C3%B6rderung-f%C3%BCr-Privatpersonen-Wohngeb%C3%A4ude-%28458%29/): Förderlogik für klimafreundliche Heizungen in bestehenden Wohngebäuden.
- [co2online](https://www.co2online.de/modernisieren-und-bauen/waermepumpe/): grobe Orientierungswerte für Anschaffung und Wartung von Luftwärmepumpen.
