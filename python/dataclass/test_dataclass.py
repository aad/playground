import pytest
from pytest import mark as m

from dataclasses import make_dataclass, FrozenInstanceError

from example import DataClassCard, RegularCard, RegularCardExtended
from example import Position2, DefaultPosition
from example import ImmutablePosition, ImmutableCard, ImmutableDeck
from example import Capital, Capital2
from example import Users, Users2, User3

NO_DACITE = False
try:
    from dacite import from_dict, MissingValueError
except:
    NO_DACITE = True

NO_DATACLASS_JSON = False
try:
    from dataclasses_json import dataclass_json
except:
    NO_DATACLASS_JSON = True


@m.describe("Compare basic dataclass and regular class")
class TestCompareTheBasics(object):
    @m.context("When dataclass DataClassCard is instantiated")
    @m.context("https://www.python.org/dev/peps/pep-0557/#id34")
    @m.it("Can print and compare")
    def test_basic_dataclass(self, capsys):
        queen_of_hearts = DataClassCard('Q', 'Hearts')
        assert queen_of_hearts.rank == "Q"
        print(queen_of_hearts)
        captured = capsys.readouterr()
        assert captured.out == "DataClassCard(rank='Q', suit='Hearts')\n"
        assert queen_of_hearts.__repr__() == "DataClassCard(rank='Q', suit='Hearts')"
        assert queen_of_hearts == DataClassCard('Q', 'Hearts')
        assert DataClassCard.__eq__(queen_of_hearts, DataClassCard(rank='Q', suit='Hearts'))

    @m.context("When regular class RegularCard is instantiated")
    @m.it("Can not print and compare by default")
    def test_basic_regular_class(self, capsys):
        queen_of_hearts = RegularCard('Q', 'Hearts')
        assert queen_of_hearts.rank == "Q"
        print(queen_of_hearts)
        captured = capsys.readouterr()
        assert "<example.RegularCard" in captured.out
        assert queen_of_hearts != RegularCard('Q', 'Hearts')

    @m.context("When regular class RegularCardExtended is instantiated")
    @m.it("Can print and compare")
    def test_basic_regular_class_extended(self, capsys):
        queen_of_hearts = RegularCardExtended('Q', 'Hearts')
        assert queen_of_hearts.rank == "Q"
        print(queen_of_hearts)
        captured = capsys.readouterr()
        assert captured.out == "RegularCardExtended(rank='Q', suit='Hearts')\n"
        assert queen_of_hearts.__repr__() == "RegularCardExtended(rank='Q', suit='Hearts')"
        assert queen_of_hearts == RegularCardExtended('Q', 'Hearts')


@m.describe("More Position Examples...")
class TestBasicExample(object):
    @m.context("When dataclass Position is created by make_dataclass")
    @m.it("It is (almost) equivalent to the definition of Position with decorator")
    def test_make_dataclass(self, capsys):
        Position = make_dataclass('Position', ['name', 'lon', 'lat'])
        pos = Position('Oslo', 10.8, 59.9)
        print(pos)
        captured = capsys.readouterr()
        assert captured.out == "Position(name='Oslo', lon=10.8, lat=59.9)\n"
        assert pos.lat == 59.9

    @m.context("When dataclass Position has default values")
    @m.it("Can print and compare")
    def test_defaults(self):
        assert DefaultPosition('Null Island').__repr__() == "DefaultPosition(name='Null Island', lon=0.0, lat=0.0)"
        assert DefaultPosition('Greenwich', lat=51.8).__repr__() == \
            "DefaultPosition(name='Greenwich', lon=0.0, lat=51.8)"
        oslo = DefaultPosition('Oslo', 10.8, 59.9)
        vancouver = DefaultPosition('Vancouver', -123.1, 49.3)
        assert oslo.distance_to(vancouver) == 7181.784122942119

    @m.context("Type hint is required")
    @m.it("0.0 was treated as type..")
    def test_defaults2(self):
        with pytest.raises(TypeError):
            Position2('n', '1')
            # TypeError: __init__() missing 1 required positional argument: 'lat'
        assert Position2('n', '1', '2') == Position2(name='n', lon='1', lat='2')


@m.describe("Immutable dataclass")
class TestImmutable(object):
    @m.context("When dataclass ImmutablePosition is frozen")
    @m.it("assign value will raise FrozenInstanceError")
    def test_frozen(self):
        pos = ImmutablePosition('Oslo', 10.8, 59.9)
        with pytest.raises(FrozenInstanceError):
            pos.name = 'Stockholm'

    @m.context("When dataclass PositionImmutable is frozen")
    @m.it("can assign mutable fields")
    def test_frozen_with_mutable_fields(self):
        queen_of_hearts = ImmutableCard('Q', '♡')
        ace_of_spades = ImmutableCard('A', '♠')
        deck = ImmutableDeck([queen_of_hearts, ace_of_spades])
        assert deck == ImmutableDeck(cards=[ImmutableCard(rank='Q', suit='♡'), ImmutableCard(rank='A', suit='♠')])
        deck.cards[0] = ImmutableCard('7', '♢')
        assert deck == ImmutableDeck(cards=[ImmutableCard(rank='7', suit='♢'), ImmutableCard(rank='A', suit='♠')])


@m.describe("Dataclass inheritance")
class TestInheritance(object):
    @m.context("When dataclass is inherited from another class")
    @m.it("will just work")
    def test_simple_inheritance(self):
        assert Capital('Oslo', 10.8, 59.9, 'Norway') == Capital(name='Oslo', lon=10.8, lat=59.9, country='Norway')

    @m.context("When fields are overridden")
    @m.it("fields order is reserved")
    def test_field_order(self):
        assert Capital2('Madrid', country='Spain') == Capital2(name='Madrid', lon=0.0, lat=40.0, country='Spain')


@m.describe("From JSON to dataclass")
class TestJson(object):
    @m.context("When I use dacite")
    @m.it("will just work")
    @pytest.mark.skipif(NO_DACITE, reason="requires dacite")
    def test_dacite_from_dict(self, response_json):
        result = from_dict(data_class=Users, data=response_json)
        assert result.users[0].name == "John"
        assert result.users[1].is_active

    @m.it("Missing value will raise MissingValueError")
    @pytest.mark.skipif(NO_DACITE, reason="requires dacite")
    def test_dacite_missing_value(self, response_json_invalid):
        with pytest.raises(MissingValueError) as e:
            from_dict(data_class=Users, data=response_json_invalid)
        assert str(e.value) == 'missing value for field "users.age"'

    @m.context("When I use dataclass_json")
    @m.it("will just work")
    @pytest.mark.skipif(NO_DATACLASS_JSON, reason="requires dataclass_json")
    def test_dataclass_json_from_json(self, response_json):
        import json
        result = Users2.from_json(json.dumps(response_json))
        assert result.users[0].name == "John"
        assert result.users[1].is_active

    @m.context("When I use dataclass_json")
    @m.it("Missing value will raise MissingValueError")
    @pytest.mark.skipif(NO_DATACLASS_JSON, reason="requires dataclass_json")
    def test_dataclass_json_missing_value(self, response_json_invalid):
        with pytest.raises(KeyError) as e:
            import json
            Users2.from_json(json.dumps(response_json_invalid))
        assert str(e.value) == "'age'"


@m.describe("Make properties work")
class TestProperties(object):
    @m.context("Add the associated private variable using field(init=False, repr=False")
    def test_properties(self, capsys):
        user = User3(False)
        captured = capsys.readouterr()
        assert "setting status to False" in captured.out
        user.is_active
        captured = capsys.readouterr()
        assert "getting status" in captured.out


"""
[PEP 557 -- Data Classes](https://www.python.org/dev/peps/pep-0557)
[The Ultimate Guide to Data Classes in Python 3.7](https://realpython.com/python-data-classes/)
[Reconciling Dataclasses And Properties In Python](https://florimond.dev/blog/articles/2018/10/reconciling-dataclasses-and-properties-in-python/)
"""