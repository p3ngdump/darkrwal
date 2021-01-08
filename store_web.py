import os
import sys

def store(file):
	cur_path = os.getcwd()

	title_flag = 0
	title = ""

	value = keyword(file)
	if(value):
		for i in file:
			if(title_flag):
				title = i
				title_flag
			if(title == "" and 'title' in i):
				title_flag = 1

		f = open(title + ".html", "w")
		f.write(file)
		f.close()
	else:
		return False

def keyword(file):
	score = 0
	keyword = ['sex', 'ransom', 'virus', 'worm', 'apt', 'hack', 'drug', 'cocaine', 'addict', 'backdoor', 'trojan', 'bypass', 'vulnerabl', 'attack', 'ransomware', 'hacker', 'rape', 'violate', 'vulnerable', 'vulnerability']

	for i in file:
		for j in keyword:
			if(j in i):
				score += 1

	if(score > 5):
		return True
	else:
		return False