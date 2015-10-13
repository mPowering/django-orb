#!/usr/bin/python
import argparse
import csv
import json
import os, sys


BASE_DIR = os.path.dirname(os.path.dirname(__file__))   
INFILE = os.path.join(BASE_DIR, '1mchw-data.csv')

MAPPING = {
           'Number of children under 5':'no_u5',
           }

def run(): 
    
    with open(INFILE, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for k,v in row.iteritems():
                print k,v
                        
    
if __name__ == "__main__":
    run()
