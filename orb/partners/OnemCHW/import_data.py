#!/usr/bin/python
import argparse
import csv
import json
import os, sys


BASE_DIR = os.path.dirname(__file__)  
INFILE = os.path.join(BASE_DIR, '1mchw-data.csv')

MAPPING = {
           'Number of children under 5':'no_children_under5',
           'Number of Community Health Care Workers': 'no_chw',
           'Country Name': 'country_name',
           'Population Estimate': 'pop_est',
           'Number of women in childbearing age': 'no_childbearing_age',
           'Total Fertility Rate': 'fertility_rate',
           'POSTAL': 'country_code',
           'Under 5 Mortality': 'under5_mortality',
           'LASTCENSUS': 'last_census_year'
           }

def run(): 
    
    from orb.partners.OnemCHW.models import CountryData
    
    with open(INFILE, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            country_data, result  = CountryData.objects.get_or_create(country_name=row['Country Name'])
            for k,v in row.iteritems():
                try:
                    setattr(country_data, MAPPING[k], v)
                except KeyError:
                    pass # just ignore as not data we're using         
                
            country_data.save()
            print "saved: ", country_data
            
if __name__ == "__main__":
    import django
    django.setup()
    run()
