import unittest
from datetime import datetime, timedelta, timezone
import GUI_static as gui


class TestGUIStatic(unittest.TestCase):

    def test_get_milliseconds_until_midnight(self):
        # Use UTC+8
        now = datetime.now(timezone.utc) + timedelta(hours=8)
        millis = gui.get_milliseconds_until_midnight(8)
        expected = (datetime.combine(now.date() + timedelta(days=1), datetime.min.time(), tzinfo=now.tzinfo) - now).total_seconds() * 1000
        self.assertAlmostEqual(millis, expected, delta=1000)

    def test_status_toggle_runs(self):
        # Should toggle the flag
        current = gui.toggle_state
        gui.status_toggle()
        self.assertNotEqual(current, gui.toggle_state)


if __name__ == "__main__":
    unittest.main()
