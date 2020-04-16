#!/usr/bin/env python3
import os
import PyGnuplot as gp
import argparse

COLOR_PALETTE = [
                    '#FF0000',
                    '#00FFFF',
                    '#228b22',
                    '#984EA3',
                    '#FF7F00',
                    '#964B00',
                    '#000000',
                    '#FFEC8B',
                    '#C8B18B',
                    '#8A8489'
                ]

def plot_csv_file(csv_file_name, width, height, max_y, log_scale):
    if not os.path.exists(csv_file_name):
        print('skiping %s because it does not exist' % csv_file_name)
        return
    output_file_name = os.path.join('plots', os.path.basename(csv_file_name))
    last_dot = output_file_name.rfind('.')
    output_file_name = output_file_name[:last_dot] + '.png'
    print('  plotting %s as %s' % (csv_file_name, output_file_name))
    with open(csv_file_name, 'r') as csv_file:
        first_line = csv_file.readline()[:-1]
    fields = first_line.split(',')
    assert 'date' in fields
    assert fields.index('date') == 0
    gp.c('set xdata time')
    gp.c('set timefmt "%Y-%m-%d"')
    gp.c('set format x "%Y-%m-%d"')
    gp.c('set term png size %u,%u' % (width, height))
    gp.c('set output "%s"' % output_file_name)
    gp.c('set datafile separator ","')
    gp.c('set title "%s"' % csv_file_name[:-4].replace('_', ' '))
    if log_scale:
        gp.c('set logscale y 10')
    if max_y != 0:
        gp.c('set yr [0:%u]' % max_y)
    plot_cmd = 'plot '
    first_series = False
    for i in range(1, len(fields)):
        if not first_series:
            first_series = True
        else:
            plot_cmd += ', '
        plot_cmd += '"%s" using 1:%u with lines title "%s" lw 2 lt rgb "%s"' % (csv_file_name, i + 1, fields[i].replace(r'_', r'\\_'), COLOR_PALETTE[i % len(COLOR_PALETTE)])
    gp.c(plot_cmd)

parser = argparse.ArgumentParser(description='Plot the fields in a CSV file to a PNG file')
parser.add_argument('-W', '--width', type=int, default=2400, help='width in pixels of the output image')
parser.add_argument('-H', '--height', type=int, default=1800, help='height in pixels of the output image')
parser.add_argument('-y', '--max-y', type=int, default=0, help='max y range value')
parser.add_argument('-l', '--log-y-scale', action='store_true', default=False, help='use log-scale for y axis')
parser.add_argument('csv_file', type=str, help='input CSV file')
args = parser.parse_args()

plot_csv_file(args.csv_file, args.width, args.height, args.max_y, args.log_y_scale)
