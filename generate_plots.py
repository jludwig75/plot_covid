#!/usr/bin/env python3
import os

for file_name in os.listdir('outputs'):
    if file_name.endswith('.csv'):
        file_name = os.path.join('outputs', file_name)
        print(file_name)
        os.system('./plot_csv.py %s' % file_name)
