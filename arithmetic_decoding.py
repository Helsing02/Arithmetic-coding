class Node:
	def __init__(self, char, num_in_text, freq=0, low=0, high=0):
		self.char=char
		self.num_in_text=num_in_text
		self.freq=freq
		self.low=low
		self.high=high
	def __repr__(self):
		return repr((self.char, self.freq, self.low, self.high))
	def __str__(self):
		return str(self.char)+" "+str(self.freq)+' '+str(self.low)+' '+str(self.high)
	def new_lr(self, interval):
		interval[0], interval[1]=interval[0]+(interval[1]-interval[0])*self.low, interval[0]+(interval[1]-interval[0])*self.high 






def decode(name_code):
	try:
		decoded=open(name_code[:-13]+"(decoded).txt", "w")
		code=open(name_code, "rb")
	except:
		print("Указанный файл не может быть открыт")
		input("Нажимте Enter для закрытия консоли")
		exit()

	str1=''
	sym=code.read(1)
	sym=sym.decode("ascii")
	while ord(sym)!=1:
		str1+=sym
		sym=code.read(1)
		sym=sym.decode("ascii")
	end_message=int(str1)
	while ord(sym)==1:
		sym=code.read(1)
		sym=sym.decode("ascii")

	str1=''
	while ord(sym)!=1:
		str1+=sym
		sym=code.read(1)
		sym=sym.decode("ascii")
	num_of_sym=int(str1)

	str1=''
	node_list=[]
	len_of_mess=0
	while ord(sym)!=2:
		sym=code.read(1)
		char=sym.decode("ascii")
		# print(char)
		sym=code.read(1)
		sym=sym.decode("ascii")
		str1=''
		while ord(sym)!=1 and ord(sym)!=2:
			str1+=sym
			sym=code.read(1)
			sym=sym.decode("ascii")
		# print(str1)
		node_list.append(Node(char, int(str1)))
		len_of_mess+=int(str1)
	collect=0
	for i in node_list:
		i.low=collect/len_of_mess
		collect+=i.num_in_text
		i.high=collect/len_of_mess

	
	sym=code.read(1)
	integer=int.from_bytes(sym, "big")
	num=0
	while True:
		bits=0
		for i in range(4):
			bits=bits<<8
			bits=bits|integer
			sym=code.read(1)
			integer=int.from_bytes(sym, "big")
		mask=1<<31
		num=0
		for i in range(32):
			if (bits&mask)!=0:
				num+=1/2**(i+1)
			mask=mask>>1
		# print ("num ", num)
		for i in range(num_of_sym):
			for j in node_list:
				if j.low<=num and j.high>num:
					decoded.write(j.char)
					len_of_mess-=1
					if len_of_mess==0:
						return
					num=(num-j.low)/(j.high-j.low)
					# print(num, i, num_of_sym)
					break










p=input("Введите путь файла для декодировки: ")

decode(p)

# orig=input("Введите путь оригинального файла: ")