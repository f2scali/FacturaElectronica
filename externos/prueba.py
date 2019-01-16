#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
from daemon import runner
import socket
import sys
import argparse
import signal

import subprocess, os
import shutil
import pwd
import grp


class porcesarGS():
	"""docstring for porcesarGS"""
	def __init__(self, archivo="/tmp/formatos.ps"):
		self.archivo = archivo

	def Procesar(self):
		logger.info('Procesando GS')
		uid = pwd.getpwnam("www-data").pw_uid
		gid = grp.getgrnam("www-data").gr_gid

		comando="gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -o /tmp/formatos%0d.pdf /tmp/formatos.ps"
		logger.info('Comando:{}'.format(comando))
		gsProc=subprocess.Popen(comando.split(),stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		error=gsProc.communicate()[0]
		logger.info(error)

		for i in range(1,3):
			if os.path.isfile('/tmp/formatos{}.pdf'.format(i)):
				os.chown("/tmp/formatos{}.pdf".format(i), uid, gid)
			else:
				logger.error('No existe /tmp/formatos{}.pdf'.format(i))

		comando="gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=ljet4 -o /tmp/formatos%0d.pcl /tmp/formatos.ps"
		logger.info('Comando:{}'.format(comando))
		gsProc=subprocess.Popen(comando.split(),stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		error=gsProc.communicate()[0]
		logger.info(error)

		for i in range(1,3):
			if os.path.isfile('/tmp/formatos{}.pcl'.format(i)):
				entr=open('/tmp/formatos{}.pcl'.format(i),"rb")
				entr.seek(57)
				datos=entr.read()[:-1]
				entr.close()
				if i==1:
					arch=open("/tmp/Extracto_frente.pdf.pcl","wb")
					arch.write("&f1000y0X")
				else:
					arch=open("/tmp/Extracto_atras.pdf.pcl","wb")
					arch.write("&f1001y0X")
				arch.write(datos)
				arch.write('*p0Y&f1x10X')
				arch.close()

				if i==1:
					os.chown("/tmp/Extracto_frente.pdf.pcl", uid, gid)
					os.chown("/tmp/formatos1.pdf", uid, gid)
					os.rename("/tmp/formatos1.pdf","/home/www-data/web2py/applications/Extractos/static/formularios/Extracto_frente.pdf")
					os.rename("/tmp/Extracto_frente.pdf.pcl","/home/www-data/web2py/applications/Extractos/static/formularios/Extracto_frente.pdf.pcl")
				else:
					os.chown("/tmp/Extracto_atras.pdf.pcl", uid, gid)
					os.chown("/tmp/formatos2.pdf", uid, gid)
					os.rename("/tmp/formatos2.pdf","/home/www-data/web2py/applications/Extractos/static/formularios/Extracto_atras.pdf")
					os.rename("/tmp/Extracto_atras.pdf.pcl","/home/www-data/web2py/applications/Extractos/static/formularios/Extracto_atras.pdf.pcl")

				logger.info('Raidcados..')
			else:
				logger.error('No existe /tmp/formatos{}.pcl'.format(i))

class App():
	def __init__(self):
		self.stdin_path      = '/dev/null'
		self.stdout_path     = '/dev/tty'
		self.stderr_path     = '/dev/tty'
		self.pidfile_path    =  '/var/run/Recibeprint.pid'
		self.pidfile_timeout = 5

	def run(self):
		logger.info('Arranque.. Inciando puerto')
		HOST = "localhost"
		PORT = 9999
		s = None
		for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
			af, socktype, proto, canonname, sa = res
			try:
				s = socket.socket(af, socktype, proto)
			except socket.error, msg:
				s = None
				logger.error(msg)
				continue
			try:
				s.bind(sa)
				s.listen(1)
			except socket.error, msg:
				s.close()
				s = None
				logger.error(msg)
				continue
			break
		if s is None:
			logger.error('No puede abrir socket')
			sys.exit(1)
		logger.info("Inciando en {}:{}".format(HOST,PORT))
		while 1:
			conn, addr = s.accept()
			logger.info("Conectador por {}".format(addr))
			f = open('/tmp/formatos.ps', 'w')
			logger.info("Recibe impresion")
			while 1:
				data = conn.recv(1024)
				f.write(data)
				if not data: break
				#conn.send(data)
			logger.info("Fin de la impresion")
			f.close()
			conn.close()
			gs=porcesarGS()
			gs.Procesar()
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
