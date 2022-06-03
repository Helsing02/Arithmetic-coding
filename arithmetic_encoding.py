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




def prov(interval):
	return interval[1]-interval[0]>Decimal("1")/2**32


def count_freq(name):
	count=0
	freq=[0 for i in range(129)]
	try:
		read_file=open(name, "r")
	except:
		print("Указанный файл не может быть открыт")
		input("Нажимте Enter для закрытия консоли")
		exit()
	sym=read_file.read(1)
	while(sym!=''):
		try:
			freq[ord(sym)]+=1
		except:
			print('Символ "'+sym+'" не из семибитной кодировки ASCII')
			input("Нажимте Enter для закрытия консоли")
			exit()
		sym=read_file.read(1)
		count+=1
	read_file.close()
	freq[128]=count
	return freq

def make_list(freq):
	node_list=[]
	for i in range(128):
		if freq[i]!=0:
			d=Decimal(str(freq[i]))
			node_list.append(Node(chr(i), freq[i], d/freq[128]))
	node_list=sorted(node_list, key=lambda i: i.freq, reverse=True)
	collect=0
	for i in node_list:
		i.low=Decimal(str(collect))
		collect+=i.freq
		i.high=Decimal(str(collect))
	return node_list

def check(curr, interval):
	if interval[0]<=curr and interval[1]>curr:
		return -1
	if interval[0]<=curr:
		return 0
	return 1

def write(fileadr, interval):
	cont=Decimal("0")
	bits=0
	t=True
	for i in range(1, 33):
		bits=bits<<1
		if (cont+Decimal("1")/(2**i))<interval[1]:
			bits=bits|1
			cont+=Decimal("1")/(2**i)
	for j in range(3, -1, -1):
		new_i=bits>>8*j
		fileadr.write(bytes([new_i&255]))
	

def encoding(name, node_list):
	try:
		to_encode=open(name, "r")
		encoded=open(name[:-4]+"(encoded).txt", 'wb')
	except:
		print("Указанный файл не может быть открыт")
		input("Нажимте Enter для закрытия консоли")
		exit()
	for i in node_list:
		encoded.write((i.char+str(i.num_in_text)+'\x01').encode("ascii"))
	encoded.write("\x02".encode("ascii"))

	curr_num=0
	interval=[Decimal("0"), Decimal("1")]
	sym=to_encode.read(1)

	while sym!='':
		for i in node_list:
			if i.char==sym:
				if prov(i.new_lr(interval)):
					interval=i.new_lr(interval)
					sym=to_encode.read(1)
				else:
					write(encoded, interval)
					interval[0]=Decimal("0")
					interval[1]=Decimal("1")
				break
	if (interval!=[0, 1]):
		write(encoded, interval)










#вызовы 
getcontext().prec=38
# p=input("Введите путь файла для кодировки: ")
p='c:\\users\\user\\desktop\\text.txt'

freq=count_freq(p)
node_list=make_list(freq)

encoding(p, node_list)

a=os.stat(p).st_size
b=os.stat(p[:-4]+'(encoded).txt').st_size
print('Сжатие %f%%' %(b/a*100))

