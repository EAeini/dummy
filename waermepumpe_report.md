# Auslegungsreport Wärmepumpe – Drei Familienhäuser – R290 Luft-Wasser

Erstellt am: 2026-05-13

## 1. Eingabedaten

| Parameter | Wert |
| --- | ---: |
| Gebäudeanzahl | 3 |
| Wärmepumpentyp | Luft-Wasser-Wärmepumpe |
| Kältemittel | R290 / Propan |
| Dämmung | 18 cm |
| Fenster | Dreifachverglasung |
| Jahreswärmebedarf | 17.000 kWh/a |
| Auslegungs-Vollbenutzungsstunden | 1.800 h/a |
| Warmwasseranteil | 18 % |
| Ziel-Vorlauftemperatur | 45 °C |
| angesetzter saisonaler COP / JAZ | 3,30 |
| Strompreis | 0,32 €/kWh |
| Vergleichspreis Altanlage | 0,12 €/kWh |
| Bruttoinvestition | 67.500 € |
| Förder-/Zuschussquote | 35 % |

> Hinweis: Falls mit „17.000 kW“ eine Leistung gemeint war, sind die Eingaben nicht plausibel. Für Wohngebäude wird der Jahresbedarf üblicherweise in kWh/a angegeben; dieser Report interpretiert den Wert als 17.000 kWh/a.

## 2. Dimensionierung

| Ergebnis | Wert |
| --- | ---: |
| Raumheizung | 13.940 kWh/a |
| Trinkwarmwasser | 3.060 kWh/a |
| überschlägige Heizleistung ohne Reserve | 9,4 kW |
| empfohlene WP-Leistung inkl. Reserve | 11,3 kW |
| jährlicher WP-Strombedarf | 5.152 kWh/a |

Empfehlung: Für drei Häuser ist hydraulisch meist eine Kaskade aus 2 Modulen sinnvoller als ein einzelnes Großgerät, z. B. zwei R290-Luft-Wasser-Geräte mit zusammen rund 11,3 kW. Dadurch bleiben Redundanz, Teillastbetrieb und Wartbarkeit besser.

## 3. COP-/JAZ-Bewertung

Der angesetzte COP ist ein saisonaler Planwert (JAZ) von **3,30**. Bei Luft-Wasser-Wärmepumpen sinkt die Effizienz mit höherer Vorlauftemperatur und niedriger Außentemperatur. Für 45 °C Vorlauf ist der Wert als konservative Vorplanung geeignet; nach Herstellerdaten und Heizlastberechnung muss er projektspezifisch verifiziert werden.

Sensitivität:

| JAZ | Strombedarf | Stromkosten/a |
| ---: | ---: | ---: |
| 2,8 | 6.071 kWh | 1.943 € |
| 3,3 | 5.152 kWh | 1.648 € |
| 3,8 | 4.474 kWh | 1.432 € |

## 4. Kosten und ROI

| Position | Wert |
| --- | ---: |
| Investition brutto | 67.500 € |
| angenommener Zuschuss | 23.625 € |
| Nettoinvestition | 43.875 € |
| WP-Energiekosten/a | 1.648 € |
| WP-Gesamtkosten Betrieb/a | 2.098 € |
| Altanlage Betrieb/a | 3.017 € |
| jährliche Einsparung | 918 € |
| einfacher ROI | 47,8 Jahre |
| Cashflow über 20 Jahre | -25.511 € |

## 5. Baukomponenten

- R290-Luft-Wasser-Wärmepumpe bzw. Kaskade mit zusammen ca. 11,3 kW Heizleistung.
- Außenaufstellung mit Schallschutz, Kondensatablauf, Fundament/Konsolen und Sicherheitsabständen für Propan.
- Pufferspeicher oder hydraulische Weiche nach Herstellerhydraulik.
- Trinkwarmwasserspeicher oder Frischwasserstation, ausgelegt auf 3 Häuser.
- Hocheffizienzpumpen, Misch-/Umschaltventile, Schmutz-/Magnetitabscheider, Entlüfter, Ausdehnungsgefäß.
- Niedertemperatur-Wärmeverteilung: größere Heizflächen oder Fußbodenheizung prüfen, Ziel Vorlauf ≤ 45 °C.
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
