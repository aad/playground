from dataclasses import dataclass, field
from math import asin, cos, radians, sin, sqrt
from typing import List

try:
    from dataclasses_json import dataclass_json
except Exception:
    print("dataclasses-json is required to run some of the tests")


@dataclass
class DataClassCard:
    rank: str
    suit: str


class RegularCard:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit


class RegularCardExtended:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'(rank={self.rank!r}, suit={self.suit!r})')

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (self.rank, self.suit) == (other.rank, other.suit)


# @dataclass(frozen=True)
# class DefaultPosition1:
#     name: str
#     lon: float = 0.0
#     lat: float
# # E   TypeError: non-default argument 'lat' follows default argument


# @dataclass
# class Position2:
#     name: str
#     lon: float
#     lat
#


@dataclass
class Position2:
    name: str
    lon: float
    lat: 0.0


@dataclass
class DefaultPosition:
    name: str
    lon: float = 0.0
    lat: float = 0.0

    def distance_to(self, other):
        r = 6371  # Earth radius in kilometers
        lam_1, lam_2 = radians(self.lon), radians(other.lon)
        phi_1, phi_2 = radians(self.lat), radians(other.lat)
        h = (sin((phi_2 - phi_1) / 2)**2
             + cos(phi_1) * cos(phi_2) * sin((lam_2 - lam_1) / 2)**2)
        return 2 * r * asin(sqrt(h))


@dataclass(frozen=True)
class ImmutablePosition:
    name: str
    lon: float = 0.0
    lat: float = 0.0


@dataclass(frozen=True)
class ImmutableCard:
    rank: str
    suit: str


@dataclass(frozen=True)
class ImmutableDeck:
    cards: List[ImmutableCard]


@dataclass
class Position:
    name: str
    lon: float
    lat: float


@dataclass
class Capital(Position):
    country: str


# @dataclass
# class Capital2(DefaultPosition):
#     country: str # E   TypeError: non-default argument 'country' follows default argument
#
# def __init__(name: str, lon: float = 0.0, lat: float = 0.0, country: str):

# @dataclass
# class Capital2(DefaultPosition):
#     country: str = "default conuntry"


@dataclass
class Capital2(DefaultPosition):
    country: str = 'Unknown'
    lat: float = 40.0


# @dataclass
# class SimplePosition:
#     name: str
#     lon: float
#     lat: float
#
#
# @dataclass
# class SlotPosition:
#     __slots__ = ['name', 'lon', 'lat']
#     name: str
#     lon: float
#     lat: float


@dataclass
class User:
    name: str
    age: int
    is_active: bool


@dataclass
class Users:
    region: str
    total_numbers: int
    users: List[User]


@dataclass_json
@dataclass
class User2:
    name: str
    age: int
    is_active: bool


@dataclass_json
@dataclass
class Users2:
    region: str
    total_numbers: int
    users: List[User]


@dataclass
class User3:
    is_active: bool
    _is_active: bool = field(init=False, repr=False)

    @property
    def is_active(self) -> bool:
        print('getting status')
        return self._is_active

    @is_active.setter
    def is_active(self, is_active: bool):
        print(f"setting status to {is_active}")
        self._is_active = is_active
