import filecmp
from decimal import Decimal, getcontext
class Node:
    def __init__(self, char, num_in_text, freq='0', low='0', high='0'):
        self.char=char
        self.num_in_text=num_in_text
        self.freq=Decimal(freq)
        self.low=Decimal(low)
        self.high=Decimal(high)
    def __repr__(self):
        return repr((self.char, self.freq, self.low, self.high))
    def __str__(self):
        return str(self.char)+' '+str(self.freq)+' '+str(self.low)+' '+str(self.high)
    def new_lr(self, interval):
        interval[0], interval[1]=interval[0]+(interval[1]-interval[0])*self.low, interval[0]+(interval[1]-interval[0])*self.high 



def decode(name_code):
    try:
        decoded_file=open(name_code[:-13]+'(decoded).txt', 'w')
        encoded_file=open(name_code, 'rb')
    except:
        print('Указанный файл не может быть открыт')
        input('Нажимте Enter для закрытия консоли')
        exit()

    # Making node_list
    str1=''
    node_list=[]
    len_of_mess=0
    sym='a'
    while True:
        sym=encoded_file.read(1)
        char=sym.decode('ascii')
        if ord(char)==2:
            break
        sym=encoded_file.read(1)
        sym=sym.decode('ascii')
        str1=''
        while ord(sym)!=1 and ord(sym)!=2:
            str1+=sym
            sym=encoded_file.read(1)
            sym=sym.decode('ascii')
        node_list.append(Node(char, int(str1)))
        len_of_mess+=int(str1)
    to_sym=Decimal('0')
    for i in node_list:
        i.low=to_sym/len_of_mess
        to_sym+=i.num_in_text
        i.high=to_sym/len_of_mess

    # Decoding
    sym=encoded_file.read(1)
    byte=int.from_bytes(sym, 'big')
    num=Decimal('0')
    differ=Decimal('1')
    while True:
        bits=0
        for i in range(4):
            bits<<=8
            bits|=byte
            sym=encoded_file.read(1)
            byte=int.from_bytes(sym, 'big')
        mask=1<<31
        num=Decimal('0')
        for i in range(32):
            if (bits&mask)!=0:
                num+=Decimal('1')/2**(i+1)
            mask>>=1
        differ=Decimal('1')
        flagBrake=False
        while flagBrake is False:
            for j in node_list:
                if j.low<=num and j.high>num:
                    if differ*(j.high-j.low)>Decimal('1')/2**32:
                        differ=differ*(j.high-j.low)
                        decoded_file.write(j.char)
                        len_of_mess-=1
                        if len_of_mess==0:
                            return
                        num=(num-j.low)/(j.high-j.low)
                    else:
                        flagBrake=True
                    break

    decoded_file.close()
    encoded_file.close()



def cmp(name, orig):
    if filecmp.cmp(name, orig):
        print('Идентичны')
    else:
        print('Неидентичны')
        f1=open(orig, 'r')
        f2=open(name, 'r')

        sym1=f1.read(1)
        sym2=f2.read(1)
        count=1
        while sym1!='' or sym2!='':
            if sym1!=sym2:
                print (sym1, sym2, 'false', count)
            else:
                print(sym1, sym2)
            count+=1
            sym1=f1.read(1)
            sym2=f2.read(1)
        f1.close()
        f2.close()




getcontext().prec=38

# p=input('Введите путь файла для декодировки: ')
p='c:\\users\\user\\desktop\\text(encoded).txt'

decode(p)

# orig=input('Введите путь оригинального файла: ')
orig='c:\\users\\user\\desktop\\text.txt'

cmp(p[:-13]+'(decoded).txt', orig)

