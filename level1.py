import requests
import sys

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
    for character in characters:
        if character['name'].lower() == name.lower():
            return character
    return None

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
        character = search_character(name, characters)
        
        if character:
            # Get detailed information about the character
            info = get_character_info(character['url'])
            print_character_info(info)
        else:
            print("The force is not strong within you ")
    
    elif option.isdigit():  # Assuming UID is passed as argument
        uid = sys.argv[1]
        info = fetch_character(uid)
        print_character_info(info)
    
    else:
        print("The force is not strong within you")

def print_character_info(info):
    print(f"Name: {info.get('name')}")
    print(f"Height: {info.get('height')} cm")
    print(f"Mass: {info.get('mass')} kg")
    print(f"Birth Year: {info.get('birth_year')}")

if __name__ == "__main__":
    main()
