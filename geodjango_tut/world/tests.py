#!/usr/bin/env python3
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from world.models import AirbnbListings
import world.policy_functions

# Create your tests here.

# models test class for all 
class ListingsTestCase(TestCase):
    #method to create listing object 
    def setUp(self):
        AirbnbListingstable.objects.create(id="2", price="44.00")
        #AirbnbListings.objects.all().values #to get all values
        pass
        
    #method to test xyz
    def test_listings_creation():
        pass

    def understand_database_usages():
        QuerySet.explain()
        pass





