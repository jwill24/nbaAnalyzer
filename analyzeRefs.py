# Create player teams dictionary dynamically

import sys
import requests
import pandas as pd
import array
import csv
import datetime
import itertools
import json
from bs4 import BeautifulSoup

#--------------------------------

def getDateString(date):
	wd, d, year = date.split(',')
	year = year.strip()
	month_name, day = d.split()
	time_object = datetime.datetime.strptime(month_name, '%b')
	month_number = time_object.month
	string = year + '{:02d}'.format(month_number) + '{:02d}'.format(int(day))
	return string

#--------------------------------

def getAbbreviation(team):
	for block in nba_teams:
		if block['teamName'] == team: return block['abbreviation']
	return 'None'

#--------------------------------

def getOfficials(html):
	loc = html.find('Officials')
	block = html[loc-13:loc+300]
	soup = BeautifulSoup(block, 'html5lib')
	string = soup.find('div').getText()[11:]
	return string.split(',')

#--------------------------------


# Dictionary for Chris Paul's teams over the years
teams = {
	2013 : 'LAC',
	2014 : 'LAC',
	2015 : 'LAC',
	2016 : 'LAC',
	2017 : 'LAC',
	2018 : 'HOU',
	2019 : 'HOU',
	2020 : 'OKC',
	2021 : 'PHO',
}

# Load JSON file
f = open ('teams.json', "r")
nba_teams = json.loads(f.read())

foster = 0
wins = 0 
losses = 0

# Get the schedule
for year in teams.keys():
	print(year)
	schedule_url = 'https://www.basketball-reference.com/teams/%s/%i_games.html' % (teams[year], year)
	html_schedule = requests.get(schedule_url).content
	df_schedule = pd.read_html(html_schedule)

	try: df_schedule[1]
	except: 
		print('No playoffs in %s' % year)
		continue

	for (date, home, opponent, win) in zip(df_schedule[1]['Date'], df_schedule[1]['Unnamed: 5'],\
		df_schedule[1]['Opponent'], df_schedule[1]['Unnamed: 7']):



		# Get home team abbreviation
		away = True if home == '@' else False
		if away: home_team = getAbbreviation(opponent)
		else: home_team = teams[year]
		
		# Convert date to url string format
		if date == 'Date': continue
		date_str = getDateString(date)

		game_url = 'https://www.basketball-reference.com/boxscores/%s0%s.html' % (date_str, home_team)
		soup = BeautifulSoup(requests.get(game_url).content, 'html5lib')
		#print(soup)

		
		# Did CP3 win?
		win = True if win == 'W' else False

		if win: wins += 1
		else: losses += 1

		# Is Scott Foster a ref?
		html_game = str(requests.get(game_url).content)
		officials = getOfficials(html_game)

		if 'Scott Foster' in officials: 
			foster += 1
			print('Scott Foster reffed on %s' % date)

print('Scott Foster has reffed %i playoff games of CP3' % foster)
print('Since Apr 20, 2013, CP3 is %i and %i in playoff games' % (wins, losses))


# Print number of Foster games
