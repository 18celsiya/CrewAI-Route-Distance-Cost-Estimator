
import os
from crewai import Agent
from crewai.llm import LLM
from dotenv import load_dotenv
from tools import get_city_distance

load_dotenv()

llm = LLM(
    model="openai/gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7,
    max_tokens=200,
    timeout=120
)

# =======================================
# Distance Calculator Agent
# =======================================
distance_calculator = Agent(
    role="Distance Calculator",
    goal="Calculate the driving distance between a starting_address and a destination_address in the requested unit (km, miles, or NM).",
    llm=llm,
    backstory="""
You are an expert travel assistant specialized in calculating driving distances.

Instructions:
1. Always provide numeric distance in the requested unit only (km, miles).
2. The destination city (city2) is either fixed or provided.
3. Units are case-insensitive (e.g., 'Km', 'MILES').
4. The mode of transport is provided (e.g., driving-car, cycling).
4. If either city is unknown or not found, respond exactly with 'Distance not found'.
5. Only return the numeric distance without extra text when distance is valid.

Examples:
- Input: address1='New York', city2='Los Angeles', unit='miles', mode_of_transport='driving-car'
  Output: 2789

- Input: address1='UnknownCity', city2='Los Angeles', unit='km', mode_of_transport='driving-car'
  Output: Distance not found
""",
    tools=[get_city_distance],
    temperature=0,
    verbose=True,
    memory=True,
    max_execution_time=1200
)

# =======================================
# Travel Cost Calculator Agent
# =======================================
travel_agent = Agent(
    role="Travel Cost Calculator",
    goal="Calculate the travel cost based on the driving distance between starting_address and destination_address.",
    llm=llm,
    backstory="""
You are an expert travel cost calculator.

Instructions:
1. Take the driving distance from the Distance Calculator Agent.
2. The cost rate per unit distance & the currency are provided by the user.
3. Calculate the total travel cost using: total_cost = distance * cost_rate.
4. Always return numeric cost only (integer or float).
5. If the distance is invalid or 'Distance not found', respond exactly with 'Invalid distance'.

Examples:
- Input: distance=2789, cost_rate=2
  Output: 5578

- Input: distance='Distance not found', cost_rate=2
  Output: Invalid distance
""",
    temperature=0,
    verbose=True,
    memory=True,
    max_execution_time=1200
)