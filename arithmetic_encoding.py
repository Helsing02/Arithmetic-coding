import os
from decimal import Decimal, getcontext
class Node:
	def __init__(self, char, num_in_text, freq="0", low="0", high="0"):
		self.char=char
		self.num_in_text=num_in_text
		self.freq=Decimal(freq)
		self.low=Decimal(low)
		self.high=Decimal(high)
	def __repr__(self):
		return repr((self.char, self.freq, self.low, self.high))
	def __str__(self):
		return str(self.char)+" "+str(self.num_in_text)+" "+str(self.freq)+' '+str(self.low)+' '+str(self.high)
	def new_lr(self, interval):
		new_inter=[interval[0]+(interval[1]-interval[0])*self.low, interval[0]+(interval[1]-interval[0])*self.high]
		return new_inter 

def proverka(obj, interval):
	inter=obj.new_lr(interval)
	return inter[1]-inter[0]>Decimal("1")/2**32

def count_freq(path_orig):
	freq=[0 for i in range(129)]
	try:
		original_file=open(path_orig, "r")
	except:
		print("Указанный файл не может быть открыт")
		input("Нажимте Enter для закрытия консоли")
		exit()

	sym=original_file.read(1)
	len_of_mess=0
	while(sym!=''):
		try:
			freq[ord(sym)]+=1
		except:
			print('Символ "'+sym+'" не из семибитной кодировки ASCII')
			input("Нажимте Enter для закрытия консоли")
			exit()
		sym=original_file.read(1)
		len_of_mess+=1
	freq[128]=len_of_mess
	original_file.close()
	return freq

def make_list(path):
	freq=count_freq(path)
	node_list=[]
	for i in range(128):
		if freq[i]!=0:
			d=Decimal(str(freq[i]))
			node_list.append(Node(chr(i), freq[i], d/freq[128]))
	node_list=sorted(node_list, key=lambda i: i.freq, reverse=True)
	to_sum=0
	for i in node_list:
		i.low=Decimal(str(to_sum))
		to_sum+=i.freq
		i.high=Decimal(str(to_sum))
	return node_list

def write(fileadr, interval):
	bits=0
	cont=Decimal("0")
	for i in range(1, 33):
		bits=bits<<1
		if (cont+Decimal("1")/(2**i))<interval[1]:
			bits|=1
			cont+=Decimal("1")/(2**i)
	for j in range(3, -1, -1):
		new_i=bits>>8*j
		fileadr.write(bytes([new_i&255]))
	
def encoding(path_orig, node_list):
	try:
		original_file=open(path_orig, "r")
		encoded_file=open(path_orig[:-4]+"(encoded).txt", 'wb')
	except:
		print("Указанный файл не может быть открыт")
		input("Нажимте Enter для закрытия консоли")
		exit()
	for i in node_list:
		encoded_file.write((i.char+str(i.num_in_text)+'\x01').encode("ascii"))
	encoded_file.write("\x02".encode("ascii"))

	interval=[Decimal("0"), Decimal("1")]
	sym=original_file.read(1)
	while sym!='':
		for i in node_list:
			if i.char==sym:
				if proverka(i, interval):
					interval=i.new_lr(interval)
					sym=original_file.read(1)
				else:
					write(encoded_file, interval)
					interval[0]=Decimal("0")
					interval[1]=Decimal("1")
				break
	if (interval!=[Decimal("0"), Decimal("1")]):
		write(encoded_file, interval)



#вызовы 
getcontext().prec=38
path=input("Введите путь файла для кодировки: ")
# path='c:\\users\\user\\desktop\\text.txt'


node_list=make_list(path)

encoding(path, node_list)

a=os.stat(path).st_size
b=os.stat(path[:-4]+'(encoded).txt').st_size
print('Сжатие %f%%' %(b/a*100))

