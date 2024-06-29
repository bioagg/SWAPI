import requests
import sys

def fetch_all_characters():
    url = 'https://www.swapi.tech/api/people/'
    characters = []
    while url:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        characters.extend(data['results'])
        url = data.get('next')
    return characters

def get_character_info(character_url):
    response = requests.get(character_url)
    response.raise_for_status()
    data = response.json()
    properties = data['result']['properties']
    return properties

def get_planet_info(planet_url):
    response = requests.get(planet_url)
    response.raise_for_status()
    data = response.json()
    properties = data['result']['properties']
    return properties

def search_character(name, characters):
    for character in characters:
        if character['name'].lower() == name.lower():
            return character
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py search <character_name>")
        return
    
    command = sys.argv[1]
    if command == 'search':
        name = ' '.join(sys.argv[2:]) 
        
        # Fetch all characters
        characters = fetch_all_characters()
        
        # Search for the character
        character = search_character(name, characters)
        
        if character:
            # Get detailed information about the character
            info = get_character_info(character['url'])
            print(f"Name: {info.get('name')}")
            print(f"Height: {info.get('height')} cm")
            print(f"Mass: {info.get('mass')} kg")
            print(f"Birth Year: {info.get('birth_year')}")
            
            # Get the homeworld information
            homeworld_url = info.get('homeworld')
            if homeworld_url:
                planet_info = get_planet_info(homeworld_url)
                print("\nHomeworld")
                print("-" * 16)
                print(f"Name: {planet_info.get('name')}")
                print(f"Population: {planet_info.get('population')}")
                
                # Calculate the correlation between an Earth day and an Earth year for the homeworld
                earth_day_in_hours = 24
                earth_year_in_days = 365
                planet_day_in_hours = float(planet_info.get('rotation_period', 0))
                planet_year_in_days = float(planet_info.get('orbital_period', 0))
                
                if planet_day_in_hours > 0 and planet_year_in_days > 0:
                    earth_days_per_planet_day = planet_day_in_hours / earth_day_in_hours
                    earth_years_per_planet_year = planet_year_in_days / earth_year_in_days
                    print(f"On {planet_info.get('name')}, 1 year on Earth is {earth_years_per_planet_year:.2f} years and 1 day is {earth_days_per_planet_day:.2f} days.")
                else:
                    print(f"Unable to calculate correlation for {planet_info.get('name')}.")
        else:
            print("The force is not strong within you")

if __name__ == "__main__":
    main()
