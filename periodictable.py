import json
import requests
import time
from bs4 import BeautifulSoup

# Pixabay API Key (Replace with your actual API key)
PIXABAY_API_KEY = "37461367-f11ac0f53b95b35a0b6117aa2"
PIXABAY_URL = "https://pixabay.com/api/"

# Wikipedia URL for periodic table
WIKI_URL = "https://en.wikipedia.org/wiki/List_of_chemical_elements"

# General properties description template
PROPERTIES_DESCRIPTION_TEMPLATE = (
    "This element has unique physical and chemical properties that define its behavior. "
    "It belongs to the {category} category and is typically found in {phase} phase under standard conditions. "
    "It is considered a {state}, and its atomic mass is approximately {atomic_mass}. "
    "The element is {reactivity} reactive in nature, influencing its interactions with other substances."
)

# Fetch periodic elements from Wikipedia
def fetch_periodic_elements():
    response = requests.get(WIKI_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"class": "wikitable"})  # Find the table
    rows = table.find_all("tr")[1:]  # Skip header row

    elements = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 8:  # Ensure there are enough columns
            atomic_number = cols[0].text.strip()
            symbol = cols[1].text.strip()
            name = cols[2].text.strip()
            atomic_mass = cols[3].text.strip()
            category = cols[4].text.strip()
            phase = cols[6].text.strip()
            state = cols[7].text.strip()
            reactivity = "reactive" if "reactive" in category.lower() else "non-reactive"
            
            element_description = f"{name} ({symbol}) is an element with atomic number {atomic_number}. It belongs to the {category} category."

            # Generate a general properties description
            properties_description = PROPERTIES_DESCRIPTION_TEMPLATE.format(
                category=category, phase=phase, state=state, atomic_mass=atomic_mass, reactivity=reactivity
            )

            element = {
                "name": name,
                "symbol": symbol,
                "atomicNumber": atomic_number,
                "atomicMass": atomic_mass,
                "description": element_description,  # Element explanation
                "reactive": reactivity,
                "category": category,
                "properties": {
                    "category": category,
                    "phase": phase,
                    "state": state,
                    "reactivity": reactivity,
                    "atomic_mass": atomic_mass
                },
                "property-desc": properties_description  # General properties description
            }
            elements.append(element)

    return elements

# Fetch image from Pixabay
def fetch_image(query):
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "image_type": "photo",
        "per_page": 1
    }
    
    response = requests.get(PIXABAY_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["hits"]:
            return data["hits"][0]["webformatURL"]  # Get image URL
    return None

# Generate JSON with images and detailed data
def generate_json():
    elements = fetch_periodic_elements()
    data_list = []

    for element in elements:
        image_url = fetch_image(element["name"])  # Get Pixabay image
        time.sleep(1)  # Avoid hitting rate limits

        element["image"] = image_url
        data_list.append(element)
        print(f"Fetched: {element['name']}")

    # Save to JSON
    with open("periodic_elements_detailed_pixabay.json", "w") as file:
        json.dump(data_list, file, indent=2)

    print("JSON file generated successfully!")

# Run the script
generate_json()
