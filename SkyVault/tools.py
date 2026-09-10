# Roll Number: cert-aai-2026-06-0002
from data import FLIGHTS, WEATHER, MAINTENANCE, GATES

def get_flight_status(flight_number: str) -> dict:
    return FLIGHTS.get(flight_number, {"error": "Flight not found"})

def get_weather(airport: str) -> dict:
    if airport == "ERR":
        raise ValueError("Simulated weather API failure")
    return WEATHER.get(airport, {"error": "Airport not found"})

def maintenance_history(tail_number: str) -> dict:
    return MAINTENANCE.get(tail_number, {"error": "Tail number not found"})

def find_available_gate(terminal: str) -> str:
    gates = GATES.get(terminal, [])
    return gates[0] if gates else "No gates available"