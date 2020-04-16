#!/usr/bin/env python3
from covid.dataset import load_dataset, date_string
from datetime import datetime
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('country_list', help='comma separated list of country codes to compare')
args = arg_parser.parse_args()
country_list = args.country_list.split(',')
print(country_list)

country_datasets = []
for geoid in country_list:
    country_datasets.append(load_dataset(geoid))

# Find the latest start date
latest_start = datetime(year=1900, month=1, day=1)
for cds in country_datasets:
    if cds.datapoints[0].date > latest_start:
        latest_start = cds.datapoints[0].date

start_indexes = {}
counts = []
for cds in country_datasets:
    start_index = 0
    while cds.datapoints[start_index].date < latest_start:
        start_index += 1
    start_indexes[cds.geoid] = start_index
    counts.append(len(cds.datapoints) - start_index)
rows_to_compare = min(counts)
file_name_base = 'compare_' + '_'.join(country_list)

# generate new cases per 1M pop chart
file_name = file_name_base + '_new_cases_per_1m.csv'
print('generating', file_name)
with open(file_name, 'wt') as file:
    file.write('date')
    for cds in country_datasets:
        file.write(',%s_new_cases' % cds.geoid)
    file.write('\n')
    for r in range(rows_to_compare):
        first = True
        for cds in country_datasets:
            idx = r + start_indexes[cds.geoid]
            if first:
                file.write('%s' % date_string(cds.datapoints[idx].date))
                first = False
            file.write(',%.3f' % cds.datapoints[idx].new_cases_per_1m)
        file.write('\n')

# generate new deaths per 1M pop chart
file_name = file_name_base + '_new_deaths_per_1m.csv'
print('generating', file_name)
with open(file_name, 'wt') as file:
    file.write('date')
    for cds in country_datasets:
        file.write(',%s_new_deaths' % cds.geoid)
    file.write('\n')
    for r in range(rows_to_compare):
        first = True
        for cds in country_datasets:
            idx = r + start_indexes[cds.geoid]
            if first:
                file.write('%s' % date_string(cds.datapoints[idx].date))
                first = False
            file.write(',%.3f' % cds.datapoints[idx].new_deaths_per_1m)
        file.write('\n')

# generate cummulative cases per 1M pop chart
file_name = file_name_base + '_cum_cases_per_1m.csv'
print('generating', file_name)
with open(file_name, 'wt') as file:
    file.write('date')
    for cds in country_datasets:
        file.write(',%s_cum_cases' % cds.geoid)
    file.write('\n')
    for r in range(rows_to_compare):
        first = True
        for cds in country_datasets:
            idx = r + start_indexes[cds.geoid]
            if first:
                file.write('%s' % date_string(cds.datapoints[idx].date))
                first = False
            file.write(',%.3f' % cds.datapoints[idx].cummulative_cases_per_1m)
        file.write('\n')

# generate cummulative deaths per 1M pop chart
file_name = file_name_base + '_cum_deaths_per_1m.csv'
print('generating', file_name)
with open(file_name, 'wt') as file:
    file.write('date')
    for cds in country_datasets:
        file.write(',%s_cum_deaths' % cds.geoid)
    file.write('\n')
    for r in range(rows_to_compare):
        first = True
        for cds in country_datasets:
            idx = r + start_indexes[cds.geoid]
            if first:
                file.write('%s' % date_string(cds.datapoints[idx].date))
                first = False
            file.write(',%.3f' % cds.datapoints[idx].cummulative_deaths_per_1m)
        file.write('\n')
