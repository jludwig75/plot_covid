#!/usr/bin/env python3
from covid.dataset import load_dataset, date_string, CountryDataset
from datetime import datetime
import argparse
import os

def get_country_csv_file_names():
    country_list = []
    for file_name in os.listdir('country_data'):
        if file_name.lower().endswith('.csv') and not file_name.lower().startswith('jpg'):
            country_list.append(file_name[:-len('.csv')].upper())
    country_list.sort()
    return country_list

def find_top_case_counts(country_list, cmp_func, top_count=10):
    # print(cmp_func)
    counts = []
    for geoid in country_list:
        cds = load_dataset(geoid)
        # print(geoid)
        counts.append((cmp_func(cds), geoid))
    counts.sort(key=lambda x: -x[0])
    # print(counts)
    counts = counts[:top_count]
    # print(counts)
    return [x[1] for x in counts]

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('country_list', help='comma separated list of country codes to compare')
arg_parser.add_argument('-l', '--label', type=str, default=None, help='label for file name')
args = arg_parser.parse_args()
cl = args.country_list.lower()
if cl == 'all':
    country_list = get_country_csv_file_names()
elif cl.startswith('top'):
    country_list = get_country_csv_file_names()
    if cl == 'top_cum_cases_total':
        country_list = find_top_case_counts(country_list, CountryDataset.get_max_case_count)
    elif cl == 'top_new_cases_total':
        country_list = find_top_case_counts(country_list, CountryDataset.get_max_new_case_count)
    elif cl == 'top_cum_deaths_total':
        country_list = find_top_case_counts(country_list, CountryDataset.get_max_death_count)
    elif cl == 'top_new_deaths_total':
        country_list = find_top_case_counts(country_list, CountryDataset.get_max_new_death_count)
    elif cl == 'top_cum_cases_per_1m':
        country_list = find_top_case_counts(country_list, CountryDataset.get_max_case_count_per_1m)
    elif cl == 'top_new_cases_per_1m':
        country_list = find_top_case_counts(country_list, CountryDataset.get_max_new_case_count_per_1m)
    elif cl == 'top_cum_deaths_per_1m':
        country_list = find_top_case_counts(country_list, CountryDataset.get_max_death_count_per_1m)
    elif cl == 'top_new_deaths_per_1m':
        country_list = find_top_case_counts(country_list, CountryDataset.get_max_new_death_count_per_1m)
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

if args.label != None:
    file_name_base = 'outputs/compare_' + args.label
elif cl.lower() == 'all':
    file_name_base = 'outputs/compare_all'
elif cl.startswith('top'):
    file_name_base = 'outputs/compare_' + cl
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
