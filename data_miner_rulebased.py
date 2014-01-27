import csv
import random

def main():
	data=list(datareader())
	random.shuffle(data)
	dataset1=data[:16]
	dataset2=data[17:]
	print dataset1
	print dataset2

def datareader():
	with open('data1.txt', 'rb') as csvfile:
		datafromfile = list(csv.reader(csvfile, delimiter=' ', quotechar='|'))
		del datafromfile[0]
	return datafromfile
		#for row in datafromfile:
			#print row

main()