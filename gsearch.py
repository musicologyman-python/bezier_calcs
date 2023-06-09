#!/usr/bin/env python3

import argparse
from datetime import date, timespan
from urllib.parse import parse_qs, urlsplit

CHOICES = { 
        0.5: timedelta(days=182),
        1: timedelta(days=365),
        2: timedelta(days=730),
        3: timedelta(days=1095),
        4: timedelta(days=1461),
        5: timedelta(days=1826),
        30: None
      }

def setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('search_term', type=str)
    parser.add_argument('date_range', default=3, type=int,
                        choices=list(CHOICES.keys()))
    parser.add_argument('--lit', '--literal', type=bool, 
                        action='store_true', default=false)
    return parser.parse_args()

def process_date_range(choice):
    try:
       start_date = CHOICES[choice]
    
    if start_date:
        ecd_min': strftime(date.today() - start_date, 
                          '%Y/%m/%d')
        'cd_max': strftime(date.today(), '%Y/%m/%d')
        


def main():
    ns = setup()
    

  

if __name__ == '__main__':
  main()
