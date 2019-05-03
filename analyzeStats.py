import requests
import pandas as pd
import array
import csv
import os
import sys
import matplotlib.pyplot as plt


#----------------

def didWin(wl):
    return( bool( wl == 'W' ) )

#----------------

def winPercent(win,loss):
    if win+loss == 0: return('N/A')
    else: return( round( win/(win+loss),2 ) )

#----------------

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

myGrey = '#FBFBFB'

win = [0] * 28
loss = [0] * 28
pct = [0] * 28

MAXFTA = 28
MAXTPA = 24

group1 = [0] * 2
group2 = [0] * 2
group3 = [0] * 2

g1 = 0.
g2 = 0.
g3 = 0.



name = input('What player do you want info about? ')

getWeb(name)

#exist = os.path.isfile('harden.csv')
#if exist:
#    print('Harden file already exist')
#else:


file = csv.reader(open(name.split(' ', 1)[1]+'.csv', "r"), delimiter=",")
#fieldnames = ['RANK', 'GAME', 'DATE', 'AGE', 'TEAM', 'HOME', 'OPP', 'WL', 'GS', 'MP', 'FG', 'FGA', 'FGP', '3P', '3PA', '3PP', 'FT', 'FTA', 'FTP', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'GmSc', 'PM']

playoff_teams = ['MIL','TOR','PHI','BOS','IND','BRK','ORL','DET','GSW','LAC','HOU','UTA','POR','OKC','DEN','SAS']
games = [1, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 58, 60, 61, 62, 63, 64, 65, 66, 67, 68, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82]


#--------------

for row in file:
    
    #Skip rows without data
    if row[18] == 'Inactive' or row[18] == 'FTA':
        continue
    
    #Only consider playoff teams
    for x in playoff_teams:
        if row[7] == x:

        #Only consider big3 games
	    #for x in games:
            #if float( row[1] ) == x:
            
        #Find number of FTAs
            for i in range(MAXTPA):
                if float(row[15]) == i:
                    if didWin(row[8][0]):
                        win[i] += 1
                    else:
                        loss[i] += 1

#print('Win', win)
#print('Loss', loss)

for i in range(MAXTPA):
    tmp_w = win[i]
    tmp_l = loss[i]

    if i >= 0 and i < 9:
        group1[0] += win[i]
        group1[1] += loss[i]
    if i > 8 and i < 16:
        group2[0] += win[i]
        group2[1] += loss[i]
    if i > 15:
        group3[0] += win[i]
        group3[1] += loss[i]

    pct[i] = winPercent(tmp_w,tmp_l)

g1 = winPercent(group1[0],group1[1])*100
g2 = winPercent(group2[0],group2[1])*100
g3 = winPercent(group3[0],group3[1])*100

#print('Percentages', pct)

print( g1, g2, g3 )

#--------------------

#Plot the win percentages
fig, ax = plt.subplots()
fig.canvas.draw()

#3PA xlabels
xlabels = ['','0-8','','','','9-15','','','','16+']

#FTA xlabels
#xlabels = ['','0-6','','','','7-14','','','','15+']

ylabels = ['20%','40%','60%','80%','100%']

plt.plot([g1,g2,g3])
plt.axhline(y=57.14, color='r', linestyle='--', lw=0.75, label='Total win %')
plt.ylabel('Win Percentage')
plt.xlabel('Three Point Attempts')
plt.title('Win Percentage vs 3PAs', fontweight='bold', fontsize=16)

ax.set_xticklabels(xlabels)
ax.set_yticks( range(20,100,20) )
ax.set_yticklabels(ylabels)

#ax.patch.set_facecolor(myGrey)

plt.legend(loc='lower right', fancybox=True, framealpha=0.1)
plt.show()

fig.savefig('winpct_vs_3pa.png', transparent=True)


