#!/usr/bin/python
import argparse
import csv
import json
import os, sys


BASE_DIR = os.path.dirname(os.path.dirname(__file__))   
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
           }

def run(): 
    
    with open(INFILE, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for k,v in row.iteritems():
                try:
                    print MAPPING[k],v
                except KeyError:
                    pass # just ignore as not data we're using         
    
if __name__ == "__main__":
    run()
