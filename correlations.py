import requests
import pandas as pd
import array
import csv
import os
import sys
import matplotlib.pyplot as plt
from  common import didWin, winPercent, getWeb, isEmpty, storePct, getTime, correlation_matrix, get_top_abs_correlations

d = []
coef = []

print('')
name = input('What player do you want correlations for? ')

getWeb(name)

file = csv.reader(open(name.split(' ', 1)[1]+'.csv', "r"), delimiter=",")

for row in file:

    #Skip rows without data
    if row[18] == 'Inactive' or row[18] == 'FTA' or row[18][0] == 'D' or row[18][0] == 'N': continue

    d.append( { 'Win': (0,1)[didWin(row[8][0])], 'MP': getTime(row[10]), 'FG': float(row[11]), 'FGA': float(row[12]), 'FGP': storePct(row[13]), 'TP': float(row[14]), 'TPA': float(row[15]), 'TPP': storePct(row[16]), 'FT': float(row[17]), 'FTA': float(row[18]), 'FTP': storePct(row[19]), 'ORB': float(row[20]), 'DRB': float(row[21]), 'TRB': float(row[22]), 'AST': float(row[23]), 'STL': float(row[24]), 'BLK': float(row[25]), 'TO': float(row[26]), 'PTS': float(row[28]) } )

df = pd.DataFrame(d)

print( df.corr() )
print('')
print('MP corr: ', df['MP'].corr( df['Win'] ) )

correlation_matrix(name,df)





        

        
    
