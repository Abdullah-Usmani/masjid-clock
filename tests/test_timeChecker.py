import unittest
from datetime import time, datetime
from unittest.mock import patch, MagicMock
import pandas as pd
import timeChecker as tc


class TestTimeChecker(unittest.TestCase):

    def test_midnight_basic(self):
        result = tc.midnight("5:00 AM", "6:00 PM")
        self.assertEqual(result, "11:30 PM")

    def test_midnight_edge_case(self):
        result = tc.midnight("12:00 AM", "12:00 PM")
        self.assertEqual(result, "6:00 AM")

    @patch("timeChecker.pd.read_csv")
    def test_initializers_structure(self, mock_read_csv):
        mock_df = pd.DataFrame({
            'Date': ['01-Jan-2024'],
            'Hijri': ['01-Muh-1445'],
            'Day': ['Isnin'],
            'Fajr': ['5:30 AM'],
            'Syuruk': ['7:00 AM'],
            'Zohor': ['12:30 PM'],
            'Asar': ['4:00 PM'],
            'Maghrib': ['6:45 PM'],
            'Isyak': ['8:15 PM'],
            'Midnight': ['']
        })
        mock_read_csv.return_value = mock_df

        df, headers, ar_headers, iqama_headers = tc.initializers()

        self.assertIn('Fajr', df.columns)
        self.assertIn('Sunrise', df.columns)
        self.assertEqual(len(headers), 7)
        self.assertEqual(len(iqama_headers), 7)
        self.assertEqual(df.shape[0], 1)

    @patch("timeChecker.time.gmtime")
    @patch("timeChecker.time.localtime")
    @patch("timeChecker.pd.read_csv")
    def test_dateComparer(self, mock_read_csv, mock_localtime, mock_gmtime):
        mock_df = pd.DataFrame({
            'Date': ['01-Jan-2024'],
            'Hijri': ['01-Muh-1445'],
            'Day': ['Isnin'],
            'Fajr': ['5:30 AM'],
            'Sunrise': ['7:00 AM'],
            'Dhuhr': ['12:30 PM'],
            'Asr': ['4:00 PM'],
            'Maghrib': ['6:45 PM'],
            'Isha': ['8:15 PM'],
            'Midnight': ['11:30 PM'],
            'Day_Arabic': ['الإثنين']
        })
        mock_read_csv.return_value = mock_df
        mock_gmtime.return_value = time.gmtime(1704067200)  # Jan 1, 2024
        mock_localtime.return_value = time.localtime(1704096000)

        df, headers, ar_headers, iqama_headers = tc.initializers()
        res = tc.dateComparer(df, headers, iqama_headers, 8)

        self.assertTrue(res[6])  # foundFlag
        self.assertEqual(res[1], '1-January-2024')

    def test_timeComparer_formatting(self):
        current, display, seconds, meridian = tc.timeComparer(0)
        self.assertIsInstance(current, time)
        self.assertIn(meridian, ["AM", "PM"])
        self.assertRegex(display, r"\d{1,2}:\d{2}")


if __name__ == "__main__":
    unittest.main()
