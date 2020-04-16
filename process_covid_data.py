#!/usr/bin/env python3
from covid.parser import CovidParser

DATASET_URL = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx'

if __name__ == '__main__':
    parser = CovidParser(DATASET_URL)
    parser.run()