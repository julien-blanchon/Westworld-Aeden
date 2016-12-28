#!/usr/bin/python
from websocket import create_connection
import requests #Need to get the session (Post request).
import json #Need to make the any request in the right form.
import calendar #Need to get the timescamp for the post request.
import time #Also need for the timescamp.
import sys #Need if you want print that in a file ($ python aeden.py >> outpout.txt) and for cli version
import csv
reload(sys)
sys.setdefaultencoding('utf-8') #For make it printable in a file

try: #Try if the path of the dataset is specified
	importfilepath = sys.argv[1] #The path of file to get dataset of word or sentence.
except: #If any path is in argument, exit.
	print "python aeden.py <YourWordDataset>"
	sys.exit()

importfile = open(importfilepath).read().splitlines() #Default take sentence of each line.
# words = open(importfile).read().split(",") #Take all sentence between ",".
# words = open(importfile).read().split(";") #Take all sentence between ";".
# words = open(importfile).read().split(" ") #Take all sentence between " " (space).

yourdataset = []
for i in importfile:
	if len(i)>17 and i not in yourdataset: #Drop the short and duplicate question
		yourdataset.append(i)

try : #Try if the path of the dataset is specified
	exportfilepath = sys.argv[2] #The path of the csv to export.
	exportfile = open(exportfilepath, 'r+a') #Open the exportfilepath specified in argument for append and read. Read for import any topic_id and append for append it all the new topic_id discovery.
except: 
	exportfilepath = "output.csv" #If any path is specified just create one
	exportfile = open(exportfilepath, 'w') #Create and open a output.csv file.

AlreadyCsvID=[]
for line in exportfile: #Import current CSV.
	AlreadyCsvID.append(line.strip().split(',')) #Transorm the csv in a clear list

AlreadyID=[] #Import all ID discovery in the current CSV.
for i in enumerate(AlreadyCsvID): #Just take the MSG ID in the csv (without duplicate)
		try:
			if i not in AlreadyID:
				AlreadyID.append(AlreadyCsvID[i[0]-1][2])
		except:
			AlreadyID.append("None")

del AlreadyCsvID

def connection(): 
	url="https://zoobot-live.appspot.com/bot/5649391675244544/chat" #URL to post to get WebSocket.
	data=json.dumps({
		"timestamp": calendar.timegm(time.gmtime()), #Get actual time (Timestamp Epoch)
		"actor": "bot", 
		"user_id": "USER",
		"bot_id": 5649391675244544,
		"action": "start"})
	print "Getting session ..."
	response = requests.post(url,data).content #Send POST to launch session.
	global socket_uri
	socket_uri = json.loads(response)["metadata"]["socket_uri"] #Extract the Websocket session url in socket_uri.
	global session_id
	session_id = json.loads(response)["session_id"] #Extract Websocket session id in session_id.

	print "Connection to Aeden ..."
	global ws
	ws = create_connection(socket_uri) # Connection to Aeden on the session previously generated. 

	print "Connected !"
	print "-----------------------------------------------" #Get and print the initialisation message.
	result = json.loads(ws.recv()) #Get the welcome message and make it readable (json).
	msgtext = result["messages"][0]["text"] #Get the text welcome message. (Currently: 'Hello! It's so nice to meet you. What questions can I answer about Westworld?').
	msgimg = result["messages"][0]["media_url"] #Get image welcome message (Currently there are none).
	msgid = result["metadata"]["topic_name"] #Get topic name welcome message (Currently: '__welcome__').
	print "Welcome message: "
	print "\nText :'%s'" % msgtext
	print "Image :'%s'" % msgimg
	print "ID :'%s'" % msgid
	print "-----------------------------------------------"

	print "\nSession Start: "

def buildQuestion(question): #Build the question request with the right syntax and print the question. The question request need the session_id (int) of the current session, the timestamp (int) and sure the question (string).
	ws.send( 			#Send the question request in right syntax.
		json.dumps({ 			#Build the question request in the right syntax.
			"action": 'inbound',
			"actor": 'bot',
			"bot_id": 5649391675244544,
			"message": {"text": question}, #Question to ask.
			"session_id": session_id, #Session id of the current session.
			"timestamp": calendar.timegm(time.gmtime())} #Timestamp
		,separators=(',',':'))) #for json.dump

	print "\nSent: %s" % question #Print what is the question.
	
def buildReponse(question): #Get and print the question response.
	result = json.loads(ws.recv()) #Get the question response and make it readable (json).
	msgtext = result["messages"][0]["text"] #Get the question response (text).
	msgimg = result["messages"][0]["media_url"] #Get the question response (link of image).
	msgid = result["metadata"]["topic_name"] #Get the topic name of the response (id). '__unknown__' for a question misunderstood.
	print "Text: %s" % msgtext
	print "Image: %s" % msgimg
	print "ID: %s" % msgid
	if ((msgid in AlreadyID) and (msgid != "glitch")): #If this ID is already in the csv don't append it.
		print "     Already in the file"
	elif msgid == "__unknown__": #If this ID is a unknow don't append it
		print "		Just a unknown"
	elif msgid == "glitch": #If this ID is a glitch append it and ENJOY.
		print "     Enjoy, a new glitch"
		exportfile.write("%s,%s,%s,%s\n" % (question.replace(",","").replace("\n", ". "), msgtext.replace(",","").replace("\n", ". ").replace(), msgimg.replace(",",";").replace("\n", "; ")))  #Export each result with new ID in a csv without ","
	else: #If this ID is not in the cvs append it and ENJOY.
		print "     Enjoy, a new ID" #If this ID is not in the current csv, append it and ENJOY.
		AlreadyID.append(msgid)
		exportfile.write("%s,%s,%s,%s\n" % (question.replace(",","").replace("\n", ". "), msgtext.replace(",","").replace("\n", ". "), msgid, msgimg.replace(",",";").replace("\n", "; "))) #Export each result with new ID in a csv without ","
	

def ask(question): #Final function for ask question to Aeden.
	buildQuestion(question) #Ask Question.
	buildReponse(question) #Take Response.
	
def filter_list(full_list, excludes):
	s = set(excludes)
	return (x for x in full_list if x not in s)

QuestionAlreadyAsk=["Hello"]
while QuestionAlreadyAsk[-1] != yourdataset[-1]:
	connection()
	for question in list(filter_list(yourdataset, QuestionAlreadyAsk)): #Finall loop for ask any element in the dataset and get final result.
		ask(question) #For each ask
		QuestionAlreadyAsk.append(question)
		
print "\n Session close"
print "\n The last question was: ", QuestionAlreadyAsk[-1]
ws.close() #Close Aeden session.	