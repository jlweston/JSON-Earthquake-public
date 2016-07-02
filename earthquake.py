import json
import requests
import calendar
import time
from datetime import date
import datetime
import tweepy, time, sys

CONSUMER_KEY = 'xxxxxxxxxxxxxxxxxxxx'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxx'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxx'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'#keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# fetch data from JSON source and pass to printResults()
def main():
	urlData = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson'
	r = requests.get(urlData)
	if r.status_code == requests.codes.ok:
		data = r.json()
		printResults(data)
	else:
		print("Something went wrong.")


# print all magnitude, location and time/date in console if more recent than recorded timestamp
def printResults(data):
	if "title" in data["metadata"]:
		print (data["metadata"]["title"])
		print ("There were",data["metadata"]["count"],"earthquakes of at least magnitude 2.5 in the last 24 hours.")
	recentTimestamp = findRecent()
	for i in data["features"]:
		seconds = i["properties"]["time"]/1000
		output = str("There was a " + str(i["properties"]["mag"]) + " magnitude earthquake ")
		output = output + str(i["properties"]["place"]+" at "+str(time.strftime('%H:%M:%S %d-%m-%Y', time.localtime(seconds)))+" #earthquake")

		if (seconds > recentTimestamp):
			print(output)
			recentTimestamp = seconds
			api.update_status(status=output)
		else:
			break
			print("No new earthquakes since last report.")
	recordRecent(recentTimestamp) #save timestamp of most recent earthquake to file


def recordRecent(time):
	f = open('record.txt','w')
	time = str(time)
	f.write(time)
	f.close()

def findRecent():
	f = open('record.txt', 'r')
	f.seek(0)
	first_char = f.read(1)
	if not first_char:
		return 0
	else:
	    f.seek(0)
	time = float(f.read())
	return time

7

if __name__ == "__main__":
	while True:
		main()
		print("Waiting for new data...")
		time.sleep(90)
