import requests
import pandas as pd
import array
import csv
import os
import sys
import matplotlib.pyplot as plt
from matplotlib import cm as cm
import matplotlib.ticker as ticker


#----------------
#Did the team win?

def didWin(wl):
    return( bool( wl == 'W' ) )

#----------------
#Get the win percentage

def winPercent(win,loss):
    if win+loss == 0: return('N/A')
    else: return( round( win/(win+loss),2 ) )

#----------------
#Get the players stats from Basketball Reference and create a csv file

def getWeb(name):
    first = name.split(' ', 1)[0]
    last = name.split(' ', 1)[1]

    if len(last) < 5:
        abr = last[0]+last[1]+last[2]+last[3]
    else:
        abr = last[0]+last[1]+last[2]+last[3]+last[4]

    url = 'https://www.basketball-reference.com/players/' + first[0] + '/' + abr + first[0] + first[1] + '01/gamelog/2019/'

    html = requests.get(url).content
    df_list = pd.read_html(html)
    df = df_list[-1]
    df.to_csv(last+'.csv')
    return()

#----------------

def isEmpty(row):
    if row == "":
        return True
    else:
        return False

#----------------

def storePct(row):
    if isEmpty(row):
        return 0
    else:
        return float( row )

#----------------

def getTime(time):
    minutes = float( time.split(':', 1)[0] )
    seconds = float( time.split(':', 1)[1] )
    return( float(minutes) )

#----------------
#Plot the correlation matrix

def correlation_matrix(name,df):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    #ax1 = fig.add_subplot()
    cmap = cm.get_cmap('jet', 30)
    cax = ax1.imshow( abs( df.corr() ), interpolation="nearest", cmap=cmap)
    #ax1.grid(True)
    plt.title('Correlation Coefficientss for '+name)
    labels=['', 'AST',  'BLK',   'DRB',    'FG',   'FGA',    'FGP',   'FT',   'FTA', 'FTP',  'MP',  'ORB',  'PTS',  'STL', 'TO',   'TP',  'TPA',  'TPP',   'TRB',  'Win']
    ax1.set_xticklabels(labels,fontsize=6)
    ax1.set_yticklabels(labels,fontsize=6)
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(1))
    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    fig.colorbar(cax, ticks=[.25,.5,.75,1.])
    plt.show()


#----------------

def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop

#----------------

def get_top_abs_correlations(df, n=5):
    au_corr = df.corr().abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr[0:n]

#----------------



#----------------


