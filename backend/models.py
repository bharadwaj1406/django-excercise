from django.db import models
from typing import Optional
import uuid

# Create your models here.

class Country (models.Model):
    id : uuid.UUID = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name : str = models.CharField(max_length=100)
    country_code :str = models.CharField(max_length=10)
    currency_symbol :str = models.CharField(max_length=10)
    phone_code :str = models.CharField(max_length= 5)
    
    def __str__(self):
        return f"{self.name} is the country "
    

class State(models.Model):
    id : uuid.UUID = models.UUIDField(primary_key=True,editable= False,default=uuid.uuid4)
    name : str = models.CharField(max_length=100)
    country :Country = models.ForeignKey(Country, on_delete= models.CASCADE , related_name='states')
    state_code : str = models.CharField(max_length=10)
    gst_code : str = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.name} is the state name"
    
class City(models.Model):
    id : uuid.UUID = models.UUIDField(primary_key=True,editable= False,default=uuid.uuid4)
    name : str = models.CharField(max_length=100)
    state :State = models.ForeignKey(State, on_delete= models.CASCADE , related_name='cities')
    state_code : str = models.CharField(max_length=10)
    gst_code : str = models.CharField(max_length=10)
    phone_code :str = models.CharField(max_length= 5)
    city_code: str = models.CharField(max_length=10, unique=True)

    population: int = models.PositiveIntegerField()
    avg_age: float = models.FloatField()
    num_of_adult_males: int = models.PositiveIntegerField()
    num_of_adult_females: int = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.name}, {self.state.name}"
    

    