from crewai import Task
from agents import distance_calculator, travel_agent

# =======================================
# Task 1: Distance Calculation
# =======================================
distance_task = Task(
    description="""
    Find the driving distance between {starting_address} and {destination_address} using the specified mode_of_transport {mode_of_transport}.
    You must use the get_city_distance tool to calculate the distance.
    Do not guess the distance.
""",
    agent=distance_calculator,
    expected_output="Numeric distance in requested unit (km or miles)."
)

# =======================================
# Task 2: Travel Cost Calculation
# =======================================
travel_cost_task = Task(
    description="""
Using the distance provided in {distance} and the cost rate {cost_rate}, calculate the total travel cost.
Return numeric output only.
If the distance is invalid or missing, handle it in the calling code (e.g., write 'NA' to Excel).
""",
    agent=travel_agent,
    expected_output="Total travel cost in {currency}",
    context=[distance_task]
)