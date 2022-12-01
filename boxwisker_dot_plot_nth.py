import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import scipy as sp
import math
import os
import numpy as np
import pandas as pd

def do_plot(files):

    plt.rcParams['font.family']= 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']

    name= os.path.basename(files)
    base, ext = os.path.splitext(name)
    df  = pd.read_csv(files)
    #df_avg=df.groupby(['sample_name','#th_seg']).mean()
    df = df.round({'#th_seg':0})

    fig = plt.figure()

    fig.subplots_adjust(left=0.2, bottom=0.2)
    ax = plt.axes()
    df.insert(4,'value_h',df['value']*60)

    #df2=df_avg.reset_index()


    sns.boxplot(data=df,x='nth_peak',y='value_h',hue='sample_name', palette='Set2',
        fliersize=0,ax=ax)
    sns.stripplot(data=df,x='nth_peak',y='value_h',hue='sample_name', color='black',
        alpha=.75, ax=ax)

    handles, labels = ax.get_legend_handles_labels()

# When creating the legend, only use the first two elements
# to effectively remove the last two.

    l = plt.legend(handles[0:1], labels[0:1], loc=2, borderaxespad=0.2)

    plt.yticks(fontsize=18)
    plt.xticks(fontsize=18)

    ax.tick_params('x',length=0)

    plt.ylim((0, 500))

    plt.ylabel('Period (min)',fontsize=18)
    plt.xlabel('#th peak', fontsize=18)

    plt.savefig(base+'.pdf')




if __name__ == '__main__':

        parser = argparse.ArgumentParser(description=u'') # parserを作る
        parser.add_argument('input', type=str, help=u"", nargs='+')
        #print (parser.parse_args())
        args = parser.parse_args()



        if args.input:
                for files in args.input:

                    do_plot(files)

        exit()
