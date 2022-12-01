# -*- coding: utf-8 -*-
# Author: Kumiko Yoshioka-Kobayashi

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import savitzky_golay as sg
import scipy as sp
from matplotlib.ticker import ScalarFormatter

plt.rcParams['font.family']= 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

def get_xmin(series_time, time_start):
    for i in range(series_time.size):
        if series_time[i] > time_start:
            return i
    return 0


def get_xmax(series_time, time_end):
    for i in range(series_time.size):
        if series_time[i] > time_end:
            return i - 1
    return series_time.size - 1


def get_cut_series(series, xmin, xmax):
    series_out = sp.zeros(xmax - xmin)
    for i in range(series_out.size):
        series_out[i] = series[i + xmin]
    return series_out


def get_record_time(value_date, value_time):
    meta_month = (str(0) + str(value_date.month)) if value_date.month < 10 else str(value_date.month)
    meta_day = (str(0) + str(value_date.day)) if value_date.month < 10 else str(value_date.day)
    meta_hour = (str(0) + str(value_time.hour)) if value_time.hour < 10 else str(value_time.hour)
    meta_minute = (str(0) + str(value_time.minute)) if value_time.minute < 10 else str(value_time.minute)
    return str(value_date.year) + "/" + meta_month + "/" + meta_day + " " + meta_hour + ":" + meta_minute


def do_analysis(csv, interval, trend_window, sg_window, sg_order, is_plot, output_dir):
    col_names = ['c{0:02d}'.format(i) for i in range(53)]

    temp = pd.read_csv(csv, names=col_names, header=None, engine='python', skiprows=10, nrows=1)
    sample_name = temp.dropna(how='all', axis=1)
    sample_name = sample_name.values.tolist()[0]

    temp = pd.read_csv(csv, names=col_names, header=None, engine='python', skiprows=12)

    sub_nrows = 4
    sub_ncols = 6
    cmap1 = plt.get_cmap("tab20")
    cmap2 = plt.get_cmap("tab20b")
    t_bg = temp['c' + str(1).zfill(2)].values
    bg = temp['c' + str(2).zfill(2)].values
    fig_all = plt.figure(figsize=(11.69, 8.27))
    fig_indivi = plt.figure()

    if np.remainder(trend_window, 2) == 0:
        trend_window = trend_window + 1

    ax = fig_all.add_subplot(1, 1, 1,xlabel='Time (h)')


    for n in range(2, len(sample_name) + 1):

        t = temp['c' + str(n * 2 - 1).zfill(2)].values
        data = temp['c' + str(n * 2).zfill(2)].values

        print("Well " + sample_name[n - 1] + ": data set was detected")

        data = data - bg
        trend_karnel = np.ones(trend_window) / trend_window
        data_pad = np.pad(data, (int((trend_window - 1) / 2), int((trend_window - 1) / 2)), 'reflect')
        trend = np.convolve(data_pad, trend_karnel, 'valid')


        output_path_raw = output_dir + '/' + csv.replace('.csv', '_' + sample_name[n - 1] + '_bgsub' + '.csv')

        f = open(output_path_raw, 'w')

        f.write('Time (h)' + ',' + 'Counts(c.p.s)' + '\n')

        for i in range(len(data) - 1):
            f.write(str(t[i]) + "," + str(data[i]) + '\n')
        f.close()

        ax_indivi=fig_indivi.add_subplot(sub_nrows, sub_ncols, n-1)
        ax_indivi.plot(t, data, linewidth=0.5, linestyle="-")
        ax_indivi.tick_params(labelsize=5, length=1)
        ax_indivi.set_title(sample_name[n-1], fontsize=3, loc='center')




        if is_plot:

            if n > 1:

                if n < 22:
                    ax.plot(t, data, linewidth=1, linestyle="-")
                else:
                    ax.plot(t, data, linewidth=1, linestyle='dashed')


    if is_plot:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.yaxis.offsetText.set_fontsize(5)
        ax.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
        ax.legend(sample_name[1:len(sample_name)])
        ax.tick_params(labelsize=8, length=1)
        plt.tight_layout()
        #plt.xlabel('Time (h)', fontsize=8, fontname='Arial')
        ax.set_ylabel('Photon counts (c.p.s.)', fontsize=8, fontname='Arial')

        output_path_fig = output_dir + '/' + csv.replace('.csv', '.pdf')
        output_path_fig_indivi = output_dir + '/' + csv.replace('.csv', '_indivi'  + '.pdf')

        fig_all.savefig(output_path_fig, format='pdf')
        fig_indivi.savefig(output_path_fig_indivi, format='pdf')
        #plt.savefig(output_path_fig.replace(".pdf", "") + ".png", format='png')
        #plt.savefig(output_path_fig.replace(".pdf", "") + ".svg", format='svg')
        plt.close()


if __name__ == '__main__':
    print("Running!")
    parser = argparse.ArgumentParser(description=u'ATTO -- a tool for analysis of ATTO PMT data')  # parserを作る
    parser.add_argument('input', type=str, help=u"", nargs='+')
    # parser.add_argument("--header", type=str, help=u"Header for output", nargs='+')
    parser.add_argument("--output-dir", type=str, help=u"Directory for output", nargs='+')
    # parser.add_argument("--input-header", type=str, help=u"Header for filtering input files", nargs='+')
    parser.add_argument("--interval", type=int, help=u"Intervals between data-points (default: 5)", nargs=1)
    # parser.add_argument("--bin-size", type=int, help=u"Bin size for phase distribution (default: 24)", nargs=1)

    parser.add_argument("--trend-window", type=int, help=u"Window size to extract trend (default: 36) ", nargs=1)
    parser.add_argument("--sg-window", type=int, help=u"Window size of Savitzky-Golay filter (default: 13) ", nargs=1)
    parser.add_argument("--sg-order", type=int,
                        help=u"Order of polinominal functions Savitzky-Golay filter (default: 4) ", nargs=1)
    parser.add_argument("--plot", type=int, help=u"Plot figures of peak positions (default: False)", nargs=1)
    parser.add_argument("--p-max", type=int, help=u"Upper limit of y axis range ", nargs=1)
    parser.add_argument("--p-min", type=int, help=u"Lower limit of y axis range ", nargs=1)

    parser.add_argument("--cos-threshold", type=float, help=u"Cos threshold for peak detection (default: 0.5)", nargs=1)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 170411b')  # version

    args = parser.parse_args()

    if args.output_dir:
        output_dir = args.output_dir[0]
        if os.path.isdir(output_dir):
            print(get_class_name() + ": Now you may overwrite results...")
        else:
            os.mkdir(output_dir)
    else:
        output_dir = "./"

    if args.interval:
        interval = args.interval[0]
    else:
        interval = 5

    if args.trend_window:
        trend_window = args.trend_window[0]
    else:
        trend_window = 70
    if args.sg_window:
        sg_window = args.sg_window[0]
    else:
        sg_window = 13
    if args.sg_order:
        sg_order = args.sg_order[0]
    else:
        sg_order = 4

    if args.plot:
        is_plot = True
    else:
        is_plot = False

    if args.p_max:
        p_max = args.p_max[0]
    else:
        p_max = None

    if args.p_min:
        p_min = args.p_min[0]
    else:
        p_min = None

    if args.cos_threshold:
        cos_threshold = args.cos_threshold[0]
    else:
        cos_threshold = 0.5
    interval_dataset = []

    if args.input:
        for csv in args.input:
            do_analysis(csv, interval, trend_window, sg_window, sg_order, is_plot, output_dir)
    exit()
