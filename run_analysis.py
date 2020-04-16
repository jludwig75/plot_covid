#!/usr/bin/env python3
import os

PLOT_TYPES = ['cum', 'new']
DATA_TYPES = ['cases', 'deaths']
COUNT_TYPES = ['total', 'per_1m']

for plot_type in PLOT_TYPES:
    for data_type in DATA_TYPES:
        for count_type in COUNT_TYPES:
            sort_tag = 'top_%s_%s_%s' % (plot_type, data_type, count_type)
            print(sort_tag)
            os.system('./compare_countries.py %s' % sort_tag)

# plot countries of particular interest
os.system('./compare_countries.py US,IT,ES,CA,AU,AT,FR,SE,UK,DE')
