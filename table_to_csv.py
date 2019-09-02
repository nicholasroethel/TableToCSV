 # ============================================================================
 # Name        : table_to_csv.py
 # Author      : Nicholas Roethel
 # Description : A program which takes html files containing tables and converts them
 # to to csv files
 # ============================================================================

import sys
import re
import csv
import argparse

def theOutput(tableList):
	count = 0
	for table in tableList:
		count = count +1
		if count >1:
			print("\n", end='')
		print("TABLE {}:\n" .format(count), end='')
		for item in table:
			print("%s\n" % (','.join(map(str, item[0:]))), end='')

def getTables(tableList,text):
	text = re.sub(r"\n"," ",text)
	regexForTh = "<th[^>]*>\n?(.*?)\n?</th>" #code for finding tags
	compiledTh = re.compile(regexForTh,re.IGNORECASE)
	regexForTd = "<td[^>]*>\n?(.*?)\n?</td[^>]*>"
	compiledTd = re.compile(regexForTd,re.IGNORECASE)
	regexForTr = "<tr[^>]*>(.*?)</tr[^>]*>" 
	compiledTr = re.compile(regexForTr,re.IGNORECASE)
	regexForTable = ("<table[^>]*>(.*?)</table[^>]*>")
	compiledTable = re.compile(regexForTable,re.IGNORECASE)
	tables = re.findall(compiledTable,text)

	for table in tables:
		isHeader = 0
		lines = []
		headerline = re.findall(compiledTh,table)
		if(len(headerline)>0):
			isHeader = 1
			lines.append(headerline)
		rows = re.findall(compiledTr,table)
		maxlen = 0

		for element in rows: #appends entries
			element = ' '.join(element.split())
			lines.append(re.findall(compiledTd,element))

		if(isHeader == 1):
			lines.pop(1) #pop out the header if it exists

		for entry in lines: #removing whitespace
		 	for element in entry:
		 		lines = [[s.strip() for s in inner] for inner in lines]

		for entry in lines: #gets maxlen
			size = len(entry)
			if size>maxlen:
				maxlen = size

		for entry in lines: #appends commas
			diff = maxlen - len(entry)
			for x in range(0,diff):
				entry.append('')
		tableList.append(lines)

def main():
	tableList = []
	if(sys.stdin.isatty() is True): #checks for nothing in stdin
		sys.exit(0)
	data = sys.stdin.read()
	getTables(tableList,data)
	theOutput(tableList)
  		
if __name__ == "__main__":
	main()
