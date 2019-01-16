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
		if debug:print ("ObjImap Start-->",ruta)
		self.servidor=servidor
		self.puerto=puerto
		self.login=login
		self.password=password
		self.bandeja=bandeja
		self.ruta=ruta
		self.docXML={}
		self.docpdf={}
		self.debug=debug

	def Procesar(self):
		import imaplib
		import os
		import email
		try:
			if self.debug:print ("{}:{}".format(self.servidor,self.puerto))
			connection = imaplib.IMAP4_SSL(self.servidor,self.puerto)
			if self.debug:print ("{}:{}".format(self.login,self.password))
			reporte = connection.login(self.login, self.password)
		except Exception as e:
			return "{}".format(e)
		verificar=connection.select(self.bandeja) # connect to inbox.
		if verificar[0]!="OK":
			return "{}-{}".format(verificar[0],verificar[0])
		result, data = connection.uid('search', None,'UNSEEN') # search and return uids instead
		for uid in data[0].split():
			if self.debug:print ("{}:{}".format(self.login,self.password))

			status,data=connection.fetch(uid,'(RFC822)')
			body=data[0][1]
			dbody=body.decode()
			mail=email.message_from_string(dbody)
			if self.debug:print ("revisar datos")
			for registro in mail.walk():
				archivo=registro.get_filename()
				if self.debug:print (archivo)
				arch_salida=None
				if archivo:   
					if archivo[-3:].lower()=="pdf":
						arch_salida =os.path.join(self.ruta,archivo)
						self.docpdf[archivo[:-4]]=arch_salida
						
					elif archivo[-3:].lower()=="xml":
						arch_salida =os.path.join(self.ruta,archivo)
						self.docXML[archivo[:-4]]=arch_salida

					if arch_salida:
						if self.debug:print ("Ruta de salida:{}".format(arch_salida))
						fp=open(arch_salida, 'wb')
						fp.write(registro.get_payload(decode=True))
						fp.close()
		return "OK"
		connection.close()

