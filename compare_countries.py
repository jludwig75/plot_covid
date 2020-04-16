#!/usr/bin/env python3
from covid.dataset import load_dataset, date_string
from datetime import datetime
import argparse
import os

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('country_list', help='comma separated list of country codes to compare')
args = arg_parser.parse_args()
if args.country_list.lower() == 'all':
    country_list = []
    for file_name in os.listdir('country_data'):
        if file_name.endswith('.csv'):
            country_list.append(file_name[:-len('.csv')].upper())
else:
    country_list = args.country_list.split(',')
country_list.sort()
print(country_list)

country_datasets = []
for geoid in country_list:
    country_datasets.append(load_dataset(geoid))

days = {}
# generate a complete database
for cds in country_datasets:
    for dp in cds.datapoints:
        if dp.date not in days:
            days[dp.date] = {}
        assert cds.geoid not in days[dp.date]
        days[dp.date][cds.geoid] = dp

rows = [(key, value) for key, value in days.items()]
rows.sort(key = lambda row: row[0])
for r in rows:
    print(r[0])

if args.country_list.lower() == 'all':
    file_name_base = 'outputs/compare_all'
else:
    file_name_base = 'outputs/compare_' + '_'.join(country_list)

# generate new cases per 1M pop chart
file_name = file_name_base + '_new_cases_per_1m.csv'
print('generating', file_name)
with open(file_name, 'wt') as file:
    file.write('date')
    for cds in country_datasets:
        file.write(',%s_new_cases' % cds.geoid)
    file.write('\n')
    for r in rows:
        file.write('%s' % date_string(r[0]))
        for cds in country_datasets:
            if cds.geoid in r[1]:
                file.write(',%.3f' % r[1][cds.geoid].new_cases_per_1m)
            else:
                file.write(',')
        file.write('\n')

# generate new deaths per 1M pop chart
file_name = file_name_base + '_new_deaths_per_1m.csv'
print('generating', file_name)
with open(file_name, 'wt') as file:
    file.write('date')
    for cds in country_datasets:
        file.write(',%s_new_deaths' % cds.geoid)
    file.write('\n')
    for r in rows:
        file.write('%s' % date_string(r[0]))
        for cds in country_datasets:
            if cds.geoid in r[1]:
                file.write(',%.3f' % r[1][cds.geoid].new_deaths_per_1m)
            else:
                file.write(',')
        file.write('\n')

# generate cummulative cases per 1M pop chart
file_name = file_name_base + '_cum_cases_per_1m.csv'
print('generating', file_name)
with open(file_name, 'wt') as file:
    file.write('date')
    for cds in country_datasets:
        file.write(',%s_cum_cases' % cds.geoid)
    file.write('\n')
    for r in rows:
        file.write('%s' % date_string(r[0]))
        for cds in country_datasets:
            if cds.geoid in r[1]:
                file.write(',%.3f' % r[1][cds.geoid].cummulative_cases_per_1m)
            else:
                file.write(',')
        file.write('\n')

# generate cummulative deaths per 1M pop chart
file_name = file_name_base + '_cum_deaths_per_1m.csv'
print('generating', file_name)
with open(file_name, 'wt') as file:
    file.write('date')
    for cds in country_datasets:
        file.write(',%s_cum_deaths' % cds.geoid)
    file.write('\n')
    for r in rows:
        file.write('%s' % date_string(r[0]))
        for cds in country_datasets:
            if cds.geoid in r[1]:
                file.write(',%.3f' % r[1][cds.geoid].cummulative_deaths_per_1m)
            else:
                file.write(',')
        file.write('\n')
