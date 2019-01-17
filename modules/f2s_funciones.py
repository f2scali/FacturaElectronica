#!/usr/bin/env python
# -*- coding: utf-8 -*-
def prueba():
	import os
	archivo="/home/www-data/imagenes/frmFactura.pdf"
	stream=open(archivo,"rb")
	db.tbl_factelectronica.arch_pdf.uploadfolder=os.path.join(request.folder,"uploads","2018")
	db.tbl_factelectronica.insert(arch_pdf=db.tbl_factelectronica.arch_pdf.store(stream, archivo))
	return os.path.join(request.folder,"uploads","2018")

def ExtraerQR(arch_imagen,x=779,y=20,x1=896,y1=131):
	'''
	Recorta la imagen en (x,y,x1,y1)
	Extrae el contenido del qr
	Retorna el contenido del qr
	'''
	print ("ExtraerQR.")
	from pyzbar.pyzbar import ZBarSymbol,decode  
	from PIL import Image
	from datetime import datetime

	arch_imagen=arch_imagen.replace("%04d","0001")
	print "Archivo QR", arch_imagen

	imagen=Image.open(arch_imagen)
	area=imagen.crop((x,y,x1,y1))
	#area.show()
	area.save("{}_crop.png".format(arch_imagen))
	decodificado=decode (area,symbols=[ZBarSymbol.QRCODE])
	decodificado = decodificado[0][0].split("\r\n")
	salida={}
	for items in decodificado:
		partir=items.split(":")
		if partir[0].strip()=="NumFac":
			prefijo,nrofac=SepararPrefijo_Nro(partir[1].strip())
			salida["NumFac"]=nrofac
			salida["Prefijo"]=prefijo
		elif partir[0].strip()=="FecFac":
			salida["FecFac"]=datetime.strptime(partir[1].strip(),"%Y%m%d%H%M%S")
		elif partir[0][0:3]=="Val":
			salida[partir[0].strip()]=float(partir[1].strip())
		else:
			salida[partir[0].strip()]=partir[1].strip()
	return salida

def GeneraPNG(arch_pdf):
	print ("GeneraPNG")
	import subprocess
	import os
	from tempfile import gettempdir
	print arch_pdf
	if not os.path.isfile(arch_pdf):
		return False

	salida,nombre=os.path.split(arch_pdf)

	comando=['gs',
			'-dNOPAUSE',
			'-dBATCH',
			'-sDEVICE=png256',
			'-r150',
			#'-sPAPERSIZE=%s' %(self.tampagina), 
			'-q',
			'-sOutputFile="{}_%04d.png"'.format( os.path.join(gettempdir(), nombre) ),
			#'-sstdout="Facil_{}.gs"'.format( os.path.join(gettempdir(), nombre) ),
			'-f',
			arch_pdf
			]
	print comando
	##proceso = subprocess.Popen(comando,stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
	##resultado = proceso.stdout.read()
	##return salida, resultado
	subprocess.call(comando)
	salida='{}_%04d.png'.format( os.path.join(gettempdir(), nombre) )
	return salida

def SepararPrefijo_Nro(valor):
	perfijo=""
	nrofac=""
	for item in valor:
		if item.isalpha():
			perfijo +=item
		elif item.isdigit():
			nrofac +=item
	if nrofac=="":
		nrofac=None
	else:
		nrofac=nrofac[3:]	#ojo esto es un error del QR????
	return perfijo,int(nrofac)

def UnirFormato(datos,formato):
	from PyPDF2 import PdfFileWriter, PdfFileReader
	salida = PdfFileWriter()
	try:
		arch_e=open(datos, "rb")
		arch_f=open(formato, "rb")
		entrada=PdfFileReader(arch_e)
		formato=PdfFileReader(arch_f)
		for pagina in range(entrada.getNumPages()):
			fondo=entrada.getPage(pagina)
			fondo.mergePage(formato.getPage(0))
			salida.addPage(fondo)
		guardar=file("{}.nuevo.pdf".format(datos),"wb")
		salida.write(guardar)
		guardar.close()
		arch_e.close()
		arch_f.close()
		resultado=True
	except Exception as e:
		resultado = [e, datos, formato]

	return resultado

def UnirImpresion(listapdfs,formato,nombsalida):
	if len(listapdfs)<1:
		return None
	from PyPDF2 import PdfFileWriter, PdfFileReader

	arch_f=open(formato, "rb")
	formato=PdfFileReader(arch_f)
	arch_f.close()

	salida = PdfFileWriter()

	try:
		for datos in listapdfs:
			arch_e=open(datos, "rb")
			entrada=PdfFileReader(arch_e)
			for pagina in range(entrada.getNumPages()):
				fondo=entrada.getPage(pagina)
				fondo.mergePage(formato.getPage(0))
				salida.addPage(fondo)
			arch_e.close()

		guardar=file(nombsalida,"wb")
		salida.write(guardar)
		guardar.close()
		resultado=True

	except Exception as e:
		resultado = [e, datos, formato]

	return resultado




if __name__=="__main__":
	resultado=GeneraPNG("/home/www-data/paso/face_f0890312749003A75090B.pdf")
	#print (resultado)
	print ExtraerQR(resultado)
	#print ExtraerQR('/tmp/face_f0890312749003A75090B.pdf_0001.png')
