import typing

from BaseClasses import Location

class LocData(typing.NamedTuple):
    id: int
    region: str


class YachtDiceLocation(Location):
    game: str = "Spinball"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)

location_table = {"Yellow key": LocData(6007209100, "Board"),
                  "Orange key": LocData(6007209101, "Board")}