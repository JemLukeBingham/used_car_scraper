import unittest
from text_formatting import format_mileage, format_year, format_price

class TestParsing(unittest.TestCase):
    def test_mileage(self):
        self.assertEqual(format_mileage("  100 000 km"), int(100000))
        self.assertEqual(format_mileage("  100000km"), int(100000))
        #self.assertEqual(format_mileage("  100,000 km"), int(100000))
        #self.assertEqual(format_mileage("  100,000km"), int(100000))
        self.assertEqual(format_mileage("null"), "null")
        self.assertEqual(format_mileage(None), None)
        #self.assertEqual(format_mileage(100000), 100000)

    def test_year(self):
        self.assertEqual(format_year(2016), 2016)
        self.assertEqual(format_year(2016.0), 2016)
        self.assertEqual(format_year("2016"), 2016)
        self.assertEqual(format_year("   2016 \n"), 2016)
        self.assertEqual(format_year("No Year"), "No Year")
        self.assertEqual(format_year(None), None)

    def test_price(self):
        #self.assertEqual(format_price("ZAR 10,000"), 10000)
        #self.assertEqual(format_price("ZAR 10000"), 10000)
        self.assertEqual(format_price("  R 10,000"), 10000)
        self.assertEqual(format_price("  R 10000"), 10000)

if __name__=="__main__":
    unittest.main()
