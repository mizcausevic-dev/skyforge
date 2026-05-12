from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any


def _clamp(value: float, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, round(value)))


@dataclass(slots=True)
class SkyForgeService:
    source_path: Path

    def load(self) -> dict[str, Any]:
        return json.loads(self.source_path.read_text(encoding="utf-8"))

    def vehicles(self) -> list[dict[str, Any]]:
        data = self.load()
        events_by_vehicle: dict[str, list[dict[str, Any]]] = {}
        for event in data["events"]:
            events_by_vehicle.setdefault(event["vehicle_id"], []).append(event)

        enriched: list[dict[str, Any]] = []
        for vehicle in data["vehicles"]:
            history = events_by_vehicle.get(vehicle["vehicle_id"], [])
            critical_events = sum(1 for event in history if event["severity"] == "critical")
            separation_breaches = sum(1 for event in history if event["event_type"] == "separation-breach")
            governance_risk = _clamp(
                max(0, 120 - vehicle["separation_m"]) * 0.55
                + max(0, 60 - vehicle["battery_pct"]) * 0.8
                + max(0, 65 - vehicle["wind_margin_pct"]) * 0.9
                + (14 if not vehicle["override_ready"] else 0)
                + critical_events * 18
                + separation_breaches * 16
                + min(vehicle["last_hold_minutes"], 45) * 0.65
            )
            status = "contain" if governance_risk >= 76 else "watch" if governance_risk >= 48 else "clear"
            next_action = (
                "Freeze autonomous corridor expansion, require human release authority, and preserve the full airspace replay chain."
                if status == "contain"
                else "Hold the vehicle in a tighter corridor envelope and monitor separation and weather constraints before the next slot."
                if status == "watch"
                else "Continue operations with governance telemetry attached to the mission record."
            )
            enriched.append(
                {
                    "vehicleId": vehicle["vehicle_id"],
                    "name": vehicle["name"],
                    "class": vehicle["class"],
                    "corridor": vehicle["corridor"],
                    "task": vehicle["task"],
                    "batteryPct": vehicle["battery_pct"],
                    "separationM": vehicle["separation_m"],
                    "windMarginPct": vehicle["wind_margin_pct"],
                    "overrideReady": vehicle["override_ready"],
                    "policyEnvelope": vehicle["policy_envelope"],
                    "governanceRisk": governance_risk,
                    "status": status,
                    "nextAction": next_action,
                }
            )
        return sorted(enriched, key=lambda item: (-item["governanceRisk"], item["name"]))

    def events(self) -> list[dict[str, Any]]:
        data = self.load()
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        vehicles = {vehicle["vehicleId"]: vehicle for vehicle in self.vehicles()}
        enriched: list[dict[str, Any]] = []
        for event in data["events"]:
            provenance_score = _clamp(
                (30 if event["override_applied"] else 12)
                + len(event["handoff_chain"]) * 12
                + (20 if event["resolution_state"] in {"rerouted", "sequenced"} else 8)
                + (22 if event["severity"] == "critical" else 14 if event["severity"] == "high" else 7)
            )
            enriched.append(
                {
                    "eventId": event["event_id"],
                    "timestamp": event["timestamp"],
                    "vehicleId": event["vehicle_id"],
                    "vehicleName": vehicles.get(event["vehicle_id"], {}).get("name", event["vehicle_id"]),
                    "corridor": event["corridor"],
                    "severity": event["severity"],
                    "eventType": event["event_type"],
                    "policyTriggered": event["policy_triggered"],
                    "handoffChain": event["handoff_chain"],
                    "overrideApplied": event["override_applied"],
                    "resolutionState": event["resolution_state"],
                    "distanceM": event["distance_m"],
                    "provenanceScore": provenance_score,
                }
            )
        return sorted(enriched, key=lambda item: (severity_order[item["severity"]], item["timestamp"]))

    def summary(self) -> dict[str, Any]:
        data = self.load()
        vehicles = self.vehicles()
        events = self.events()
        contain = [vehicle for vehicle in vehicles if vehicle["status"] == "contain"]
        high_events = [event for event in events if event["severity"] in {"critical", "high"}]
        avg_risk = mean(vehicle["governanceRisk"] for vehicle in vehicles)
        avg_provenance = mean(event["provenanceScore"] for event in events)
        return {
            "network": data["network"],
            "city": data["city"],
            "vehicleCount": len(vehicles),
            "containCount": len(contain),
            "highSeverityEventCount": len(high_events),
            "averageGovernanceRisk": round(avg_risk, 1),
            "averageProvenanceScore": round(avg_provenance, 1),
            "leadRecommendation": (
                "Keep the hospital-priority drone and airport-arrival eVTOL inside tighter separation and hold policies, then preserve every override and sequencing branch so flight investigations can replay the chain without ambiguity."
            ),
        }

    def vehicle(self, vehicle_id: str) -> dict[str, Any] | None:
        for vehicle in self.vehicles():
            if vehicle["vehicleId"] == vehicle_id:
                return vehicle
        return None

    def event(self, event_id: str) -> dict[str, Any] | None:
        for event in self.events():
            if event["eventId"] == event_id:
                return event
        return None

    def sample_payload(self) -> dict[str, Any]:
        vehicles = self.vehicles()
        events = self.events()
        return {
            "dashboard": self.summary(),
            "vehicles": [
                {
                    "vehicleId": vehicle["vehicleId"],
                    "name": vehicle["name"],
                    "governanceRisk": vehicle["governanceRisk"],
                    "status": vehicle["status"],
                    "nextAction": vehicle["nextAction"],
                }
                for vehicle in vehicles[:3]
            ],
            "events": [
                {
                    "eventId": event["eventId"],
                    "severity": event["severity"],
                    "eventType": event["eventType"],
                    "resolutionState": event["resolutionState"],
                    "provenanceScore": event["provenanceScore"],
                }
                for event in events[:3]
            ],
        }


def build_service(root: Path | None = None) -> SkyForgeService:
    base = root or Path(__file__).resolve().parents[2]
    return SkyForgeService(base / "app" / "data" / "sample_airspace.json")
