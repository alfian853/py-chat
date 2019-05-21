import sys
import os.path
import uuid
from glob import glob
from datetime import datetime

class HttpServer:
	def __init__(self):
		self.sessions={}
		self.types={}
		self.types['.pdf']='application/pdf'
		self.types['.jpg']='image/jpeg'
		self.types['.txt']='text/plain'
		self.types['.html']='text/html'
	def response(self,kode=404,message='Not Found',messagebody='',headers={}):
		tanggal = datetime.now().strftime('%c')
		resp=[]
		resp.append("HTTP/1.0 {} {}\r\n" . format(kode,message))
		resp.append("Date: {}\r\n" . format(tanggal))
		resp.append("Connection: close\r\n")
		resp.append("Server: myserver/1.0\r\n")
		for kk in headers:
			resp.append("{}:{}\r\n" . format(kk,headers[kk]))
		resp.append("\r\n")
		resp.append("{}" . format(messagebody))
		response_str=''
		for i in resp:	
			response_str="{}{}" . format(response_str,i)
		return response_str

	def proses(self,data):
		requests = data.split("\r\n")
		baris = requests[0]
		print baris
		j = baris.split(" ")
		try:
			method=j[0].upper().strip()
			if (method=='GET'):
				object_address = j[1].strip()
				return self.http_do(object_address)
			elif(method=='HEAD'):
				object_address = j[1].strip()
				return self.http_head(object_address)
			elif(method=='POST'):
				object_address = '/'+requests[14]
				return self.http_do(object_address)
			elif(method=='OPTIONS'):
				object_address = j[1].strip()
				return self.http_options(object_address)
			else:
				return self.response(400,'Bad Request','',{})
		except IndexError:
			return self.response(400,'Bad Request','',{})

	def http_head(self, object_address):
		files = glob('./*')
		thedir='.'
		if thedir+object_address not in files:
			return self.response(404,'Not Found','',{})
		fp = open(thedir+object_address,'r')
		isi = fp.read()
		
		fext = os.path.splitext(thedir+object_address)[1]
		content_type = self.types[fext]
		
		headers={}
		headers['Content-type']=content_type
		headers['Content-length'] = len(isi)
		return self.response(200,'OK','',headers)

	def http_options(self, object_address):
		files = glob('./*')
		thedir='.'
		if thedir+object_address not in files:
			return self.response(404,'Not Found','',{})
		fp = open(thedir+object_address,'r')
		con = fp.read()
		
		fext = os.path.splitext(thedir+object_address)[1]
		content_type = self.types[fext]
		
		headers={}
		headers['Allow'] = "GET, POST, HEAD, OPTIONS"
		headers['Content-type']=content_type
		headers['Content-length'] = len(con)
		return self.response(200, 'OK','', headers)


	def http_do(self,object_address):
		files = glob('./*')
		thedir='.'
		if thedir+object_address not in files:
			return self.response(404,'Not Found','',{})
		fp = open(thedir+object_address,'r')
		isi = fp.read()
		
		fext = os.path.splitext(thedir+object_address)[1]
		content_type = self.types[fext]
		
		headers={}
		headers['Content-type']=content_type
		headers['Content-length'] = len(isi)

		return self.response(200,'OK',isi,headers)
		
			 	
#>>> import os.path
#>>> ext = os.path.splitext('/ak/52.png')

if __name__=="__main__":
	httpserver = HttpServer()
	#d = httpserver.proses('GET testing.txt HTTP/1.0')
	#print d
    #    d = httpserver.http_get('testing2.txt')
	#print d
	#d = httpserver.http_get('/testing.txt')
	#print d
