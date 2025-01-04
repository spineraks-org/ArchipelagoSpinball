from dataclasses import dataclass

from Options import PerGameCommonOptions, Range

class NotAnOption(Range):
    """
    This game has no options yet :)
    """

    display_name = "Not an option"
    range_start = 160
    range_end = 1000
    default = 300

@dataclass
class YachtDiceOptions(PerGameCommonOptions):
    not_an_option: NotAnOption