#!/usr/bin/python
# -*- coding: UTF-8 -*-

# not sure if this ^ is necessary
# but it was recommended, and i
# was too scared to take it out

# Stephen Norod

import cgi
import cgitb
import requests
import json
cgitb.enable()
form = cgi.FieldStorage()

username = "sayak97"
# HARDCODED! Would typically take in username via the line below,
# but I don't have Apache or something similar to run the script
# from my HTML file
#
# username =  form.getvalue('username')

animeBaseURL = "https://api.jikan.moe/v3/"

url = animeBaseURL + "user/" + username + "/animelist/completed"
response = requests.get(url)
parsed_json = json.loads(response.text)
mal = [] # list of titles
datesDict = {} # dictionary mapping titles to the date the anime was released

# dictionary mapping titles to the URL of their images (for display purposes)
# did not have time to properly implement
imagesDict = {}

scores = [] # list of the scores given to the anime by the user (0-10)
for anime in parsed_json['anime']:
    mal.append(anime['title']) # add to the list of titles

     # start_date param is in form yyyy-mm-dd but then some more time stamp stuff,
     # so i just took the first ten characters, which is especially nice because
     # it's the same format which the Russian api takes in as a parameter
    datesDict[anime['title']] = anime['start_date'][:10]

    # imagesDict[anime['title']] = was in the middle of typing when time ran out sad.jpg
    scores.append(anime['score']) # add to the list of scores

# following code is for sorting the scores (don't care about low reviewed anime),
# then mapping that sorting order to the list of titles using zip
tups = zip(mal, scores)
tups.sort()
zip(*tups)
mal.reverse()
scores.reverse()

# to store boolean values of holiday/not with dates as keys
finalDict = {}

holidayBaseURL = "https://datazen.katren.ru/calendar/day/"

# could be less than 5 anime in the list (arbitrary number, figured I'd show top 5) so must be careful
for i in xrange(min(len(mal), 5)):

    title = mal[i]
    date = datesDict[mal[i]]
    url = holidayBaseURL + date + "/"

    response = requests.get(url)
    parsed_json = json.loads(response.text)
    holiday = parsed_json['holiday']
    finalDict[title] = holiday

for i in finalDict:
    print("Yes, " + i + " was released on a Russian holiday!" if finalDict[i] else "No, " + i + " was not released on a Russian holiday :,-(")

# goal from here would be to map the image url dictionary to these boolean values
# and display these two things nicely on a webpage
