"""
Tool declarations formatted for  Function Calling.
"""

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_flight_status",
            "description": "Returns operational status, departure time, origin, destination, assigned gate, and assigned tail number for a flight (e.g., 'A1203').",
            "parameters": {
                "type": "object",
                "properties": {
                    "flight_number": {
                        "type": "string",
                        "description": "The unique flight code, such as 'A1203'."
                    }
                },
                "required": ["flight_number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_passenger",
            "description": "Finds passenger booking details, assigned flight, and seat number given a passenger's full or partial name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Full or partial name of the passenger (e.g., 'Rahul Sharma')."
                    }
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "maintenance_history",
            "description": "Retrieves aircraft maintenance records, open mechanical issues, inspection dates, and flight hours for a specific tail number (e.g., 'N101AW').",
            "parameters": {
                "type": "object",
                "properties": {
                    "tail_number": {
                        "type": "string",
                        "description": "The aircraft registration tail number (e.g., 'N101AW')."
                    }
                },
                "required": ["tail_number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_available_gate",
            "description": "Returns open, unassigned gates for a specific terminal (e.g., 'Terminal 1' or 'Terminal 2').",
            "parameters": {
                "type": "object",
                "properties": {
                    "terminal": {
                        "type": "string",
                        "description": "The terminal identifier, such as 'Terminal 1' or 'Terminal 2'."
                    }
                },
                "required": ["terminal"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Fetches current weather observations, visibility, wind speed, and active alerts for a 3-letter IATA airport code (e.g., 'HYD', 'DEL').",
            "parameters": {
                "type": "object",
                "properties": {
                    "airport": {
                        "type": "string",
                        "description": "The 3-letter airport code (e.g., 'HYD', 'DEL', 'BOM')."
                    }
                },
                "required": ["airport"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_aircraft",
            "description": "Provides technical specifications, passenger capacity, and fuel limits for an aircraft type (e.g., 'A320', 'B737').",
            "parameters": {
                "type": "object",
                "properties": {
                    "aircraft_type": {
                        "type": "string",
                        "description": "Aircraft model family code, e.g. 'A320' or 'B737'."
                    }
                },
                "required": ["aircraft_type"]
            }
        }
    }
]