import requests
from dotenv import load_dotenv

from langchain.tools import tool
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


# --------------------------------
# Weather Tool
# --------------------------------

@tool
def get_weather(city: str) -> dict:
    """Get the current weather of a city."""

    # ---------- Geocoding API ----------

    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    geocoding_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(
        geocoding_url,
        params=geocoding_params
    )

    data = response.json()
    if "results" not in data or not data["results"]:
        return {
        "error": f"Could not find the city: {city}"
    }


    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]


    # ---------- Weather API ----------

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params
    )

    weather_data = weather_response.json()


    # ---------- Extract weather ----------

    current = weather_data["current"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    wind_speed = current["wind_speed_10m"]


    return {
        "city": city,
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed
    }

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
# --------------------------------
# Gemini
# --------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)


# --------------------------------
# Create Agent
# --------------------------------
tools = [get_weather, add, multiply]

agent = create_agent(
    model=llm,
    tools=tools
)


# --------------------------------
# Ask Agent
# --------------------------------
while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ]
    })

    final_message = result["messages"][-1]

    print("Agent:", final_message.content)