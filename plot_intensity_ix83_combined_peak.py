# -*- coding: utf-8 -*-
# Author: Kumiko Yoshioka-Kobayashi


import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import os
import numpy as np
import pandas as pd
import glob
from matplotlib.font_manager import FontProperties
import savitzky_golay as sg
from detecta import detect_peaks as dp
from datetime import datetime
from scipy import interpolate

plt.rcParams['font.family']= 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
df=pd.DataFrame(columns=[ 'Sample#','Sample_name'])
df_all=pd.DataFrame()
target='Gene'
dt=10
#colorlist = ["goldenrod","fuchsia", "darkturquoise"]
#colorlist = ["red", "g"]

#font properties of legend text
font_leg = FontProperties()
font_leg.set_family('sans-serif')
font_leg.set_name('Arial')
font_leg.set_style('italic')

def padconvolve(data,window):
        if window % 2 == 1:
                half_w=(int(window/2),int(window/2))
        else:
                half_w=(int(window/2),int(window/2-1))
        karnel = np.ones(window)/window
        convolved = np.convolve(np.pad(data, half_w, 'reflect'), karnel,'valid')
        return convolved

def peak_detection(signal):
    indexes = dp.detect_peaks(signal, mph=0.4, mpd=5)
    return indexes

def get_ref_index(df, x_label,y_label,sg_window,sg_order):
    data=df[y_label].values.tolist()
    data=np.array(data)

    data_sg = sg.savitzky_golay(data, window_size=sg_window, order=sg_order, deriv=0)
    #i_max=data_sg.max()
    #i_min=data_sg.min()
    #data_norm = (data_sg-i_min)/(i_max-i_min)
    ind = peak_detection(data_sg[1:-1])+1

    return ind[0]

def fig_plot(df, x_label,y_label, plot_y, ave_op, norm_op, agg_op, italic_op, ci,xmin,xmax, ymin, ymax):

    fig = plt.figure() #figsize=(11.69, 8.27) for A4

    #x_max=max(df[x_label].values.tolist())
    if norm_op==1:
        y_max=1
    else:
        y_max=max(df[y_label].values.tolist())
    ax =fig.add_subplot(1, 1, 1,aspect=xmax/y_max*0.5)
    fig.subplots_adjust(left=0.2)
    nu = df[target].nunique()

    if ave_op==1:
        if agg_op==1:
            sns.lineplot(data=df, x=x_label, y=plot_y, alpha=0.7, ax=ax,
                #ci=ci, linewidth = 2)
                ci=ci,linewidth = 2)
                #confidential interval/ci=68% means +/- 1 S.E.M.
        else:
            sns.lineplot(data=df, x=x_label, y=plot_y, alpha=0.1, ax=ax, linewidth = 1,
                #units='Sample_ID',estimator=None,legend=False)
                units=target,estimator=None,legend=False)
            sns.lineplot(data=df, x=x_label, y=plot_y, alpha=0.9,ax=ax,
                #ci=0, linewidth = 3)
                ci=0, linewidth = 3)

    else:
        sns.lineplot(data=df, x=x_label, y = plot_y, hue = target, alpha=0.75, ax=ax,
            units='Sample_ID', estimator=None,  palette = colorlist[0:nu])
            #units='Sample_ID', estimator=None)

    if norm_op==1:
        plt.ylabel('Lumimnescence (a.u.)',fontsize=18)
    else:
        plt.ylabel('Lumimnescence (a.u.)',fontsize=18)
    #plt.ylabel('Intensity (a.u.)',fontsize=18)
    plt.xlabel('Time (h)', fontsize=18)

    xmin_tmp, xmax_tmp =plt. xlim()
    if xmin is not None and xmax is not None:
        plt.xlim((xmin ,xmax))
    elif xmin is not None:
        plt.xlim((xmin ,xmax_tmp))
    elif xmax is not None:
        plt.xlim((xmin_tmp ,xmax))

    ymin_tmp, ymax_tmp =plt. ylim()
    if ymin is not None and ymax is not None:
        plt.ylim((ymin ,ymax))
    elif ymin is not None:
        plt.ylim((ymin ,ymax_tmp))
    elif ymax is not None:
        plt.ylim((ymin_tmp ,ymax))

    ax.tick_params(labelsize=15, length=1)

    return fig

def do_plot_all(df, base, x_label,y_label, path, plot_y, ave_op, norm_op, agg_op, italic_op,sample_name):

    fig = fig_plot(df, x_label,y_label, plot_y, ave_op, norm_op, agg_op, italic_op, 68, xmin,xmax,ymin, ymax)

    if plot_y==y_label:
        output_path = path + base + '_'+sample_name+'_all_'+'Raw_subbg'
    else:
        output_path = path + base + '_'+sample_name+'_all_' + plot_y

    if ave_op==1:
        output_path = output_path + '_averaged'
    if agg_op==1:
        output_path = output_path + '_aggregated'


    plt.savefig(output_path+'.pdf', transparent=True)

    plt.close()




def do_plot(df_tmp ,base, x_label,y_label, sma_window, trend_window,
        sg_window, sg_order, path, plot_y, italic_op,
        xmin, xmax, ymin, ymax, x_ref):

    print(name)

    x=np.array(df_tmp[x_label].values.tolist())
    data=np.array(df_tmp[y_label].values.tolist())
    #dx=1.65729
    #dx=0.61

    #data_basesub = data - np.amin(data)


    data_sg = sg.savitzky_golay(data, window_size=sg_window, order=sg_order, deriv=0)
    #data_norm_sg = sg.savitzky_golay(data_norm, window_size=sg_window, order=sg_order, deriv=0)
    i_max=data_sg.max()
    i_min=data_sg.min()
    data_norm = (data_sg-i_min)/(i_max-i_min)

    max_index = np.argmax(data_norm)
    if max_index<5:
        ref_ind=0
    else:
        ref_ind=get_ref_index(df_tmp,x_label,y_label,sg_window,sg_order)
    x_sub=x-x[ref_ind]

    data_sub=data[x_sub>=0]
    x_sub=x_sub[x_sub>=0]

    f = interpolate.interp1d(x_sub, data_sub, kind='cubic',fill_value='extrapolate')

    x_norm = x_ref[x_ref<=max(x_sub)]
    data = f(x_ref)[x_ref<=max(x_sub)]


    df_tmp=pd.DataFrame({ x_label : x_norm,y_label: data})

    df_tmp.insert(1,'Time (h)', df_tmp[x_label]*dt/60)


    #df_tmp.insert(2,y_label, data)
    df_tmp.insert(1, 'Sample#', name[name.find('sample')+6])

    ch_name=base[base.find('_ch#')+6:]
    #ch=int(name[name.find('ch#')+3])
    df_tmp.insert(2, target, ch_name)
    df_tmp.insert(3, 'Sample_ID', name[0:name.find('sample')+8])



    trend_karnel = np.ones(trend_window)/trend_window
    data_pad = np.pad(data, (int((trend_window-1)/2),int((trend_window-1)/2)), 'reflect')
    trend = np.convolve(data_pad, trend_karnel, 'valid')


    data_detrended = data - trend
    data_norm_ma = data/trend

    data_sg = sg.savitzky_golay(data, window_size=sg_window, order=sg_order, deriv=0)
    #data_norm_sg = sg.savitzky_golay(data_norm, window_size=sg_window, order=sg_order, deriv=0)
    i_max=data_sg.max()
    i_min=data_sg.min()
    data_norm = (data_sg-i_min)/(i_max-i_min)




    data_basesub_sg = data_sg - np.amin(data)
    data_norm_sg = sg.savitzky_golay(data_norm, window_size=sg_window, order=sg_order, deriv=0)
    df_tmp.insert(5,'Normalized',data_norm)

    df_tmp.insert(6,'Data_det',data_detrended)
    df_tmp.insert(7,'Norm_MA',data_norm_ma)
    df_tmp.insert(8,'Data_sg',data_sg)
    df_tmp.insert(9,'Data_basesub_sg',data_basesub_sg)
    #df=pd.concat([df, df_tmp])

    fig = fig_plot(df_tmp, 'Time (h)',y_label, plot_y, ave_op, norm_op, 0, italic_op, 68, xmin, xmax, ymin, ymax)



    if plot_y==y_label:
        plt.savefig(path + base +'_Raw'+'.pdf', transparent=True)
    else:
        plt.savefig(path + base + '_' + plot_y+'.pdf', transparent=True)


    plt.close()


    return df_tmp




if __name__ == '__main__':
    print("Running!")

    parser = argparse.ArgumentParser(description=u'') # parserを作る
    parser.add_argument('input', type=str, help=u"Folder where you have csv files. If it is the current directory, type cd. ", nargs='+')
    parser.add_argument("--ave", type=int, help=u"Options for averaging ")
    parser.add_argument("--agg", type=int, help=u"Options for data aggregation ")
    parser.add_argument("--bgsub", type=int, help=u"Options for bg subtraction ")
    parser.add_argument("--norm", type=int, help=u"Options for normalization ")
    parser.add_argument("--trend-window", type=int, help=u"Window size to extract trend (default: 71) ", default=71)
    parser.add_argument("--sma-window", type=int, help=u"Window size of moving average (default: 10) ", default=10)
    parser.add_argument("--sg", type=int, help=u"Options for Savitzky-Golay filtering ")
    parser.add_argument("--sg-window", type=int, help=u"Window size of Savitzky-Golay filter (default: 23) ", default=23)
    parser.add_argument("--sg-order", type=int, help=u"Order of polinominal functions Savitzky-Golay filter (default: 4) ", default=4)
    parser.add_argument("--xmin", type=int, help=u"Minimum of x-axis range")
    parser.add_argument("--xmax", type=int, help=u"Maximum of x-axis range")
    parser.add_argument("--ymin", type=int, help=u"Minimum of y-axis range")
    parser.add_argument("--ymax", type=int, help=u"Maximum of y-axis range")
    parser.add_argument("--italic", type=int, help=u"Options for using italic font in figure legends ")

    args = parser.parse_args()


    sma_window, trend_window  = args.sma_window, args.trend_window
    sg_window, sg_order = args.sg_window, args.sg_order

    ave_op, agg_op, bgsub_op, norm_op, sg_op, italic_op = args.ave, args.agg, args.bgsub, args.norm, args.sg, args.italic

    xmin, xmax, ymin, ymax = args.xmin, args.xmax, args.ymin, args.ymax

    if norm_op==None:
        if bgsub_op==1:
            plot_y='Data_basesub_sg'
        elif sg_op==1:
            plot_y='Data_sg'

        else:
            plot_y=None

    elif norm_op==1:
        plot_y='Normalized'

    if args.input:

        if args.input[0]=='cd':
            folder = os.getcwd()
        else:
            #args.input[0].endswith('/')
            folder = args.input[0]


        #if args.input[0]=='cd' or args.input[0].endswith('/'):
        file_list=glob.glob(folder+'/*.csv')
        file_list_data=[]
        for file in file_list:
            name = os.path.basename(file)
            base, ext = os.path.splitext(name)

            df = pd.read_csv(file)
            if len(df.columns)==2:
                file_list_data.append(file)

        sample_number=[]
        max_x=[]

        for file in file_list_data:
            name = os.path.basename(file)
            base, ext = os.path.splitext(name)

            df = pd.read_csv(file)
            if len(df.columns)==2:

                sample_number.append(base[base.find('sample')+7])

                x_label = df.columns.values[0]

                max_x.append(max(np.array(df[x_label].values.tolist())))

        n_sample=max(sample_number)

        length_max=max(max_x)

        max_ind = max_x.index(length_max)

        df = pd.read_csv(file_list_data[max_ind])
        x_ref=np.array(df[x_label].values.tolist())
        file_ref=glob.glob(folder+'/*sample*.csv')

        #name = os.path.basename(file_ref[0])
        #base, ext = os.path.splitext(name)



        #for file in file_ref:
        #    name = os.path.basename(file)
        #    base, ext = os.path.splitext(name)
        #    sample_number.append(base[base.find('sample')+7])



        path = folder + '/'
        folder=os.path.dirname(folder)
        subfolder=os.path.basename(os.path.dirname(path))

        csv_count = 0

        df=pd.DataFrame()



        #ref_ind=get_ref_index(file_ref,sg_window,sg_order)
        for i in range(len(file_ref)):
            for file in file_list_data:
                name = os.path.basename(file)
                base, ext = os.path.splitext(name)

                df_tmp  = pd.read_csv(file)

                if len(df_tmp.columns)==2:

                    if (int(base[base.find('sample')+6:base.find('sample')+8])) is i+1:

                        print('Processing...')
                        x_label = df_tmp.columns.values[0]
                        y_label = df_tmp.columns.values[1]

                        if plot_y == None:
                            plot_y = y_label

                        df_tmp  = do_plot(df_tmp, base,x_label, y_label, sma_window,  trend_window,
                            sg_window, sg_order, path, plot_y, italic_op,
                            xmin, xmax, ymin, ymax , x_ref)
                        df = pd.concat([df, df_tmp])
                        csv_count+=1

            if csv_count == 0:
                print ('No csv files (with 2-columns) found.')
            #else:

                #df = df.sort_values('Channel#')

                #do_plot_all(df, folder,  x_label,y_label, path, plot_y, ave_op, norm_op, agg_op, italic_op,'sample'+(str(i+1)))


            df_all = pd.concat([df_all, df])
            df = pd.DataFrame()


        #df_all=df_all.sort_values('Channel#')
        #df_ext=df_all[df_all['Distance_normalized'] >= 0]
        #df_ext=df_ext[df_ext['Distance_normalized'] <800]

        do_plot_all(df_all, folder, 'Time (h)', y_label, path, plot_y, ave_op, norm_op, agg_op, italic_op,subfolder)
        df_all.to_csv(path+'dataset_'+datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss')+'.csv', index=False)
    exit()
