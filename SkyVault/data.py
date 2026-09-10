# Roll Number: cert-aai-2026-06-0002
"""
Mock operational database for AeroWing Airlines.
"""

FLIGHTS = {
    "A1203": {
        "flight_number": "A1203",
        "tail_number": "N101AW",
        "origin": "HYD",
        "destination": "DEL",
        "departure_time": "14:30",
        "status": "Scheduled",
        "assigned_gate": "Gate B12",
        "scheduled_delay_minutes": 0
    },
    "A1405": {
        "flight_number": "A1405",
        "tail_number": "N202AW",
        "origin": "BOM",
        "destination": "BLR",
        "departure_time": "16:00",
        "status": "Boarding",
        "assigned_gate": "Gate A4",
        "scheduled_delay_minutes": 15
    }
}

MAINTENANCE = {
    "N101AW": {
        "tail_number": "N101AW",
        "aircraft_type": "A320",
        "last_inspection": "2026-08-10",
        "hours_flown": 1420,
        "open_issues": ["Auxiliary Power Unit (APU) pressure advisory under review"]
    },
    "N202AW": {
        "tail_number": "N202AW",
        "aircraft_type": "B737",
        "last_inspection": "2026-08-18",
        "hours_flown": 980,
        "open_issues": []
    }
}

GATES = {
    "Terminal 1": ["Gate A1", "Gate A2", "Gate A5"],
    "Terminal 2": ["Gate B3", "Gate B7"]
}

WEATHER = {
    "HYD": {
        "airport": "HYD",
        "visibility": "Low (600m - dense fog)",
        "wind": "18 knots gusting",
        "temperature": "24C",
        "advisory": "Adverse weather alert: Ground holds possible"
    },
    "DEL": {
        "airport": "DEL",
        "visibility": "Good (10km)",
        "wind": "5 knots",
        "temperature": "32C",
        "advisory": "Clear conditions"
    }
}