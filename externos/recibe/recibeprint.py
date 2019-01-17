#!/usr/bin/env python
'''
Recepcion de archivos desde un socker y enviado a Web2py,
El web2py esta en Docker y se debe enviar el llamado 
'''
import socket
import sys
import tempfile
import urllib2
import os
import ConfigParser
import logging
import time
from daemon import runner

def Configuracion():
	'''Lectura e la configuracion'''
	salida ={}
	ruta =os.path.join('/etc/facil','configurar.conf')
	logger.info("configurar:{}".format(ruta))
	if os.path.exists(ruta):
		configurar=ConfigParser.ConfigParser()
		try:
			#os.write(2,"leer")
			configurar.read(ruta)
			salida["ruta"]=configurar.get ('printsocker','ruta')
			salida["rutavirtual"]=configurar.get ('printsocker','rutavirtual')
			salida["puerto"]=configurar.get ('printsocker','puerto')
			salida["host"]=configurar.get ('printsocker','host')
			salida["app"]=configurar.get ('printsocker','app')
			salida["hostweb"]=configurar.get ('printsocker','hostweb')
			logger.info("leer{}".format(salida))
			if not os.path.isdir(salida['ruta']):
				os.makedirs(salida[ruta])

		except Exception as e:
			logger.info("Error en config {}".format(e))
			salida =None

	logger.info("configuracion:{}".format(salida))
	return salida

class App():
	def __init__(self):
		self.stdin_path      = '/dev/null'
		self.stdout_path     = '/dev/tty'
		self.stderr_path     = '/dev/tty'
		self.pidfile_path    =  '/var/run/Recibeprint.pid'
		self.pidfile_timeout = 5

	def run(self):
		logger.info('Arranque.. lectura Configuracion')
		conf=Configuracion()
		if conf==None:
			logger.error("No hay configuracion")
			sys.exit(1)

		s = None
		for res in socket.getaddrinfo(conf['host'], conf['puerto'], socket.AF_UNSPEC,socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
			af, socktype, proto, canonname, sa = res
			try:
				s = socket.socket(af, socktype, proto)
			except socket.error, msg:
				s = None
				continue
			try:
				s.bind(sa)
				s.listen(1)
			except socket.error, msg:
				s.close()
				s = None
				continue
			break
		if s is None:
			logger.error('No puede abrir puerto {}\n'.format(conf['puerto']))
			sys.exit(1)

		logger.info("Escuchando por el puerto [{}]:....".format(conf['puerto']))

		while 1:
			arch_entrada = tempfile.NamedTemporaryFile(prefix="F2S-", delete=False,dir=conf['ruta'])
			conn, addr = s.accept()
			logger.info('Archivo       :{}'.format(arch_entrada.name))
			logger.info ('Conectador por:{}'.format(addr))
			logger.info("Recibe impresion.------------------------------>>>")
			while 1:
				data = conn.recv(1024)
				arch_entrada.write(data)
				if not data: break
				#conn.send(data)
			arch_entrada.close()
			conn.close()
			logger.info("--------------------------------<<<< Fin Impresion")
			nombre_arch=os.path.split(arch_entrada.name)[-1]
			salida =os.path.join(conf ['rutavirtual'],nombre_arch)
			logger.info("Virutal:{}".format(salida))
			logger.info("App    :{}".format(conf['app']))
			logger.info("hostweb:{}".format(conf['hostweb']))

			rutaurl="{}/{}/subirimpresion/index.html?archivo={}".format(conf['hostweb'],conf['app'],salida)
			logger.info("rutaurl:{}".format(rutaurl))
			try:
				req=urllib2.urlopen(rutaurl)
				logger.info (req.read())
			except Exception as e:
				logger.error("{}".format (e))
		time.sleep(1)

if __name__=='__main__':
	app=App()
	logger = logging.getLogger("testlog")
	logger.setLevel(logging.INFO)
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
	handler = logging.FileHandler("/var/log/RecibePrint.log")
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	serv = runner.DaemonRunner(app)
	serv.daemon_context.files_preserve=[handler.stream]
	serv.do_action()