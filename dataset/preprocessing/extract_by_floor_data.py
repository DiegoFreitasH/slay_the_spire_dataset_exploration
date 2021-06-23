import ijson
import csv
import argparse

parser = argparse.ArgumentParser(prog='extract_by_floor_data')
parser.add_argument('Feature', choices=['card_choices', 'relics_obtained', 'damage_taken'])
args = parser.parse_args()

input_path = './november.json'
FIELD_PREFIX = 'item.event.'
FEATURE = args.Feature

object_fields = {
    'card_choices': {
        'picked': '',
        'floor': 0
    },
    'relics_obtained': {
        'key': '',
        'floor': 0,
    },
    'damage_taken': {
        'enemies': '',
        'damage': 0,
        'turns': 0,
        'floor': 0
    }
}

header = [k for k in object_fields[FEATURE]]
header.insert(0, 'play_id')
game_record = {}

output_path = f'{FEATURE}_by_floor.csv'

with open(output_path, 'w') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    for prefix, type_of_object, value in ijson.parse(open(input_path)):
        if(prefix == f'{FIELD_PREFIX}play_id'):
            game_record['play_id'] = value
        
        if(prefix.startswith(f'{FIELD_PREFIX}{FEATURE}')):
            if(type_of_object == 'start_array' or type_of_object == 'end_array'):
                continue
            elif(type_of_object not in ['end_map', 'start_map', 'map_key']):
                context, prefix_field = prefix.split('.')[-2:]
                if(context == 'not_picked'):
                    continue
                game_record[prefix_field] = value
                if(type_of_object == 'number'):
                    game_record[prefix_field] = int(game_record[prefix_field])
            elif(type_of_object == 'end_map'):
                writer.writerow(game_record)

    