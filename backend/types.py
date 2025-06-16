from typing import TypedDict
import uuid


class CountryDict(TypedDict):
    id: uuid.UUID
    name: str
    country_code: str
    currency_symbol: str
    phone_code: str


class StateDict(TypedDict):

    id: uuid.UUID
    name: str
    state_code: str
    gst_code: str
    country_id: uuid.UUID


class CityDict(TypedDict):
    id: uuid.UUID
    name: str
    city_code: str
    phone_code: str
    population: int
    avg_age: float
    num_of_adult_males: int
    num_of_adult_females: int
    state_id: uuid.UUID
