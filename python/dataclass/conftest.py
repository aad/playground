import pytest


@pytest.fixture
def response_json():
    return {
        'region': 'ap',
        'data_that_i_dont_care1': 's1',
        'total_numbers': 2,
        'users': [
            {
                'name': 'John',
                'age': 1,
                'is_active': True,
                'data_that_i_dont_care2': False,
            },
            {
                'name': 'Jane',
                'is_active': True,
                'age': 2,
                'something_more': False,
            }
        ]
    }


@pytest.fixture
def response_json_invalid():
    return {
        'region': 'ap',
        'data_that_i_dont_care1': 's1',
        'total_numbers': 3,
        'users': [
            {
                'name': 'John',
                'age': 1,
                'is_active': True,
                'data_that_i_dont_care2': False,
            },
            {
                'name': 'Jane',
                'age': 2,
                'is_active': True,
                'something_more': False,
            },
            {
                'name': 'foo',
                'i_missed_something': True,
                'is_active': True,
            }
        ]
    }
