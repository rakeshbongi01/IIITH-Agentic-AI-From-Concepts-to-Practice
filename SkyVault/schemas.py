# Roll Number: cert-aai-2026-06-0002

FLIGHT_STATUS_SCHEMA = {
    "type": "object",
    "properties": {"flight_number": {"type": "string"}},
    "required": ["flight_number"]
}

WEATHER_SCHEMA = {
    "type": "object",
    "properties": {"airport": {"type": "string"}},
    "required": ["airport"]
}

MAINTENANCE_SCHEMA = {
    "type": "object",
    "properties": {"tail_number": {"type": "string"}},
    "required": ["tail_number"]
}

GATE_SCHEMA = {
    "type": "object",
    "properties": {"terminal": {"type": "string"}},
    "required": ["terminal"]
}