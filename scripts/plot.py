#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os

def draw_figure5(input_dir, input_file):

    output_dir = input_dir
    input_path = os.path.join(input_dir, input_file)

    plt.rc('text')
    matplotlib.rcParams['hatch.linewidth'] = 2.0
    df = pd.read_csv(input_path, delimiter='\t', index_col='Target')

    dafl = list(df['DAFL'])
    afl = list(df['AFL'])
    aflgo = list(df['AFLGo'])
    windranger = list(df['WindRanger'])

    targets = list(df.index)

    tools = {
        'AFL': afl,
        'AFLGo': aflgo,
        'WindRanger': windranger,
        'DAFL': dafl,
    }

    color = {
        'DAFL': 'orangered',
        'AFL': 'dodgerblue',
        'AFLGo': 'forestgreen',
        'WindRanger': 'darkorange',
    }

    ecolor = {
        'DAFL': 'whitesmoke',
        'AFL': 'whitesmoke',
        'AFLGo': 'whitesmoke',
        'WindRanger': 'whitesmoke'
    }

    alpha = {
        'DAFL': 1,
        'AFL': 0.5,
        'AFLGo': 0.5,
        'WindRanger': 0.5

    }

    hatch = {
        'DAFL': None,
        'AFL': None,
        'AFLGo': None,
        'WindRanger': None,
    }

    bar_width = 0.45
    tic_distance = 3
    tickfontsize = 23

    fig, ax = plt.subplots(figsize= (30,13))

    plt.xticks([ x * tic_distance + 0.4  for x in range(0, len(targets))],
               fontsize=tickfontsize,
               rotation=30, ha='center', va='top')
    ax.xaxis.set_tick_params(width=2, size=5)
    ax.yaxis.set_tick_params(width=2, size=5)
    plt.yticks(fontsize=tickfontsize)

    ax.set_xticklabels(targets)
    xidx = 0
    j = 0

    # a ghost bar to set the lowerbound of logscale
    plt.bar(0, 2, bar_width, color="white",  zorder=2, label='_nolegend_', log=True, alpha=0,)

    N = len(targets)
    for target in targets:
        i = 0
        to_x_list=[]
        for tool in tools:
            if "N.A." in str(tools[tool][j]):
                tte = 86400
            else:
                tte = int(tools[tool][j])

            x_cord = xidx + (i - 1) * (bar_width+0.084)

            plt.bar(x_cord,
                    tte,
                    bar_width,
                    color=color[tool],
                    hatch=hatch[tool],
                    # edgecolor=ecolor[tool],
                    zorder=2,
                    label=tool,
                    log=True,
                    alpha=alpha[tool]
                    )


            if tte == 86400:
                to_x_list.append(x_cord)

            i += 1

        if len(to_x_list) > 0:
            ax.text(sum(to_x_list)/len(to_x_list), 110000, "T.O.",
                    ha='center', va='bottom', fontsize=20, color='black')
        j += 1
        xidx += tic_distance
    plt.ylabel("TTE", size=20)

    # Note:
    # "ncol=5" : makes tools to be in one row, becase there are 5 of them.
    # "bbox_to_anchor" : makes the legend box to stay out of the plot.
    plt.legend(( 'AFL', 'AFLGo', 'WindRanger', 'DAFL' ),
               fontsize=tickfontsize-2, ncol=5, bbox_to_anchor=(0.70,1.12))

    plt.margins(0.01)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir,'figure5.pdf'))


def draw_figure7(input_dir, input_file):

    output_dir = input_dir
    input_path = os.path.join(input_dir, input_file)

    plt.rc('text')
    matplotlib.rcParams['hatch.linewidth'] = 2.0
    df = pd.read_csv(input_path, delimiter='\t',  index_col='Target')

    dafl = [str(x) for x in list(df['DAFL'])]
    dafl_naive = [str(x) for x in list(df['DAFL_naive'])]
    afl = list(df['AFL'])

    targets = list(df.index)

    tools = {
        'AFL' : afl,
        'DAFL_naive': dafl_naive,
        'DAFL': dafl,
    }



    color = {
        'DAFL': 'orangered',
        'DAFL_naive': 'forestgreen',
        'AFL': 'dodgerblue',
    }

    ecolor = {
        'DAFL_naive': 'whitesmoke',
        'DAFL': 'whitesmoke',
        'AFL': 'whitesmoke'
    }

    alpha = {
        'DAFL_naive': 0.5,
        'DAFL': 1,
        'AFL': 0.5
    }

    hatch = {
        'DAFL_naive': None,
        'DAFL': None,
        'AFL': None,
    }

    bar_width = 0.3
    tic_distance = 1.5
    tickfontsize = 12


    fig, ax = plt.subplots(figsize= (15,5.5))

    plt.xticks([ x * tic_distance   for x in range(0, len(targets))],
                fontsize=tickfontsize,
                rotation=30, ha='center', va='top')
    ax.xaxis.set_tick_params(width=2, size=5)
    plt.yticks(fontsize=tickfontsize)

    ax.set_xticklabels(targets)
    xidx = 0

    j = 0
    # a ghost bar to set the lowerbound of logscale
    plt.bar(0, 2, bar_width, color="white",  zorder=2, label='_nolegend_', log=True, alpha=0,)

    N = len(targets)


    for target in targets:
        i = 0
        to_x_list=[]
        
        for tool in tools:
            if "N.A." in str(tools[tool][j]):
                tte = 86400
            else:
                tte = int(tools[tool][j])

            x_cord = xidx + (i - 1) * (bar_width+0.05)
            plt.bar(x_cord,
                    tte,
                    bar_width,
                    color=color[tool],
                    hatch=None,
                    # edgecolor=ecolor[tool],
                    zorder=2,
                    label=tool,
                    log=True,
                    alpha=alpha[tool]
                    )
            
            if tte == 86400:
                to_x_list.append(x_cord)

            i += 1


        if len(to_x_list) > 0:
            ax.text(sum(to_x_list)/len(to_x_list), 110000, "T.O.",
                    ha='center', va='bottom', fontsize=13, color='black')
        j += 1
        xidx += tic_distance
    plt.ylabel("TTE", size=15)

    # Note:
    # The order of legend is messy in order to enhance the presentation
    # "bbox_to_anchor" : makes the legend box to stay out of the plot.
    plt.legend(( 'AFL', 'DAFL_Naive', 'DAFL'),
               fontsize=tickfontsize, ncol=3, bbox_to_anchor=(0.6,1.2))

    plt.margins(0.01)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir,'figure7.pdf'))

def draw_figure8(input_dir, input_file):

    output_dir = input_dir
    input_path = os.path.join(input_dir, input_file)

    plt.rc('text')
    matplotlib.rcParams['hatch.linewidth'] = 2.0
    df = pd.read_csv(input_path, delimiter='\t',  index_col='Target')

    afl = list(df['AFL'])
    dafl_score = list(df['DAFL_semRel'])
    dafl_select = list(df['DAFL_selIns'])
    dafl = [str(x) for x in list(df['DAFL'])]

    targets = list(df.index)

    tools = {
        'AFL': afl,
        'DAFL_score': dafl_score,
        'DAFL_inst': dafl_select,
        'DAFL': dafl,

    }

    color = {
        'DAFL': 'orangered',
        'DAFL_inst': 'darkorange',
        'DAFL_score': 'forestgreen',
        'AFL': 'dodgerblue',

    }

    ecolor = {
        'AFL': 'whitesmoke',
        'DAFL_score': 'whitesmoke',
        'DAFL_inst': 'whitesmoke',
        'DAFL': 'whitesmoke',

    }

    alpha = {
        'AFL': 0.5,
        'DAFL_score': 0.5,
        'DAFL_inst': 0.5,
        'DAFL': 1
    }

    hatch = {
        'AFL': None,
        'DAFL_score': None,
        'DAFL_inst': None,
        'DAFL': None,
    }

    bar_width = 0.3
    tic_distance = 2
    tickfontsize = 13

    fig, ax = plt.subplots(figsize= (15,5))

    plt.xticks([ x * tic_distance + 0.25  for x in range(0, len(targets))],
               fontsize=tickfontsize,
               rotation=30, ha='center', va='top')
    ax.xaxis.set_tick_params(width=2, size=5)
    plt.yticks(fontsize=tickfontsize)

    ax.set_xticklabels(targets)
    xidx = 0

    j = 0

    # a ghost bar to set the lowerbound of logscale
    plt.bar(0, 2, bar_width, color="white",  zorder=2, label='_nolegend_', log=True, alpha=0,)

    N = len(targets)
    for target in targets:
        i = 0
        to_x_list=[]
        for tool in tools:
            if "N.A." in str(tools[tool][j]):
                tte = 86400
            else:
                tte = int(tools[tool][j])

            x_cord = xidx + (i - 1) * (bar_width+0.04)

            plt.bar(x_cord,
                    tte,
                    bar_width,
                    color=color[tool],
                    hatch=hatch[tool],
                    # edgecolor=ecolor[tool],
                    zorder=2,
                    label=tool,
                    log=True,
                    alpha=alpha[tool]
                    )


            if tte == 86400:
                to_x_list.append(x_cord)

            i += 1

        if len(to_x_list) > 0:
            ax.text(sum(to_x_list)/len(to_x_list), 110000, "T.O.",
                    ha='center', va='bottom', fontsize=12, color='black')
        j += 1
        xidx += tic_distance
    plt.ylabel("TTE", size=15)

    # Note:
    # "ncol=4" : makes tools to be in one row, becase there are 4 of them.
    # "bbox_to_anchor" : makes the legend box to stay out of the plot.
    plt.legend((  'AFL', 'DAFL_SemRel', 'DAFL_SelInst', 'DAFL' ),
               fontsize=tickfontsize, ncol=4, bbox_to_anchor=(0.73,1.2))

    plt.margins(0.01)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir,'figure8.pdf'))

def draw_figure9(input_dir, input_file):

    output_dir = input_dir
    input_path = os.path.join(input_dir, input_file)

    plt.rc('text')
    matplotlib.rcParams['hatch.linewidth'] = 2.0
    df = pd.read_csv(input_path, delimiter='\t',  index_col='Target')

    afl = list(df['AFL'])
    dafl_energy = list(df['DAFL_energy'])
    dafl_seedpool = list(df['DAFL_seedpool'])
    dafl_semRel = [str(x) for x in list(df['DAFL_semRel'])]

    targets = list(df.index)

    tools = {
        'AFL': afl,
        'DAFL_seedpool': dafl_seedpool,
        'DAFL_energy': dafl_energy,
        'DAFL_SemRel': dafl_semRel,

    }

    color = {
        'DAFL_SemRel': 'orangered',
        'DAFL_seedpool': 'forestgreen',
        'DAFL_energy': 'darkorange',
        'AFL': 'dodgerblue',

    }

    ecolor = {
        'AFL': 'whitesmoke',
        'DAFL_seedpool': 'whitesmoke',
        'DAFL_energy': 'whitesmoke',
        'DAFL_SemRel': 'whitesmoke',

    }

    alpha = {
        'AFL': 0.5,
        'DAFL_seedpool': 0.5,
        'DAFL_energy': 0.5,
        'DAFL_SemRel': 1
    }

    hatch = {
        'AFL': None,
        'DAFL_seedpool': None,
        'DAFL_energy': None,
        'DAFL_SemRel': None,
    }

    bar_width = 0.3
    tic_distance = 2
    tickfontsize = 13


    fig, ax = plt.subplots(figsize= (15,5))

    plt.xticks([ x * tic_distance + 0.25  for x in range(0, len(targets))],
               fontsize=tickfontsize,
               rotation=30, ha='center', va='top')
    ax.xaxis.set_tick_params(width=2, size=5)
    plt.yticks(fontsize=tickfontsize)

    ax.set_xticklabels(targets)
    xidx = 0

    j = 0

    # a ghost bar to set the lowerbound of logscale
    plt.bar(0, 2, bar_width, color="white",  zorder=2, label='_nolegend_', log=True, alpha=0,)

    N = len(targets)
    for target in targets:
        i = 0
        to_x_list=[]
        for tool in tools:
            tte = int(tools[tool][j])
            x_cord = xidx + (i - 1) * (bar_width+0.04)

            plt.bar(x_cord,
                    tte,
                    bar_width,
                    color=color[tool],
                    hatch=hatch[tool],
                    # edgecolor=ecolor[tool],
                    zorder=2,
                    label=tool,
                    log=True,
                    alpha=alpha[tool]
                    )


            if tte == 86400:
                to_x_list.append(x_cord)

            i += 1

        if len(to_x_list) > 0:
            ax.text(sum(to_x_list)/len(to_x_list), 110000, "T.O.",
                    ha='center', va='bottom', fontsize=12, color='black')
        j += 1
        xidx += tic_distance
    plt.ylabel("TTE", size=15)

    # Note:
    # "ncol=4" : makes tools to be in one row, becase there are 4 of them.
    # "bbox_to_anchor" : makes the legend box to stay out of the plot.
    plt.legend((  'AFL', 'DAFL_SeedPool', 'DAFL_Energy', 'DAFL_SemRel$' ),
               fontsize=tickfontsize, ncol=4, bbox_to_anchor=(0.75,1.25))

    plt.margins(0.01)
    # plt.ylim([10,86400])
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir,'figure9.pdf'))

def draw_result(output_dir, target):
    if "tbl2" in target:
        draw_figure5(output_dir, target+".tsv")
    elif "fig7" in target:
        draw_figure7(output_dir, target+".tsv")
    elif "fig8" in target:
        draw_figure8(output_dir, target+".tsv")
    elif "fig9" in target:
        draw_figure9(output_dir, target+".tsv")
    else:
        print("Plotting not supported for this set of targets!")