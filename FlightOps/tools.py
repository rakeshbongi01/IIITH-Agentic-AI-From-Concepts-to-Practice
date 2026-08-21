"""
Standalone Python tool functions that interact with the mock data backend.
Includes structured error handling for failure tolerance.
"""
from data import FLIGHTS, PASSENGERS, MAINTENANCE, GATES, WEATHER, AIRCRAFT


def get_flight_status(flight_number: str) -> dict:
    """Returns current operational status, gate, and schedule for a flight."""
    try:
        flight = FLIGHTS.get(flight_number.upper())
        if not flight:
            return {"status": "error", "message": f"Flight '{flight_number}' not found."}
        return {"status": "success", "data": flight}
    except Exception as e:
        return {"status": "error", "message": f"Failed to fetch flight status: {str(e)}"}


def search_passenger(name: str) -> dict:
    """Returns booking information and seat details for a passenger."""
    try:
        # Case-insensitive search
        for passenger_name, details in PASSENGERS.items():
            if name.lower() in passenger_name.lower():
                return {"status": "success", "data": details}
        return {"status": "error", "message": f"Passenger '{name}' not found in manifest."}
    except Exception as e:
        return {"status": "error", "message": f"Failed to search passenger: {str(e)}"}


def maintenance_history(tail_number: str) -> dict:
    """Returns maintenance logs, flight hours, and open issues for an aircraft."""
    try:
        record = MAINTENANCE.get(tail_number.upper())
        if not record:
            return {"status": "error", "message": f"No maintenance records for tail '{tail_number}'."}
        return {"status": "success", "data": record}
    except Exception as e:
        return {"status": "error", "message": f"Maintenance lookup failed: {str(e)}"}


def find_available_gate(terminal: str) -> dict:
    """Returns open gates available in the specified terminal."""
    try:
        open_gates = GATES.get(terminal)
        if not open_gates:
            return {
                "status": "error",
                "message": f"Terminal '{terminal}' not recognized. Available terminals: {list(GATES.keys())}"
            }
        return {"status": "success", "data": {"terminal": terminal, "available_gates": open_gates}}
    except Exception as e:
        return {"status": "error", "message": f"Gate search failed: {str(e)}"}


def get_weather(airport: str) -> dict:
    """
    Returns weather conditions for an airport code.
    Simulates a resilient failure for airport code 'ERR'.
    """
    try:
        airport_code = airport.upper().strip()
        if airport_code == "ERR":
            # Simulated service outage
            return {"status": "error", "message": "Weather service API temporarily unreachable for station ERR."}
        
        weather_info = WEATHER.get(airport_code)
        if not weather_info:
            return {"status": "error", "message": f"No weather station data found for '{airport_code}'."}
        return {"status": "success", "data": weather_info}
    except Exception as e:
        return {"status": "error", "message": f"Weather query error: {str(e)}"}


def lookup_aircraft(aircraft_type: str) -> dict:
    """Returns technical specs and capacity for an aircraft model."""
    try:
        model = AIRCRAFT.get(aircraft_type.upper())
        if not model:
            return {"status": "error", "message": f"Aircraft model '{aircraft_type}' not found."}
        return {"status": "success", "data": model}
    except Exception as e:
        return {"status": "error", "message": f"Aircraft lookup error: {str(e)}"}


# Registry mapping tool names to callable Python functions
TOOL_REGISTRY = {
    "get_flight_status": get_flight_status,
    "search_passenger": search_passenger,
    "maintenance_history": maintenance_history,
    "find_available_gate": find_available_gate,
    "get_weather": get_weather,
    "lookup_aircraft": lookup_aircraft,
}