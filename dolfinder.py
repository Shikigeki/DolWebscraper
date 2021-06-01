#author William David
#NOTE NEEDS A CSV FILE NAMED special_cases.csv AS WELL AS zip_code_data.csv

import requests
from bs4 import BeautifulSoup

#part1
#set up for what i need
#create a class to store a state withits respective minimum wage
class StateWage:
	def __init__(self, name,abrev, minWage):
		self.name = name
		self.minWage = minWage
		self.abrev = abrev
	def __str__(self):
		return "name: "+ self.name + ", abrevetaion: " + self.abrev + ", minimum wage: "+ self.minWage
	def getName(self):
		return self.name
	def getMinWage(self):
		return self.minWage
	def getAbrev(self):
		return self.abrev

class SpecialPlace:
	def __init__(self, name, minWage, stateAbrev):
		self.name = name
		self.minWage = minWage
		self.stateAbrev = stateAbrev
	def __str__(self):
		return "name: " + self.name+", minimum wage: " + self.minWage + ", in the state: " + self.stateAbrev

#a dictionary to match all usa states with ther respective postal codes
stateDic = {
	"Alabama" : "AL",
	"Alaska" : "AK",
	"Arizona" : "AZ",
	"Arkansas" : "AR",
	"California" : "CA",
	"Colorado" : "CO",
	"Connecticut" : "CT",
	"Delaware" : "DE",
	"Florida" : "FL",
	"Georgia" : "GA",
	"Hawaii" : "HI",
	"Idaho" : "ID",
	"Illinois" : "IL",
	"Indiana": "IN",
	"Iowa": "IA",
	"Kansas": "KS",
	"Kentucky": "KY",
	"Louisiana" : "LA",
	"Maine" : "ME",
	"Maryland": "MD",
	"Massachusetts": "MA",
	"Michigan" : "MI",
	"Minnesota" : "MN",
	"Mississippi": "MS",
	"Missouri": "MO",
	"Montana" : "MT",
	"Nebraska": "NE",
	"Nevada" : "NV",
	"New Hampshire" : "NH",
	"New Jersey" : "NJ",
	"New Mexico" : "NM",
	"New York" : "NY",
	"North Carolina" : "NC",
	"North Dakota" : "ND",
	"Ohio" : "OH",
	"Oklahoma": "OK",
	"Oregon": "OR",
	"Pennsylvania": "PA",
	"Rhode Island" : "RI",
	"South Carolina" : "SC",
	"South Dakota" : "SD",
	"Tennessee" : "TN",
	"Texas" : "TX",
	"Utah" : "UT",
	"Vermont": "VT",
	"Virginia": "VA",
	"Washington": "WA",
	"West Virginia" : "WV",
	"Wisconsin" : "WI",
	"Wyoming" : "WY",
	"District of Columbia" : "DC",
	"Commonwealth of the Northern Mariana Islands" : "CNMI",
	"Puerto Rico" : "PR",
	"American Samoa" : "AS", #special case no descript wage on dol at time of waking this web crawler
	"Virgin Islands" : "VI",
	"Guam" : "GU"
}


#part2
#a list to store each of tthe states with there minimum wage
minimumWages = []
#grabs the html of page https://www.dol.gov/agencies/whd/minimum-wage/state
URL = 'https://www.dol.gov/agencies/whd/minimum-wage/state'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())

grabStrong = False
parsWage = []
wage1 = ""
wage2 = ""
wageprime = ""
stateName = ""

for x in soup.find_all(['h2', 'strong']):
	if(x.name =='h2'):
		grabStrong = True
	if((x.text[0] == ' ') or (x.text[len(x.text) - 2] == ':') or (grabStrong == False)):
		continue
	#stores up to 2 minimum wages in wage1 and wage2 and takes the bigger one after finding a new state
	if(x.name == 'strong'):
		parseWage = str(x.text).split(" ")
		if(len(parseWage) <= 14):
			wage1 = wage2
			wage2 = parseWage[5]
			
		elif(parseWage[0] == "Employers"):
			wage1 = wage2
			wage2 = parseWage[16]
			
		#print(x.text)
	#every time a new state is found it uses the minimum wages found
	elif(x.name == 'h2'):
		if(x.text != "Alabama"):
			try:
				#print(float(wage2.split("$")[1]))
				#print(float(wage1.split("$")[1]))
				
				#if(wage1 == ""):
					#wageprime = wage2.split('$')[1].split(';')[0]
				if(float(wage2.split("$")[1])>float(wage1.split("$")[1])):
					wageprime = wage2.split('$')[1].split(';')[0]
				else:
					wageprime = wage1.split('$')[1].split(';')[0]
			except:
				try:
					wageprime = wage2.split('$')[1].split(';')[0]
				except:
					wageprime = "CANNOT BE FOUND"
			s = StateWage(stateName, stateDic.get(stateName, "NOT A STATE"), wageprime)
			minimumWages.append(s)
			
		wage1 = ""
		wage2 = ""	
		wageprime = ""
		stateName = str(x.text)
#does the h2 check one last time to get min wage for guam
try:
	if(float(wage2.split("$")[1])>float(wage1.split("$")[1])):
		wageprime = wage2.split('$')[1].split(';')[0]
	else:
		wageprime = wage1.split('$')[1].split(';')[0]
except:
	try:
		wageprime = wage2.split('$')[1].split(';')[0]
	except:
		wageprime = "CANNOT BE FOUND"
s = StateWage(stateName, stateDic.get(stateName, "NOT A STATE"), wageprime)
minimumWages.append(s)
#now we have a complete list filled with the class statewage that holds a state of america and its resective minimum wage


#part3
#now have to get all special cases from
fread = open("special_cases.csv", 'r')
lineArr = []
start = False
isCounty = False
specialCases = []
for line in fread:
	lineArr = line.split(',')
	if(lineArr[0] == "City" or lineArr[0] == "County"):
		start = True
		if(lineArr[0] == "County"):
			isCounty = True
		continue
	elif(lineArr[0] == ""):
		start = False
	if(start):
		pName = lineArr[0].split('&')
		for y in pName:
			if(isCounty):
				sp = SpecialPlace(y + " County",lineArr[2].split("$")[1], lineArr[1])
			else:
				sp = SpecialPlace(y,lineArr[2].split("$")[1], lineArr[1])
			specialCases.append(sp)

#for x in specialCases:
	#print(x)

fread.close()
#for x in specialCases:
	#print(x)
#part4 writing to csv 
#holds the prevously used minwage of a state to make iterating through 40,000+ items faster
prevState = ""
prevMinWage = ""
#zip code of current line
zipcode = ""
zipCol = 0
#city of current zip code
city = ""
cityCol = 1
#state of current zip code
state = ""
stateCol = 2
#county of current zip code
county = ""
countyCol = 3
#minimum wage of current czip code
minwage = ""
#flages to 1 if current line needs checking
nc = 0
line = ""
foundC = False

fwrite = open("zip_code_wage.csv", 'w')
fread2 = open("zip_code_data.csv", 'r')
fwrite.write("zipcode,city,state,county,jurisdiction,minimum wage\n")
fread2.readline()
for x in fread2:
	line = x.split("\n")[0].split(",")
	#if(prevC.lower() == line[cityCol].lower())
	for y in specialCases:
		if((y.name.lower() == line[cityCol].lower()) and (y.stateAbrev.lower() == line[stateCol].lower())):
			#print(y.minWage)
			zipcode = line[zipCol]
			city = line[cityCol]
			state = line[stateCol]
			county = line[countyCol]
			minwage = y.minWage
			fwrite.write(zipcode+","+city+","+state+","+county+",City,"+minwage+"\n")
			foundC = True
			break
		elif((y.name.lower() == line[countyCol].lower()) and (y.stateAbrev.lower() == line[stateCol].lower())):
			#print(y.minWage)
			zipcode = line[zipCol]
			city = line[cityCol]
			state = line[stateCol]
			county = line[countyCol]
			minwage = y.minWage
			fwrite.write(zipcode+","+city+","+state+","+county+",County,"+minwage+"\n")
			foundC = True
			break
	if(foundC):
		foundC = False
		continue
	#looks to see if the state is the same so we dont have to iterate through 50~ items 40,000 times
	if(prevState.lower() == line[stateCol].lower()):
		fwrite.write(line[zipCol]+","+line[cityCol]+","+line[stateCol]+","+line[countyCol]+",State,"+prevMinWage+"\n")
		continue
	#gets the minimum wages of states that arnt special from the minWage list
	for y in minimumWages:
		if(str(y.abrev).lower() == line[stateCol].lower()):
			prevMinWage = y.minWage
			prevState = y.abrev
			zipcode = line[zipCol]
			city = line[cityCol]
			state = line[stateCol]
			county = line[countyCol]
			minwage = y.minWage
			fwrite.write(zipcode+","+city+","+state+","+county+",State,"+minwage+"\n")
			continue


	#print(line)


fwrite.close()
fread2.close()






























