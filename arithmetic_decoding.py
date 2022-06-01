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





def decode(name_code):
	try:
		decoded=open(name_code[:-13]+"(decoded).txt", "w")
		code=open(name_code, "rb")
	except:
		print("Указанный файл не может быть открыт")
		input("Нажимте Enter для закрытия консоли")
		exit()
	num_of_sym=int(code.read(1))
	freq=[0 for i in range(256)]
	sym=code.read(1)
	sym=sym.decode("ascii")
	str1=''
	node_list=[]
	while ord(sym)!=2:
		sym=code.read(1)
		char=sym.decode("ascii")
		sym=code.read(1)
		sym=sym.decode("ascii")
		while ord(sym)!=1 or ord(sym)!=1:
			str1+=sym
			sym=code.read(1)
			print(sym)
			sym=sym.decode("ascii")

		node_list.append(Node(char, float(str1)))
		str1=''







p=input("Введите путь файла для декодировки: ")

decode(p)

# orig=input("Введите путь оригинального файла: ")