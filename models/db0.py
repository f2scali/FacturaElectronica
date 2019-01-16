# -*- coding: utf-8 -*-

def F2s_VerPDF(ruta):
	pdf= open(ruta, "rb").read()
	response.headers['Content-Type'] = 'application/pdf'
	response.headers['AddHeader'] = {'content-disposition':"inline"}
	return pdf




def F2s_CrearPDF(factura,detalle):
	##from f2scodigo import ObjCode128
	import f2s_cod128
	import uuid
	import os
	import f2s_funciones  
	from reportlab.graphics import renderPDF
	from reportlab.lib.utils import ImageReader
	from reportlab.lib.pagesizes import letter
	from reportlab.pdfgen import canvas
	from reportlab.pdfbase import pdfmetrics
	from reportlab.pdfbase.ttfonts import TTFont
	from reportlab.platypus import Paragraph, Image
	from reportlab.lib.styles import ParagraphStyle	
	##from reportlab.lib.styles import getSampleStyleSheet

	FORM_FACTURA=os.path.join(request.folder,"static","formatos",'Factura_Altas.pdf')
	#factura
	rutaimgs=os.path.join(request.folder,"uploads",
								"{}".format(factura.created_on.year),
								"{}".format(factura.created_on.month),
								)
	#factura.arch_siesa)
	#Letras Definidas
	rutafont=os.path.join(request.folder,"static","fonts")
	pdfmetrics.registerFont(TTFont('Ubuntu', 	  os.path.join(rutafont,'Ubuntu-R.ttf')))
	pdfmetrics.registerFont(TTFont('Ubuntu-Bold', os.path.join(rutafont,'Ubuntu-B.ttf')))
	pdfmetrics.registerFont(TTFont('Ubuntu-Cond', os.path.join(rutafont,'Ubuntu-C.ttf')))
	pdfmetrics.registerFont(TTFont('Cod128', os.path.join(rutafont,'Codigo128.ttf')))
	#Creacion del archivo de datos factura posicionado
	datos_pdf=os.path.join("/tmp","{}{}.pdf".format(uuid.uuid4(),factura.nrofac))
	pdf_f2s= canvas.Canvas(datos_pdf,pagesize=letter)
	#Resoluucion Dian
	angulo=90
	pdf_f2s.rotate(angulo)
	pdf_f2s.setFont("Ubuntu", 6)
	pdf_f2s.drawString( 215, -512, factura.resolucion.decode('cp437').strip())
	pdf_f2s.rotate(angulo * -1)

	#encabezado
	pdf_f2s.setFont("Ubuntu-Bold", 17)
	posy=630
	posx=520
	pdf_f2s.drawRightString(posx-5, posy, "{}-".format(factura.prefijo.decode('cp437').strip()) )
	pdf_f2s.drawString(posx, posy, factura.nrofac.decode('cp437').strip() )
	posx=30	
	pdf_f2s.setFont("Ubuntu-Bold", 9)
	posy=670
	pdf_f2s.drawString(posx, posy, factura.empresa.decode('cp437').strip() )
	pdf_f2s.setFont("Ubuntu", 8)
	posy=660
	pdf_f2s.drawString(posx, posy, factura.representante.decode('cp437').strip() )
	pdf_f2s.drawString(posx, posy-9, factura.nitfac.decode('cp437').strip() )
	pdf_f2s.drawString(posx+160, posy-9, "Tel:{}".format(factura.telefono.decode('cp437')).strip() )
	pdf_f2s.drawString(posx, posy-18, factura.direccion.decode('cp437').strip() )
	pdf_f2s.drawString(posx, posy-27, factura.ciudad.decode('cp437').strip() )
	pdf_f2s.drawString(posx, posy-36, factura.barrio.decode('cp437').strip() )
	#Fecha Factura
	posy=664
	posx=345
	pdf_f2s.drawString(posx, posy,factura.fecfac[8:10].strip() )
	pdf_f2s.drawString(posx+30, posy,factura.fecfac[5:7].strip() )
	pdf_f2s.drawString(posx+70, posy,factura.fecfac[:4].strip() )
	#Fecha Vencimiento
	posy=625
	pdf_f2s.drawString(posx, posy,factura.fecfac[8:10].strip() )
	pdf_f2s.drawString(posx+30, posy,factura.fecfac[5:7].strip() )
	pdf_f2s.drawString(posx+70, posy,factura.fecfac[:4].strip() )

	#Detalle:
	posy=590
	posx=30
	for item in detalle:
		pdf_f2s.drawString(posx, posy,item.item.decode('cp437').strip() )
		pdf_f2s.drawString(posx+65, posy,item.detalle.decode('cp437').strip() )
		pdf_f2s.drawString(posx+65, posy-9,item.detalle1.decode('cp437').strip() )
		pdf_f2s.drawRightString(posx+310, posy, "{:,.0f}".format(item.cantidad) )
		pdf_f2s.drawRightString(posx+385, posy, "{:,.0f}".format(item.unitario) )
		pdf_f2s.drawRightString(posx+470, posy, "{:,.0f}".format(item.valortotal) )
		posy -=22
	#pie
	posy=295
	posx=30
	#pdf_f2s.drawString(posx, posy,factura.son.decode('cp437').strip() )
	style = ParagraphStyle(
	        name='Normal',
	        fontName='Ubuntu',
	        fontSize=8,
	        leading = 10,
	    )
	p = Paragraph(factura.son.decode('cp437').strip(), style)
	w, h = p.wrapOn(pdf_f2s, 464, 100)
	p.drawOn(pdf_f2s, posx, posy-h)


	posy=260
	posx=30
	style = ParagraphStyle(
	        name='Normal',
	        fontName='Ubuntu',
	        fontSize=8,
	        leading = 9,
	    )
	p = Paragraph(factura.observaciones.decode('cp437').strip(), style)
	w, h = p.wrapOn(pdf_f2s, 280, 100)
	p.drawOn(pdf_f2s, posx, posy-h)

	posy=264
	posx=320
	pdf_f2s.setFont("Ubuntu", 7)
	pdf_f2s.drawString(posx, posy,"cufe:{}".format(factura.cufe.decode('cp437').strip()) )
	pdf_f2s.setFont("Ubuntu", 8)
	posy=250
	posx=490
	pdf_f2s.drawRightString(posx, posy,"{:,.0f}".format(factura.valfac) )
	pdf_f2s.drawRightString(posx, posy-10,"{:,.0f}".format(factura.valiva) )
	pdf_f2s.setFont("Ubuntu-Bold", 10)
	pdf_f2s.drawRightString(posx, posy-32,"{:,.0f}".format(factura.valtot) )
	
	posy=116
	posx=30
	pdf_f2s.setFont("Ubuntu", 7)
	pdf_f2s.drawString(posx, posy, factura.empresa.decode('cp437').strip() )
	pdf_f2s.drawString(posx+150, posy, factura.nrofac.decode('cp437').strip() )
	pdf_f2s.drawString(posx+230, posy, factura.nitfac.decode('cp437').strip() )
	pdf_f2s.drawString(posx+307, posy, "{:,.0f}".format(factura.valtot) )
	pdf_f2s.drawString(posx+358, posy,factura.fecfac[8:10].strip() )
	pdf_f2s.drawString(posx+385, posy,factura.fecfac[5:7].strip() )
	pdf_f2s.drawString(posx+412, posy,factura.fecfac[:4].strip() )

	#codigo de barras
	posy=15
	posx=75
	pdf_f2s.setFont("Ubuntu", 7)
	codigo=	"(415)7709998015937(8020){:06d}{:018d}(3900){:010d}(96){}{}{}".format(int(factura.nrofac.strip()),
												int(factura.nitfac.strip()),
												int(factura.valtot),
												factura.fecfac[8:10],
												factura.fecfac[5:7],
												factura.fecfac[:4] 
											)
	pdf_f2s.drawString(posx, posy, codigo)
	posy=25
	posx=10
	codigobar=f2s_cod128.code128_image (chr(102)+codigo)
	pdf_f2s.drawImage(ImageReader(codigobar),posx,posy,width=450, height=35)


	#qr
	posy=670
	posx=503
	rutaimagenes=os.path.join(request.folder,"uploads",str(factura.created_on.year),
								str(factura.created_on.month),factura.arch_qr)
	logo = Image(rutaimagenes)
	logo.drawHeight=logo.drawHeight-32
	logo.drawWidth=logo.drawWidth-32
	logo.wrapOn(pdf_f2s, logo.drawWidth, logo.drawHeight)
	logo.drawOn(pdf_f2s, posx,posy)
	
	#Activar aui
	if AIU:
		posy=300
		posx=30
		pdf_f2s.setFont("Ubuntu", 7)
		pdf_f2s.drawString(posx, posy,"AIU 10%:{:,.0f} Tomado desde Subtotal".format(factura.valfac * .1) )

	#Fin
	pdf_f2s.showPage()
	pdf_f2s.save()
	unir = f2s_funciones.UnirFormato(datos_pdf,FORM_FACTURA)
	return datos_pdf
