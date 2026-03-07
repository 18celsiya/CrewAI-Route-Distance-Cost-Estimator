import os
from dotenv import load_dotenv
import openrouteservice
from crewai.tools import tool

load_dotenv()

client = openrouteservice.Client(key=os.getenv("ORS_API_KEY"))

@tool("get_city_distance")
def get_city_distance(
    starting_address: str,
    destination_address: str,
    mode_of_transport: str = "driving-car",
    given_unit: str = "km"
) -> float:

    """
    Returns the driving distance between two cities.
    """

    try:
        results_start = client.pelias_search(text=starting_address)['features']
        results_dest = client.pelias_search(text=destination_address)['features']

        if not results_start or not results_dest:
            return "Distance not found"

        coords_start = results_start[0]['geometry']['coordinates']
        coords_dest = results_dest[0]['geometry']['coordinates']

        unit = given_unit.lower()

        if unit not in ["km", "miles"]:
            unit = "km"

        api_unit = "km" if unit == "km" else "mi"

        coords = [coords_start, coords_dest]

        route = client.directions(
            coordinates=coords,
            profile=mode_of_transport,
            units=api_unit
        )

        distance = route['routes'][0]['summary']['distance']

        return round(distance, 2)

    except Exception as e:
        print("Distance calculation error:", e)
        return "Distance not found"