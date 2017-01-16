import binascii
from socket import *
data1 = ''
data2 = ''
 ################################################
def ByteToHex( byteStr ):
    return ' '.join( [ "%02X" % ord( x ) for x in byteStr ] )

def byte_to_binary(n):
    return ''.join(str((n & (1 << i)) and 1) for i in reversed(range(8)))
def hex_to_binary(h):
    return ''.join(byte_to_binary(ord(b)) for b in binascii.unhexlify(h))

def StringToBinaryList(astring):
	ibinarylist = []
	Valueinbits = ''
	for x in astring:
		#print x
		if x:
			hexValue = ByteToHex(x)
			binValue = hex_to_binary(hexValue)
			#print x + ' equivalent binary value ' + binValue
			if binValue == '1010':
				#print '1010: end of file'
				ibinarylist.append(binValue)
				Valueinbits += binValue
			else:
				ibinarylist.append(binValue)
				Valueinbits += binValue
	return ibinarylist
#####################################################
def stringToInteger(astring):
	listOfinteger = []
	for c in astring[0:len(astring)]:
		p = int(c)
		listOfinteger.append(p)
	return listOfinteger
def ListOfCharToListofString(alist):
	Integerlist = []
	for x in alist:
		p = stringToInteger(x)
		Integerlist.append(p)
	return Integerlist
#####################################################
def XOROperation(a, b):
	return a ^ b
def EnodeDatabits(p, q):
	c_data = []
	len1 = len(p)
	len2 = len(q)
	i = 0
	if len1 == len2:
		#print	'Both data contain equal bits'
		for x in p:
  			xor_res = XOROperation(x, q[i])
			c_data.append(xor_res)
			i = i + 1
	elif len1 > len2:
		print ''
	elif len2 > len1:
		print ''
	return c_data
def ListAfterXOREncode(lis1, lis2):
	Integerlist1 = []
	Integerlist2 = []
	xorIntegerlist = []
	# Initially coded_data is empty.
	coded_data = []
	listOfCodedData = []
	i = 0
	for x in lis1:
		p = stringToInteger(x)
		Integerlist1.append(p)
	for x in lis2:
		p = stringToInteger(x)
		Integerlist2.append(p)
	print 'Network Coding started: Performing XOR operations on bits...'
	for x in Integerlist1:
		data1 = x
		data2 = Integerlist2[i]
		i = i + 1
		coded_data = EnodeDatabits(data1, data2)
		listOfCodedData.append(coded_data)
	print 'End of Encoding!'
	return listOfCodedData
#####################################################
def IntegerToString(aint):
	listOfStr = []
	for c in aint[0:len(aint)]:
		p = str(c)
		listOfStr.append(p)
	return listOfStr
def ListOfStringToListofChar(alist):
	Charlist = []
	for x in alist:
		p = IntegerToString(x)
		string = ''
		for y in p:
			string += str(y)
		Charlist.append(string)
	return Charlist
def ListOfCharToListOfBinary(alist):
	p = []
	for x in alist:
		c = int(x)
		p.append(c)
	return p
def ListOfBinaryToListOfHex(alist):
	p = []
	for x in alist:
		c = int(x, 2)
		z = hex(c)
		p.append(z)
	return p
def ListOfBinaryToListOfChar(alist):
	p = []
	for x in alist:
		c = int(x, 2)
		z = hex(c)
		integer = int(z, 16)
		char = chr(integer)
		p.append(char)
	#print p
	return p
def BackToString(alist):
	decoded_1 =  ListOfStringToListofChar(alist)
	#print 'List of string decoded:'
	#print decoded_1
	#print 'Converting it into binary value'
	binarylist =  ListOfCharToListOfBinary(decoded_1)
	#print binarylist
	#print 'Converting binary value to hex value'
	hexlist = ListOfBinaryToListOfHex(decoded_1)
	# hexlist
	#print 'Converting to data'
	dataq = ListOfBinaryToListOfChar(decoded_1)
	#print dataq
	#print StringToBinaryList(dataq)
	#print 'done'
	return dataq
###############################
def ConcatListElements(alist):
	p = ''
	for x in alist:
		p += x
	return p
################################
# Set the socket parameters
host1 = "127.0.0.1"
port1 = 21578
buf1 = 992048
addr1 = (host1,port1)
# Create socket and bind to address
UDPSock = socket(AF_INET,SOCK_DGRAM)
UDPSock.bind(addr1)
# Receive messages
while 1:
	data,addr1 = UDPSock.recvfrom(buf1)
	if not data:
		print "Client has exited!"
		break
	else:
		print "\nReceived message from Source_1 is :\n'", data,"'"
		data1 = data
		ibinarylist1 = StringToBinaryList(data1)
		#print ibinarylist1
		print ''
		# Set the socket parameters
		host2 = "127.0.0.1"
		port2 = 21577
		buf2 = 992048
		addr2 = (host2, port2)
		# Create socket and bind to address
		UDPSock2 = socket(AF_INET, SOCK_DGRAM)
		UDPSock2.bind(addr2)
		# Receive messages
		while 1:
			data2, addr2 = UDPSock2.recvfrom(buf2)
			if not data2:
				print "Client has exited!"
				break
			else:
				print "\nReceived message from Source_2 is :\n'", data2,"'"
				dataB = data2
				ibinarylist2 = StringToBinaryList(dataB)
				#print ibinarylist2
				print ''
				break
		#Close socket
		UDPSock2.close()
		# Perform Network Coding
		first = ListOfCharToListofString(ibinarylist1)
		second = ListOfCharToListofString(ibinarylist2)
		listOfCodedData = ListAfterXOREncode(ibinarylist1, ibinarylist2)
		#print coded data
		#print 'Coded Data: '
		#print listOfCodedData

		backstring = BackToString(listOfCodedData)
		#print 'binary'
		binary = StringToBinaryList(backstring)
		backstringconcat = ConcatListElements(backstring)

		# Set the socket parameters
		host3 = "127.0.0.1"
		port3 = 21580
		buf = 992048
		addr3 = (host3, port3)
		# Create socket
		UDPSock3 = socket(AF_INET,SOCK_DGRAM)

		# Send messages
		if not backstringconcat:
			break
		else:
			if(UDPSock3.sendto(backstringconcat, addr3)):
				print "Message has being sent to Inter_2... "
		UDPSock3.close()
# Close socket
UDPSock.close()