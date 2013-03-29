#!/usr/bin/env python
#-*- coding:utf-8 -*-

import struct
from cStringIO import StringIO
from urllib import FancyURLopener
import socket

def packExt(fmt, *args):
	if fmt.find("z") < 0:
		# normal pack
		return struct.pack(fmt, *args)
	else:
		# should contain zero terminated string
		argcounter = 0
		format_buffer = ""
		result=""
		for i in xrange(0, len(fmt)):
			if fmt[i] not in ['x','c','b','B','h','H','i','I','l','L','q','Q','f','d','s','p','P','z']:
				format_buffer += fmt[i]
				continue
				
			if fmt[i] == 'z':
				zeropos = args[argcounter].find('\0')
				arg = args[argcounter]
				if zeropos < 0:
					# add after end
					nfmt = '%ds'%(len(args[argcounter])+1)
					arg += '\0'
				else:
					nfmt = '%ds'%(zeropos+1)
				result += struct.pack(nfmt, str(arg))
				argcounter += 1
			else:
				#control character!
				format_buffer += fmt[i]
				#print format_buffer, "->", args[argcounter]
				result += struct.pack(format_buffer, args[argcounter])
				argcounter += 1
			format_buffer=""
		return result

def unpackExt(fmt, string):
	if fmt.find("z") < 0:
		# normal unpack
		return struct.unpack(fmt, string)
	else:
		# contains zero terminated string
		offset = 0
		result = []
		format_buffer = ""
		for i in xrange(0, len(fmt)):
			if fmt[i] == 'z':
				#process buffer
				size = 0
				if len(format_buffer) > 0:
					size = struct.calcsize(format_buffer)
					result_this = struct.unpack_from(format_buffer, string, offset)
					offset += size
					#print " '%s, %s' => "%(format_buffer, size), result_this
					result += result_this
					format_buffer = ""
				
				# now the z part
				file_str = StringIO()
				strsize = -1
				for j in xrange(0, len(string)):
					if offset+j < len(string):
					  if string[offset+j] == '\0':
					    strsize=j;
					    break;
					  else:
					    file_str.write(string[offset+j]);
					
				result += [file_str.getvalue()]
				offset += strsize + 1 # 1 = \0
			else:
				# cache all chars for later processing
				format_buffer += fmt[i]
			
		#process last buffer
		size = struct.calcsize(format_buffer)
		result_this = struct.unpack_from(format_buffer, string, offset)
		#print " '%s' => "%format_buffer, result_this
		result += result_this
		format_buffer = ""
			
		return result

#if __name__ == '__main__':
#	print unpackExt("z", packExt("z", "test1"))
#	print unpackExt("z", packExt("z", "test1 test2"))
#	print unpackExt("z", packExt("z", "test1\0test2"))
#	print unpackExt("ibzi", packExt("ibzi", 200, 3, "test1\0test2", 34))
#	print unpackExt("ibzizf", packExt("ibzizf", 200, 3, "test1\0test2", 34, "test string", 0.234))


def Serverlist():
   class HQopener(FancyURLopener):
      version = 'HQNotify.py'
   hqopener = HQopener()
   f = hqopener.open("http://www.kitana.org/cgi-bin/playground/hqo/hqoms.exe?serverlist")
   string=f.read()
   while string != "":
      yield '.'.join([str(x) for x in bytearray(string[0:4])])
      string = string[4:len(string)]
   #print struct.unpack('BBBB', string[4:8])
#print list(Serverlist())

def Send(IP, data):
   s = socket.socket()
   s.connect((IP, 5880))
   #print "Send: ", list(bytearray(data))
   print "Send: ", repr(data)
   s.sendall(data)
   data = s.recv(1024)
   print "Recv: ", repr(data)
   s.close()
   return data

if __name__ == "__main__":
   print "Ich liebe DICH mein Kuschelinchen"
   for i in Serverlist():
      print "--", i, "--"
      ret=Send(i, struct.pack('8s', 'LCHN'))
      if ret[0:4]!='CHNS':
         print "error"
      else:
         Chan, maxChan = struct.unpack("BB", ret[8:10])
         print "Channel: ", Chan, "Max: ", maxChan
         Channel = unpackExt("BBz"*Chan, ret[10:])
         print "%8s | %4s | %s" % ("Spieler", "SL", "Name")
         for AktualChan in xrange(0, Chan):
            print "%8s | %4s | %s" % (Channel[AktualChan*3+0], Channel[AktualChan*3+1], Channel[AktualChan*3+2].decode('iso8859_15'))
         
