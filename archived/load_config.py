import json
import os

os.chdir("C:/Users/lukas/Documents/GitHub/bachelor")
with open("request_config.json", 'r') as file:
        config = json.load(file)

orbis_config=config["orbis"]
amadeus_config=config["amadeus"]

amadeus_backup=amadeus_config["backup_name"]
orbis_backup=orbis_config["backup_name"]

amadeus_subsidized=amadeus_config["subsidized"]
orbis_subsidized=orbis_config["subsidized"]

amadeus_subsidized_ids=amadeus_config["subsidized_ids"]
orbis_subsidized_ids=orbis_config["subsidized_ids"]

amadeus_not_subsidized=amadeus_config["not_subsidized"]
orbis_not_subsidized=orbis_config["not_subsidized"]

amadeus_not_subsidized_ids=amadeus_config["not_subsidized_ids"]
orbis_not_subsidized_ids=orbis_config["not_subsidized_ids"]

amadeus_subsidized_filtered=amadeus_config["filtered_subsidized"]
orbis_subsidized_filtered=orbis_config["filtered_subsidized"]

amadeus_game_ev_filtered=amadeus_config["filtered_game_ev_members"]
orbis_game_ev_filtered=orbis_config["filtered_game_ev_members"]