class Node:
	def __init__(self, char, freq, low=0, high=0):
		self.char=char
		self.freq=freq
		self.low=low
		self.high=high
	def __repr__(self):
		return repr((self.char, self.freq, self.low, self.high))
	def __str__(self):
		return str(self.char)+" "+str(self.freq)
	def is_belong(self, val, left, right):
		High=left+(right-left)*self.high 
		Low=left+(right-left)*self.low 
		return val<High and val>=Low
	def new_lr(self, interval):
		interval[1]=interval[0]+(interval[1]-interval[0])*self.high 
		interval[0]=interval[0]+(interval[1]-interval[0])*self.low
		


def proc(curr, interval):
	if interval[0]<=curr and interval[1]>curr:
		return -1
	if interval[0]<=curr:
		return 0
	return 1

def write(fileadr, interval):
	cont=0
	bits=0
	for i in range(1, 33):
		bits=bits<<1
		# print("write ", interval, cont+1/(2**i))
		if proc(cont+1/(2**i), interval)==-1:
			bits=bits|1
			bits=bits<<(32-i)
			for j in range(3, -1, -1):
				new_i=bits>>8*j
				fileadr.write(bytes([new_i&255]))
				# print(bytes([new_i&255]))
			break
		# print(cont+1/(2**i))
		if proc(cont+1/(2**i), interval)==1:
			bits=bits|1
			cont+=1/(2**i)
	interval[0]=0
	interval[1]=1


def count_freq(name):
	count=0
	freq=[0 for i in range(256)]
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
	for i in range(256):
		freq[i]/=count
	return freq

def make_list(freq):
	node_list=[]
	for i in range(256):
		if freq[i]!=0:
			node_list.append(Node(chr(i), freq[i]))
	node_list=sorted(node_list, key=lambda i: i.freq, reverse=True)
	collect=0
	for i in node_list:
		i.low=collect
		collect+=i.freq
		i.high=collect
	print(node_list)
	return node_list

def encoding(name, node_list):
	num_of_sym=5

	try:
		to_encode=open(name, "r")
		encoded=open(name[:-4]+"(encoded).txt", 'wb')
	except:
		print("Указанный файл не может быть открыт")
		input("Нажимте Enter для закрытия консоли")
		exit()
	encoded.write(" ".encode("ascii"))
	for i in range (128):
		if (freq[i]!=0):
			encoded.write(('\x01'+chr(i)+str(freq[i])).encode("ascii"))
	encoded.write("\x02".encode("ascii"))

	curr_num=0
	interval=[0, 1]
	val=0
	sym=to_encode.read(1)
	while True:
		for i in node_list:
			if i.char==sym:
				i.new_lr(interval)
				curr_num+=1
				break
		if curr_num==num_of_sym or sym=='':
			if curr_num!=0:
				write(encoded, interval)
			curr_num=0
			if sym=='':
				break
		sym=to_encode.read(1)











#вызовы 
p=input("Введите путь файла для кодировки: ")

freq=count_freq(p)
node_list=make_list(freq)
encoding(p, node_list)

