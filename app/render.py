from __future__ import annotations

import html
from pathlib import Path

from app.services.skyforge_service import build_service

service = build_service()


def page_shell(title: str, eyebrow: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #09111d;
      --panel: #101d2f;
      --panel-2: #17263c;
      --line: #29486f;
      --ink: #f3ecde;
      --muted: #b5c2d7;
      --blue: #6db2ff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        radial-gradient(circle at top left, rgba(54, 103, 164, 0.18), transparent 30%),
        linear-gradient(180deg, #08111c 0%, #0b1522 100%);
      color: var(--ink);
      font-family: Georgia, "Times New Roman", serif;
    }}
    .frame {{
      width: 1440px;
      min-height: 920px;
      margin: 0 auto;
      padding: 48px;
    }}
    .shell {{
      background: rgba(13, 24, 39, 0.94);
      border: 1px solid var(--line);
      border-radius: 36px;
      padding: 34px 36px 36px;
    }}
    .eyebrow {{
      margin: 0 0 22px;
      font: 700 13px/1.2 "Segoe UI", sans-serif;
      letter-spacing: 0.35em;
      text-transform: uppercase;
      color: var(--blue);
    }}
    h1 {{
      margin: 0;
      font-size: 68px;
      line-height: 1.02;
      max-width: 1180px;
      letter-spacing: -0.05em;
    }}
    p.lead {{
      margin: 24px 0 0;
      max-width: 1060px;
      color: var(--muted);
      font: 400 19px/1.55 "Segoe UI", sans-serif;
    }}
    .pills {{
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
      margin: 22px 0 26px;
    }}
    .pill {{
      background: #1d2d45;
      border: 1px solid #335a8d;
      color: #f5f7fb;
      padding: 10px 16px;
      border-radius: 999px;
      font: 700 15px/1 "Segoe UI", sans-serif;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      margin: 8px 0 34px;
    }}
    .card {{
      background: var(--panel-2);
      border: 1px solid #335885;
      border-radius: 24px;
      padding: 22px 22px 18px;
      min-height: 170px;
    }}
    .card h2 {{
      margin: 0 0 12px;
      color: #a8cbff;
      font: 700 12px/1.2 "Segoe UI", sans-serif;
      letter-spacing: 0.24em;
      text-transform: uppercase;
    }}
    .metric {{
      font-size: 58px;
      line-height: 1;
      margin: 0 0 10px;
    }}
    .card p, .card li, .table, .lane {{
      color: var(--muted);
      font: 400 18px/1.45 "Segoe UI", sans-serif;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1.2fr 0.9fr;
      gap: 18px;
    }}
    .table {{
      display: grid;
      gap: 12px;
    }}
    .row {{
      display: grid;
      grid-template-columns: 1.1fr 0.8fr 0.75fr 1fr;
      gap: 14px;
      align-items: center;
      padding: 16px 18px;
      background: #0c1728;
      border: 1px solid #223c5d;
      border-radius: 18px;
    }}
    .row strong {{
      color: var(--ink);
      display: block;
      font: 700 24px/1.1 Georgia, serif;
    }}
    .small {{
      font-size: 15px;
      color: #87a2c7;
    }}
    .lane {{
      padding: 16px 18px;
      background: #0c1728;
      border: 1px solid #223c5d;
      border-radius: 18px;
      margin-bottom: 12px;
    }}
    .lane strong {{
      display: block;
      color: var(--ink);
      font: 700 24px/1.15 Georgia, serif;
      margin-bottom: 6px;
    }}
    pre {{
      margin: 0;
      color: #d7e8ff;
      font: 16px/1.5 Consolas, monospace;
      white-space: pre-wrap;
    }}
  </style>
</head>
<body>
  <div class="frame">
    <div class="shell">
      <p class="eyebrow">{html.escape(eyebrow)}</p>
      {body}
    </div>
  </div>
</body>
</html>"""


def render_overview() -> str:
    summary = service.summary()
    vehicles = service.vehicles()[:3]
    rows = "".join(
        f"""
        <div class="row">
          <div>
            <strong>{html.escape(vehicle['name'])}</strong>
            <div class="small">{html.escape(vehicle['corridor'])} · {html.escape(vehicle['task'])}</div>
          </div>
          <div>{vehicle['governanceRisk']}</div>
          <div>{html.escape(vehicle['status'])}</div>
          <div>{html.escape(vehicle['policyEnvelope'])}</div>
        </div>
        """
        for vehicle in vehicles
    )
    body = f"""
      <h1>Keep advanced air mobility fleets inside a governance envelope before separation risk becomes an urban incident.</h1>
      <p class="lead">
        SkyForge is a real-time governance and regulatory control plane for eVTOL fleets and drone-delivery corridors.
        It turns corridor events, holds, overrides, and sequencing chains into one command surface for urban air mobility.
      </p>
      <div class="pills">
        <div class="pill">airspace separation governance</div>
        <div class="pill">vertiport and corridor replay</div>
        <div class="pill">weather and hold policy control</div>
        <div class="pill">human operations override chain</div>
      </div>
      <div class="stats">
        <div class="card"><h2>vehicles online</h2><div class="metric">{summary['vehicleCount']}</div><p>Air mobility assets under live governance supervision.</p></div>
        <div class="card"><h2>contain state</h2><div class="metric">{summary['containCount']}</div><p>Vehicles requiring a tighter corridor envelope right now.</p></div>
        <div class="card"><h2>high severity events</h2><div class="metric">{summary['highSeverityEventCount']}</div><p>Separation and sequencing events needing replay-grade provenance.</p></div>
        <div class="card"><h2>avg. risk</h2><div class="metric">{summary['averageGovernanceRisk']}</div><p>{html.escape(summary['leadRecommendation'])}</p></div>
      </div>
      <div class="grid-2">
        <div class="card"><h2>airspace command</h2><div class="table">{rows}</div></div>
        <div class="card"><h2>lead recommendation</h2><p>{html.escape(summary['leadRecommendation'])}</p></div>
      </div>
    """
    return page_shell("SkyForge", "SkyForge", body)


def render_event_replay() -> str:
    events = service.events()[:4]
    cards = "".join(
        f"""
        <div class="lane">
          <strong>{html.escape(event['vehicleName'])} · {html.escape(event['eventType'])}</strong>
          <div>{html.escape(event['corridor'])} · {html.escape(event['severity'])} · provenance {event['provenanceScore']}</div>
          <div class="small">{html.escape(' → '.join(event['handoffChain']))}</div>
        </div>
        """
        for event in events
    )
    body = f"""
      <h1>Every airspace event keeps a replayable handoff chain so autonomous routing decisions can be audited after the fact.</h1>
      <p class="lead">
        Override state, policy trigger, vertiport sequencing, and corridor handoffs all stay attached to the event record so investigators can reconstruct what happened and why.
      </p>
      <div class="card">
        <h2>event replay lane</h2>
        {cards}
      </div>
    """
    return page_shell("Event Replay", "Event Replay", body)


def render_incident_board() -> str:
    vehicles = [vehicle for vehicle in service.vehicles() if vehicle["status"] != "clear"]
    cards = "".join(
        f"""
        <div class="lane">
          <strong>{html.escape(vehicle['name'])} · {html.escape(vehicle['status'])}</strong>
          <div>Risk {vehicle['governanceRisk']} · separation {vehicle['separationM']} m · battery {vehicle['batteryPct']}%</div>
          <div class="small">{html.escape(vehicle['nextAction'])}</div>
        </div>
        """
        for vehicle in vehicles
    )
    body = f"""
      <h1>The incident board separates watch vehicles from contain vehicles before one routing error propagates across the city grid.</h1>
      <p class="lead">
        Operations teams can see which aircraft need slowdown, hold, reroute, or human release authority without digging through separate systems.
      </p>
      <div class="card">
        <h2>incident board</h2>
        {cards}
      </div>
    """
    return page_shell("Incident Board", "Incident Board", body)


def render_api_summary() -> str:
    payload = service.sample_payload()
    body = f"""
      <h1>The API exposes vehicle risk, event provenance, and next actions in a shape ops and compliance systems can use directly.</h1>
      <p class="lead">
        Fleet state and replay summaries stay close together so downstream systems can trigger holds and archive the decision chain without translation.
      </p>
      <div class="card">
        <h2>sample payload</h2>
        <pre>{html.escape(str(payload))}</pre>
      </div>
    """
    return page_shell("API Summary", "API Summary", body)


def write_static_proof_pages(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = {
        "01-overview.html": render_overview(),
        "02-event-replay.html": render_event_replay(),
        "03-incident-board.html": render_incident_board(),
        "04-api-summary.html": render_api_summary(),
    }
    written: list[Path] = []
    for name, contents in pages.items():
        path = output_dir / name
        path.write_text(contents, encoding="utf-8")
        written.append(path)
    return written
