import ijson
import csv
import pandas

'''
Attrs:
    Play_id
    gold_per_floor
    floor_reached
    playtime
    items_purged
    score
    local_time
    is_ascension_mode
    campfire_choices
    neow_cost
    seed_source_timestamp
    circlet_count
    master_deck
    relics
    potions_floor_usage
    damage_taken
    seed_played
    potions_obtained
    is_trial
    path_per_floor
    character_chosen
    items_purchased
    campfire_rested
    item_purchase_floors
    current_hp_per_floor
    gold
    neow_bonus
    is_prod
    is_daily
    chose_seed
    campfire_upgraded
    win_rate
    timestamp
    path_taken
    build_version
    purchased_purges
    victory
    max_hp_per_floor
    card_choices
    player_experience
    relics_obtained
    event_choices
    is_beta
    boss_relics
    items_purged_floors
    is_endless
    potions_floor_spawned
    killed_by
    ascension_level
'''

FIELD_PREFIX = 'item.event.'

def match(prefix, field_name, is_array=False):
    if(is_array):
        return prefix.startswith(f'{FIELD_PREFIX}{field_name}') and not prefix.startswith(f'{FIELD_PREFIX}{field_name}_')
    return prefix == f'{FIELD_PREFIX}{field_name}'

selected_fields = [
    'play_id',
    'victory',
    'character_chosen',
    'score',
    'floor_reached',
    'ascension_level',
    'killed_by',
    'master_deck',
    'playtime',
    'player_experience',
    'relics',
]

array_fields = {
    'master_deck': [],
    'relics': [],
}

game_record = {}
input_path = './november.json'
output_path = 'games.csv'
with open(output_path, 'w') as file:
    writer = csv.DictWriter(file, fieldnames=selected_fields)
    writer.writeheader()
    
    for prefix, type_of_object, value in ijson.parse(open(input_path)):
        
        for field in selected_fields:
            if(match(prefix, field)):
                game_record[field] = value
            
        for field in array_fields:
            if(match(prefix, field, is_array=True)):
                if(type_of_object == 'start_array'):
                    array_fields[field] = []
                elif(type_of_object != 'end_array'):
                    array_fields[field].append(value)
                else:
                    game_record[field] = ';'.join(array_fields[field])
        
        if(prefix == 'item.event' and type_of_object == 'end_map'):
            writer.writerow(game_record)


