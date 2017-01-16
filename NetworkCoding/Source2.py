import binascii
import base64
from socket import *
#########################################
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
####################################################
# Set the socket parameters
host1 = "127.0.0.1"
port1 = 21577
buf = 2048
addr1 = (host1, port1)
host2 = "127.0.0.1"
port2 = 21576
addr2 = (host2, port2)
# Create socket
UDPSock = socket(AF_INET,SOCK_DGRAM)
# Send messages
data1list = []
data1 = ''
fo = open("source2Data.txt", "r+")
data1 = fo.read()
# "Read String is : ", str
# Close opend file
fo.close()

data1list = StringToBinaryList(data1)
if data1:
	if(UDPSock.sendto(data1, addr1)):
		print "\n\nSending message to Inter_1 : \n\n '",data1,"'"
	if(UDPSock.sendto(data1, addr2)):
		print "\n\nSending message to Dest_2 : \n\n'",data1,"'"

# Close socket
UDPSock.close()


