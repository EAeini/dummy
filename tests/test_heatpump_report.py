import unittest

from heatpump_report import HeatPumpInput, calculate, render_report


class HeatPumpReportTest(unittest.TestCase):
    def test_default_capacity_and_roi(self):
        result = calculate(HeatPumpInput())
        self.assertAlmostEqual(result.recommended_capacity_kw, 11.3333333333)
        self.assertAlmostEqual(result.electricity_kwh_per_year, 5151.5151515)
        self.assertGreater(result.simple_roi_years, 40)

    def test_report_contains_required_sections(self):
        inp = HeatPumpInput()
        report = render_report(inp, calculate(inp))
        self.assertIn("COP-/JAZ-Bewertung", report)
        self.assertIn("Kosten und ROI", report)
        self.assertIn("Fließbild Kreislauf", report)
        self.assertIn("35 % durch Stadt", report)
        self.assertIn("Baukomponenten", report)
        self.assertIn("17.000 kWh/a", report)

    def test_invalid_subsidy_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate(HeatPumpInput(subsidy_rate=0.71))


if __name__ == "__main__":
    unittest.main()
