import typing


from BaseClasses import Item, ItemClassification

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification

class YachtDiceItem(Item):
    game: str = "Spinball"

item_table = {"Open gate": ItemData(1000209000, ItemClassification.progression),
              "Spawn boosts": ItemData(1000209001, ItemClassification.progression)}
