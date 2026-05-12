from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.skyforge_service import build_service


class SkyForgeServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = build_service(ROOT)

    def test_summary_shape(self) -> None:
        summary = self.service.summary()
        self.assertEqual(summary["network"], "Northstar Urban Air Mobility Grid")
        self.assertGreater(summary["vehicleCount"], 0)

    def test_critical_event_lookup(self) -> None:
        event = self.service.event("air-9001")
        self.assertIsNotNone(event)
        self.assertEqual(event["severity"], "critical")

    def test_hospital_priority_drone_is_not_clear(self) -> None:
        vehicle = self.service.vehicle("drn-311")
        self.assertIsNotNone(vehicle)
        self.assertIn(vehicle["status"], {"watch", "contain"})


if __name__ == "__main__":
    unittest.main()
