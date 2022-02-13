from urllib.request import urlopen
import yaml
import json
import traceback
import os

DICTIONARY_URL = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
INFO_URL = 'https://www.dndbeyond.com/equipment/'
DICTIONARY_FILE = 'Dictionary.yaml'

class Database:
    def __init__(self, name, info):
        self.name = name
        self.info = info
        self.type = self.info['Type']
        self.url = self.info['Url']
        self.data_path = self.info['Data Path']
        self.dictionary = load_dictionary()
        print(yaml.safe_dump(self.dictionary))

    def download(self):
        raw_filename = f'{self.name}-raw.yaml'
        print(f'loading raw data from {raw_filename}')
        card_data_root = open_cards(raw_filename)
        try:
            list_url = f'{self.url}{self.data_path}'
            print(f'list_url {list_url}')
            response = urlopen(list_url)

            download_data = yaml.safe_load(response.read())
            with open(self.name + '-list.yaml', 'w') as f:
                f.write(yaml.safe_dump(download_data, sort_keys=False))
            for result in self.get_results(download_data):
                card_name = result['name']
                card_url = result['url']
                full_card_url = f'{self.url}{card_url}'
                if card_name not in card_data_root['Cards']:
                    print(f'downloading {card_name} from {full_card_url}')
                    card_info_response = urlopen(full_card_url, timeout=3)
                    card_info = yaml.safe_load(card_info_response.read())
                    card_data_root['Cards'][card_name] = card_info
        except Exception:
            traceback.print_exc()
        finally:
            print(f'saving raw data from {raw_filename}')
            with open(raw_filename, 'w') as f:
                f.write(yaml.safe_dump(card_data_root, sort_keys=False))

    def get_results(self, download_data):
        if 'results' in download_data:
            return download_data['results']
        if type(download_data) is list:
            return download_data

    def import_database(self):
        try:
            filename = f'{self.name}.yaml'
            print(f'loading card data from {filename}')
            card_data_root = open_cards(filename)
            raw_data = open_file(self.name + '-raw.yaml', {})
            count = 0
            for raw_card_name in raw_data['Cards']:
                count += 1
                print(f'importing {raw_card_name}')
                raw_card_info = raw_data['Cards'][raw_card_name]
                card_data_root['Cards'][raw_card_name] = self.get_card_info(raw_card_name, raw_card_info)
        except Exception:
            traceback.print_exc()
        finally:
            print(f'Saving {count} cards to {filename}')
            with open(filename, 'w') as f:
                f.write(yaml.safe_dump(card_data_root, sort_keys=False))

    def get_card_info(self, name, info):
        if '/api/equipment/' in info['url']:
            return self.get_equipment_info(name, info)
        if '/api/spells/' in info['url']:
            return self.get_spell_info(name, info)

    def get_equipment_info(self, name, info):
        card_url = info['url']
        description = ' '.join(info.get('desc', ''))
        print(f'description {description}')
        if info.get('desc', '') == '':
            print(f'description: {description}')
            description = get_definition(name.lower(), self.dictionary)
            print(f'description after: {description}')
        return {
            'Type': 'Item',
            'Category': info['equipment_category']['name'],
            'Cost': str(info.get('cost', {}).get('quantity', '')) + info.get('cost', {}).get('unit', ''),
            'Weight': str(info.get('weight', '')) + 'lb',
            'Rarity': 'Common',
            'Description': description,
            'Image': f'Items/{name}.png',
            'Links': [f'{self.url}{card_url}'],
        }

    def get_spell_info(self, name, info):
        card_url = info['url']
        description = ' '.join(info.get('desc', ''))
        if info.get('desc', '') == '':
            print(f'description before: {description}')
            description = get_definition(name.lower(), self.dictionary)
            print(f'description after: {description}')

        return {
            'Type': 'Item',
            'Range': info.get('range', ''),
            'School': info['school']['name'],
            'Duration': info['duration'],
            'Casting Time': info['casting_time'],
            'Attack Type': info.get('attack_type', ''),
            'Level': info['level'],
            'Description': description,
            'Image': f'Items/{name}.png',
            'Links': [f'{self.url}{card_url}'],
        }

def get_definition(word, dictionary):
    try:
        if word in dictionary:
            print(f'in dictionary: {word}')
            return dictionary[word]
        definition = get_online_definition(word)
        if definition or definition == '':
            dictionary[word] = definition
            save_dictionary(dictionary)
            return definition
        return ''
    except Exception:
        traceback.print_exc()

def get_online_definition(word):
    try:
        if ' ' in word:
            return ''
        url = f'{DICTIONARY_URL}{word}'
        print(f'url: {url}')
        response = urlopen(url)
        string = response.read().decode('utf-8')
        print(f'string: {string}')
        result = json.loads(string)
        print(f'definition: {result}')
        return result[0]['meanings'][0]['definitions'][0]['definition']
    except Exception:
        print(f'no definition for {word}')
        traceback.print_exc()
        return ''

def load_dictionary():
    return open_file(DICTIONARY_FILE, {})

def save_dictionary(dictionary):
    with open(DICTIONARY_FILE, 'w') as f:
        f.write(yaml.safe_dump(dictionary, sort_keys=False))

def open_cards(filename):
    return open_file(filename, {'Cards': {}})

def open_file(filename, default):
    if not os.path.isfile(filename):
        return default
    with open(filename) as file:
        data = yaml.safe_load(file)
    return data

def import_databases(file):
    databases = load_databases(file)
    for database_info_name in databases:
        database = Database(database_info_name, databases[database_info_name])
        database.import_database()

def load_databases(filename):
    databases = open_file(filename, {}).get('Card Databases', {})
    return databases

def download_databases(filename):
    databases = load_databases(filename)
    for database_info_name in databases:
        database = Database(database_info_name, databases[database_info_name])
        database.download()
