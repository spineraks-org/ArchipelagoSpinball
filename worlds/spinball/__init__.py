import math
from typing import Dict

from BaseClasses import CollectionState, Entrance, Item, ItemClassification, Location, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .Items import YachtDiceItem, item_table
from .Locations import YachtDiceLocation, location_table

from .Options import YachtDiceOptions
from worlds.generic.Rules import set_rule


class YachtDiceWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Yacht Dice. This guide covers single-player, multiworld, and website.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Spineraks"],
        )
    ]


class YachtDiceWorld(World):
    """
    Yacht Dice is a straightforward game, custom-made for Archipelago,
    where you cast your dice to chart a course for high scores,
    unlocking valuable treasures along the way.
    Discover more dice, extra rolls, multipliers,
    and unlockable categories to navigate the depths of the game.
    Roll your way to victory by reaching the target score!
    """

    game: str = "Spinball"
    options_dataclass = YachtDiceOptions

    web = YachtDiceWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}

    location_name_to_id = {name: data.id for name, data in location_table.items()}
    
    ap_world_version = "0.0.1"

    def _get_yachtdice_data(self):
        return {
            # "world_seed": self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
            "race": self.multiworld.is_race,
        }

    def create_items(self):
        self.itempool = ["Open gate", "Spawn boosts"]
        self.multiworld.itempool += [self.create_item(name) for name in self.itempool]

    def create_regions(self):
        # simple menu-board construction
        menu = Region("Menu", self.player, self.multiworld)
        board = Region("Board", self.player, self.multiworld)

        # add locations to board, one for every location in the location_table
        board.locations = [
            YachtDiceLocation(self.player, loc_name, loc_data.id, board)
            for loc_name, loc_data in location_table.items()
            if loc_data.region == board.name
        ]

        # add the regions
        connection = Entrance(self.player, "New Board", menu)
        menu.exits.append(connection)
        connection.connect(board)
        self.multiworld.regions += [menu, board]

    def get_filler_item_name(self) -> str:
        return "Extra ball?"

    def set_rules(self):
        """
        set rules per location, and add the rule for beating the game
        """
    
        self.get_location("Yellow key").access_rule = lambda state: True
        self.get_location("Orange key").access_rule = lambda state: state.has("Open gate", self.player)
        
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Spawn boosts", self.player)
        
    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = YachtDiceItem(name, item_data.classification, item_data.code, self.player)
        return item

