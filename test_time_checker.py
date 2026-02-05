import unittest
from datetime import time, datetime
from unittest.mock import patch
import pandas as pd
import time_checker as tc
import os

class Testtime_checker(unittest.TestCase):

    def test_process_prayer_data_logic(self):
        """Tests if the one-time processing correctly builds the dictionary."""
        # Create a temporary dummy CSV
        df_dummy = pd.DataFrame({
            'Date': ['05-Feb-2026'],
            'Hijri': ['17-Syb-1447'],
            'Day': ['Khamis'],
            'Fajr': ['6:02 AM'],
            'Syuruk': ['7:15 AM'],
            'Zohor': ['1:24 PM'],
            'Asar': ['4:45 PM'],
            'Maghrib': ['7:23 PM'],
            'Isyak': ['8:36 PM']
        })
        df_dummy.to_csv('test_prayer.csv', index=False)

        try:
            data = tc.process_prayer_data('test_prayer.csv')
            day_data = data['05-Feb-2026']

            # Check Translations
            self.assertEqual(day_data['Day_En'], 'Thursday')
            self.assertEqual(day_data['Day_Ar'], 'الخميس')
            
            # Check if Midnight was calculated (should be a time object)
            self.assertIsInstance(day_data['Midnight'], time)
            
            # Check Display Strings
            self.assertEqual(day_data['Display']['Fajr'], "6:02 AM")
        finally:
            if os.path.exists('test_prayer.csv'):
                os.remove('test_prayer.csv')

    def test_time_comparer_output(self):
        """Checks if time_comparer returns the correct types and format."""
        current, display, seconds, meridian = tc.time_comparer(8)
        self.assertIsInstance(current, time)
        self.assertEqual(len(seconds), 2)
        self.assertIn(meridian, ["AM", "PM"])

    def test_ramadan_isha_override(self):
        """Verifies that Isha iqamah is 9:15 PM during Ramadan."""
        df_ram = pd.DataFrame({
            'Date': ['01-Mar-2026'],
            'Hijri': ['11-Ram-1447'], # Contains 'Ram'
            'Day': ['Ahad'],
            'Fajr': ['5:50 AM'], 'Syuruk': ['7:00 AM'], 'Zohor': ['1:00 PM'],
            'Asar': ['4:00 PM'], 'Maghrib': ['7:00 PM'], 'Isyak': ['8:15 PM']
        })
        df_ram.to_csv('test_ramadan.csv', index=False)

        try:
            data = tc.process_prayer_data('test_ramadan.csv')
            self.assertEqual(data['01-Mar-2026']['Display']['Isha_iqama'], "9:15 PM")
        finally:
            if os.path.exists('test_ramadan.csv'):
                os.remove('test_ramadan.csv')

if __name__ == "__main__":
    unittest.main()