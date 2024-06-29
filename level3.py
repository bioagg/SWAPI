import requests
import sys
import datetime
import pickle
import os

CACHE_FILE = 'cache.pkl'

# Φόρτωση του cache από το αρχείο, αν υπάρχει
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'rb') as f:
        cache = pickle.load(f)
else:
    cache = {}

def fetch_character(uid):
    url = f'https://www.swapi.tech/api/people/{uid}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['result']['properties']

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

def get_homeworld_info(homeworld_url):
    response = requests.get(homeworld_url)
    response.raise_for_status()
    data = response.json()
    properties = data['result']['properties']
    return properties

def search_character(name, characters, include_homeworld=False):
    name_lower = name.lower()
    if name_lower in cache:
        character_info, timestamp = cache[name_lower]
        print_character_info(character_info, timestamp)
        if include_homeworld and 'homeworld' in character_info:
            homeworld_info = get_homeworld_info(character_info['homeworld'])
            print_homeworld_info(homeworld_info)
        return character_info
    else:
        for character in characters:
            if character['name'].lower() == name_lower:
                character_info = get_character_info(character['url'])
                cache[name_lower] = (character_info, datetime.datetime.now())
                save_cache()
                print_character_info(character_info)
                if include_homeworld and 'homeworld' in character_info:
                    homeworld_info = get_homeworld_info(character_info['homeworld'])
                    print_homeworld_info(homeworld_info)
                return character_info
    return None

#εδώ φτιαχνω τη λειτουργια να καθαρίζει τη cache απο δεδεομενα που εχει 
#ηδη κανει αναζητηση 
#Όταν εκτελείς την εντολή python main.py cache --clean, ο κώδικας καλεί τη συνάρτηση 
# clear_cache, η οποία διαγράφει τα δεδομένα της cache από τη μνήμη και αφαιρεί το αρχείο cache.pkl.
def clear_cache():
    global cache
    cache = {}
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
    print("Cache cleared")

def remove_from_cache(name):
    name_lower = name.lower()
    if name_lower in cache:
        del cache[name_lower]
        save_cache()
        print(f"Removed {name} from cache")
    else:
        print(f"{name} not found in cache")

def print_cache():
    print("Current cache contents:")
    for key, value in cache.items():
        print(f"{key}: {value}")

def save_cache():
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(cache, f)

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <option> <character_name or uid>")
        return
    
    option = sys.argv[1]
    
    if option == 'search':
        include_homeworld = '--world' in sys.argv
        name = ' '.join(arg for arg in sys.argv[2:] if arg != '--world')
        
        # Fetch all characters
        characters = fetch_all_characters()
        
        # Search for the character
        character_info = search_character(name, characters, include_homeworld)
        
        if not character_info:
            print("Character not found")
    
    elif option == 'clear_cache':
        clear_cache()
    
    elif option == 'print_cache':
        print_cache()
        
    elif option == 'cache' and len(sys.argv) > 2:
        sub_option = sys.argv[2]
        if sub_option == '--clean':
            clear_cache()
        elif sub_option == '--remove' and len(sys.argv) > 3:
            name = ' '.join(sys.argv[3:])
            remove_from_cache(name)

    
    elif option.isdigit():  # Assuming UID is passed as argument
        uid = sys.argv[1]
        character_info = fetch_character(uid)
        print_character_info(character_info)
    
    else:
        print("Invalid option. Usage: python main.py <option> <character_name or uid>")

def print_character_info(info, timestamp=None):
    print(f"Name: {info.get('name')}")
    print(f"Height: {info.get('height')} cm")
    print(f"Mass: {info.get('mass')} kg")
    print(f"Birth Year: {info.get('birth_year')}")
    if timestamp:
        print(f"cached: {timestamp}")

def print_homeworld_info(info):
    print("\nHomeworld")
    print("----------------")
    print(f"Name: {info.get('name')}")
    print(f"Population: {info.get('population')}")
    
    orbital_period = float(info.get('orbital_period', 0))
    rotation_period = float(info.get('rotation_period', 0))
    
    print(f"On {info.get('name')}, 1 year on earth is {orbital_period / 365.25:.2f} years and 1 day {rotation_period / 24:.2f} days")

if __name__ == "__main__":
    main()
