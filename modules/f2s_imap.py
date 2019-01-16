# -*- coding: utf-8 -*-
'''
Creado por:SimpleSoft.com

Lee el correo y descarga solo los xml y pdf de un correo

Parametros:
===========
ruta	: Definir la carpeta de salida para ser guardos los archivos pdf, xml 
servidor: ip o nombre del servidor de correo ejemplo:imap.gmail.com
puerto	: puerto e conexcion ejemplo: 993
login	: Usuario de conexcion ejemplo: facturascali2018@gmail.com
password: Clave de ingreso: Tetero.2018
bandeja	: Bnadeja de ingrso del correo ejemplo :inbox

Propiedades:
============
docXML	: Ruta y nombre del archivo XML
docpdf	: Ruta y nombre del archivo PDF
gW6ZO
I'''
class ObjImap():
	"""docstring for ObjImap"""
	def __init__(self, ruta, servidor='imap.gmail.com', puerto=993, login='facturascali2018@gmail.com', password='Tetero.2018',bandeja="inbox",debug=False):
		if debug:print ("ObjImap Start")
		self.servidor=servidor
		self.puerto=puerto
		self.login=login
		self.password=password
		self.bandeja=bandeja
		self.ruta=ruta
		self.docXML=""
		self.docpdf=""
		self.debug=debug

	def Procesar(self):
		import imaplib
		import os
		import email
		mail = imaplib.IMAP4_SSL(self.servidor,self.puerto)
		mail.login(self.login, self.password)
		mail.list()
		mail.select(self.bandeja) # connect to inbox.
		result, data = mail.uid('search', None,'UNSEEN') # search and return uids instead
		if len(data[0])==0:
			if self.debug: print ("No hay Correos..")
			return False
		latest_email_uid = data[0].split()[-1]
		if self.debug: print (latest_email_uid)
		result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
		if self.debug: print "result:",result
		if result:#.upcase()=="OK":
			for response_part in data:
				if isinstance(response_part, tuple):
					msg = email.message_from_string(response_part[1])
					if msg.is_multipart():
						if self.debug: print ("is_multipart")
						for part in msg.walk():
							#if part.get_content_type() in ("text/plain",   "text/html"):
								#print "Text/Pain" "*" 
								#print(part.get_payload(decode = True))
							if part.get_content_type() in("text/xml"):
								if self.debug: print ("xml")
								payload = part.get_payload(decode=True)
								# Default filename can be passed as an argument to get_filename()
								filename = part.get_filename()
								# Save the file.
								if self.debug: print (filename)
								if payload and filename:
									f=open(os.path.join(self.ruta, filename), 'wb')
									f.write(payload)
									f.close()
									self.docXML=filename

							elif part.get_content_type() == 'application/pdf':
								if self.debug: print ("PDF ****")
								# When decode=True, get_payload will return None if part.is_multipart()
								# and the decoded content otherwise.
								payload = part.get_payload(decode=True)

								# Default filename can be passed as an argument to get_filename()
								filename = part.get_filename()
								if self.debug: print (filename)
								# Save the file.
								if payload and filename:
									f=open(os.path.join(self.ruta,filename), 'wb')
									f.write(payload)
									f.close()
									self.docpdf=filename
					else:
						if self.debug:
							print ("no is_multipart" )
							print(part.get_payload(decode = True))
						pass
		mail.logout()
		if self.debug: 
			print self.docXML
			print self.docpdf

		return True




