import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import scipy as sp
import math
import os
import numpy as np
import pandas as pd
colorlist = ["goldenrod","fuchsia", "darkturquoise"]
colorlist1 = ['white']
colorlist2 = ['black']
colorlist3 = [ 'fuchsia','darkorange','g']
colorlist4 = [ 'b','fuchsia']
hue_order = ['-MG', '+MG']
hue='sample_name'
def do_plot(files):

    plt.rcParams['font.family']= 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']

    name= os.path.basename(files)
    base, ext = os.path.splitext(name)
    df  = pd.read_csv(files)
    #df_avg=df.groupby(['sample_name','#th_seg']).mean()
    df = df.round({'#th_seg':0})
    df.insert(4,'Period',df['Time']*60)
    fig = plt.figure(figsize=(7,4))


    fig.subplots_adjust(left=0.2, bottom=0.2)
    ax = plt.axes()




    #df2=df_avg.reset_index()


    #sns.boxplot(data=df,x='nth_peak',y='value_h',hue='sample_name', palette='Set2',
    #fliersize=0,ax=ax)
    #sns.stripplot(data=df,x='nth_peak',y='value_h',hue='sample_name', color='black',
    #    alpha=.75, ax=ax)
    sns.set(style = 'white')
    df_stat = df.groupby(['#th_seg',hue]).agg([np.mean, np.std])
    df_stat_1= df_stat['Period']
    per = df_stat_1.reset_index(level=[hue,'#th_seg'])

    #per.plot()
    #per = df_stat_1[['Period',hue]]
    #print(per)
    #print(per.columns)
    #per.plot(kind = 'bar', y = 'mean', legend = False, alpha=1,
    #        yerr = 'std', ax=ax, error_kw=dict(lw=1, capsize=5, capthick=1),zorder=20, ecolor='r')

    sns.stripplot(data=df,x='#th_seg',y='Period',dodge=True,hue=hue, order=None, 
                 #palette = colorlist1,alpha=0.75, edgecolor='black', linewidth=1)
                 alpha=0.75,  linewidth=1,edgecolor=None,palette = colorlist4,hue_order=hue_order)
    ax.get_legend().remove()
    ax2 = ax.twinx()
    #sns.barplot(data=df,x='#th_seg',y='Period',dodge=True, hue=hue, ci='sd',alpha=0,ax=ax2,
    sns.barplot(data=df,x='#th_seg',y='Period',dodge=True, hue=hue, ci='sd',alpha=0,ax=ax2,hue_order=hue_order,
                 capsize= 0.25,  errwidth= 1,zorder=20,errcolor= 'black')#,
                #errcolor= 'r',palette = colorlist1)
    #sns.boxplot(data=df,x='#th_seg',y='Period',hue=hue,

    #            meanline=True,meanprops={'color': 'r', 'ls': '-', 'lw': 2},
                #meanline=True, meanprops={'ls': '-', 'lw': 2},
    #            showmeans=True,
    #            medianprops={'visible': False},whiskerprops={'visible': False},
    #            zorder=10,showfliers=False,showbox=False,showcaps=False,fliersize=0,ax=ax)
    #sns.pointplot(x = '#th_seg',y='Period', hue = hue, data = df, kind = 'point',
    sns.pointplot(x = '#th_seg',y='Period', hue = hue, data = df, kind = 'point',hue_order=hue_order,
        #dodge=0.55,ax=ax2, s=5,markers='_', join=False,ci=None,legend=None,palette = colorlist2)
        dodge=0.4,ax=ax2, s=5,markers='_', join=False,ci=None,legend=None,palette = colorlist2)
    plt.setp(ax2.collections, sizes=[150])
    #sns.pointplot(data=df,x='#th_seg',y='Period',linestyle=None,
    #    ax=ax, linewidth=0,join=None, markers = '_',capsize=.3,zorder=20,errwidth=0)

    #nth= df_stat['#th_seg']
    ax.set_xticklabels(ax.get_xticklabels(),rotation = 0)
# checking for results


    #sns.barplot(data=df,x='#th_seg',y='Period',dodge=True,hue='Condition', ci='sd',
    #            palette = colorlist1, capsize= 0.25, errcolor= 'r', errwidth= 1,zorder=10)

    handles, labels = ax.get_legend_handles_labels()

# When creating the legend, only use the first two elements
# to effectively remove the last two.

    l = plt.legend(handles[0:3], labels[0:3], loc=2, borderaxespad=0.2)

    plt.yticks(fontsize=18)
    plt.xticks(fontsize=18)

    ax.tick_params('x',length=0)
    ax2.set_ylim(0, 500)
    ax2.set_xlim(1, 7)
    ax.set_xlim(-0.5, 6.5)
    ax2.set_yticks([])
    ax2.set_ylabel('')
    ax.set_ylim(0, 500)

    ax.set_ylabel('Period (min)',fontsize=18)
    ax.set_xlabel('#th peak', fontsize=18)

    plt.savefig(base+'.pdf')




if __name__ == '__main__':

        parser = argparse.ArgumentParser(description=u'') # parserを作る
        parser.add_argument('input', type=str, help=u"", nargs='+')
        #print (parser.parse_args())
        args = parser.parse_args()

        # print('AAAAAAAAAAAAAA\n')
        # print(args)
        # print(args.input)
        # print('AAAAAAAAAAAAAA\n')

        print(args.input)

        if args.input:
                for files in args.input:

                    do_plot(files)

        exit()
