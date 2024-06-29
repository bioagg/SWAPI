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

def search_character(name, characters):
    name_lower = name.lower()
    if name_lower in cache:
        character_info, timestamp = cache[name_lower]
        print_character_info(character_info, timestamp)
        return character_info
    else:
        for character in characters:
            if character['name'].lower() == name_lower:
                character_info = get_character_info(character['url'])
                cache[name_lower] = (character_info, datetime.datetime.now())
                save_cache()
                print_character_info(character_info)
                return character_info
    return None

def clear_cache():
    global cache
    cache = {}
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
    print("Cache cleared")

def remove_from_cache(character_name):
    name_lower = character_name.lower()
    if name_lower in cache:
        del cache[name_lower]
        save_cache()
        print(f"Removed {character_name} from cache")
    else:
        print(f"{character_name} not found in cache")

def print_cache():
    print("Current cache contents:")
    for key, value in cache.items():
        print(f"{key}: {value}")

def visualize_cache():
    if not cache:
        print("Cache is empty.")
        return
    
    print(f"{'Search Term':<20} {'Result':<80} {'Timestamp':<30}")
    print("="*130)
    for key, (value, timestamp) in cache.items():
        result = f"Name: {value.get('name')}, Height: {value.get('height')} cm, Mass: {value.get('mass')} kg, Birth Year: {value.get('birth_year')}"
        print(f"{key:<20} {result:<80} {timestamp}")

def save_cache():
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(cache, f)

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <option> <character_name or uid>")
        return
    
    option = sys.argv[1]

    if option == 'search':
        name = ' '.join(sys.argv[2:])
        
        # Fetch all characters
        characters = fetch_all_characters()
        
        # Search for the character
        character_info = search_character(name, characters)
        
        if not character_info:
            print("Character not found")
    
    elif option == 'clear_cache':
        clear_cache()
    
    elif option == 'print_cache':
        print_cache()

    elif option == 'cache' and len(sys.argv) > 2 and sys.argv[2] == '--remove':
        character_name = ' '.join(sys.argv[3:])
        remove_from_cache(character_name)

    elif option == 'visualize_cache':
        visualize_cache()
        
    elif option.isdigit():  # Assuming UID is passed as argument
        uid = sys.argv[1]
        character_info = fetch_character(uid)
        print_character_info(character_info)
    
    else:
        print("Invalid option. Usage: python main.py <option> <character_name or uid>")

    # Αποθήκευση του cache στο αρχείο
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(cache, f)

def print_character_info(info, timestamp=None):
    print(f"Name: {info.get('name')}")
    print(f"Height: {info.get('height')} cm")
    print(f"Mass: {info.get('mass')} kg")
    print(f"Birth Year: {info.get('birth_year')}")
    if timestamp:
        print(f"cached: {timestamp}")

if __name__ == "__main__":
    main()
