import pandas as pd

games = pd.read_csv('./games.csv', index_col='play_id')
damage = pd.read_csv('./damage_taken_by_floor.csv', index_col='play_id')
relics = pd.read_csv('./relics_obtained_by_floor.csv', index_col='play_id')
cards = pd.read_csv('./card_choices_by_floor.csv', index_col='play_id')

min_floor = 4
max_floor = 57

games = games.dropna()
relics = relics.rename(columns={'key':'relic'})

games = games[games.floor_reached.between(min_floor, max_floor)]
games['num_cards'] = games.master_deck.apply(lambda x: len(x.split(';')))
games['num_relics'] = games.relics.apply(lambda x: len(x.split(';')))
games = games[games.num_cards < 200]
games = games.drop(['master_deck', 'relics'], axis=1)

damage = damage[damage.floor.between(min_floor, max_floor)]
relics = relics[relics.floor.between(min_floor, max_floor)]
cards = cards[cards.floor.between(min_floor, max_floor)]

relics['num_relics'] = relics.groupby('play_id').cumcount() + 1
cards['is_card'] = cards.picked != 'SKIP'
cards['num_cards'] = cards.groupby('play_id').is_card.cumsum()

damage = games.loc[:, ['ascension_level']].merge(damage, left_index=True, right_on='play_id')
relics = games.loc[: , ['victory']].merge(relics, left_index=True, right_on='play_id')

games.to_csv('../games_data_processed.csv', header=True, index=True)
relics.to_csv('../relics_by_floor_data_processed.csv', header=True, index=True)
cards.to_csv('../cards_by_floor_data_processed.csv', header=True, index=True)
damage.to_csv('../damage_by_floor_data_processed.csv', header=True, index=True)