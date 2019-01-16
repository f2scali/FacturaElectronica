# -*- coding: utf-8 -*-
def ServicioCorreo():
	import f2s_imap
	correo = db(db.tbl_correo.id==1).select().first()
	envio=f2s_imap.ObjImap("/tmp",correo.servidor, 
							correo.puerto, 
							correo.usuario, 
							correo.password,"Facturacion",True)
	envio.Procesar()
	if (envio.docXML)==0:
		print "Vacio"
		return "Vacio"
	for posicion in envio.docXML:
		print "envio:",envio.docXML, envio.docpdf
		try:
			ExtraerContenidos(envio.docpdf[posicion],envio.docXML[posicion])
			#Borrar Temporales falta!!!

		except Exception as e:
			return e, envio.docXML, envio.docpdf


def ExtraerContenidos(arch_pdf,arch_xml):
	print "ExtraerContenidos...>"
	import f2s_funciones
	import os
	if not os.path.isfile(arch_pdf):
		return "Error no Exite PDF [{}]".format(arch_pdf)
	if not os.path.isfile(arch_xml):
		return "Error no Exite XML [{}]".format(arch_xml)
	#ruta para guardar los pdf e imagenes
	imgpng=f2s_funciones.GeneraPNG(arch_pdf)
	datos=f2s_funciones.ExtraerQR(imgpng)
	if not datos:
		return "Error extracion QR [{}]".format(imgpng)
	buscar = db(db.tbl_factelectronica.nrofac==datos["NumFac"]).select().first()
	if buscar:
		#Verificar
		if buscar.estado == 'Cguno':
			db.tbl_novedades.insert(
				idfact=buscar.id,
				novedad="PDF actualiza, a estado de imprimir")
			estado='Imprimir'
			##db.commit()
		elif  buscar.estado == 'Electronica':
			db.tbl_novedades.insert(
				idfact=buscar.id,
				novedad="No se actuliza ya fue envido el PDF")
			#db.commit()
			return "No se actuliza ya fue envido el PDF"
		elif buscar.estado=='imprimir':
			db.tbl_novedades.insert(
				idfact=buscar.id,
				novedad="Ya se recibieron los datos del PDF")
			#db.commit()
			return "Ya se recibieron los datos del PDF"
		elif buscar.estado=='Impresa':
			db.tbl_novedades.insert(
				idfact=buscar.id,
				novedad="Ya se recibieron los datos del PDF")
			#db.commit()
			return "No se actualiza ya fue impresa"
		elif buscar.valfac!=datos["ValFac"]:
			db.tbl_novedades.insert(
				idfact=buscar.id,
				novedad="No considen el valor subtotal   valSpool={}   ValorPDF={}".format(buscar.valfac,datos["ValFac"]))
			#db.commit()
			return "No considen el subtotal valor SubTotal"
		elif buscar.valiva!=datos["ValIva"]:
			db.tbl_novedades.insert(
				idfact=buscar.id,
				novedad="No considen el valor IVA   valSpool={}   ValorPDF={}".format(buscar.valIva,datos["ValIva"]))
			#db.commit()
			return "No considen el valor IVA"
		elif buscar.valtot!=datos["ValFacIm"]:
			db.tbl_novedades.insert(
				idfact=buscar.id,
				novedad="No considen el valor Total   valSpool={}   ValorPDF={}".format(buscar.valtot,datos["ValFacIm"]))
			#db.commit()
			return "No considen el valor Total"
		elif buscar.docadq!=datos["DocAdq"]:
			db.tbl_novedades.insert(
				idfact=buscar.id,
				novedad="No considen el Nit del cliente  valSpool={}   ValorPDF={}".format(buscar.docadq,datos["DocAdq"]))
			#db.commit()
			return "No considen el valor Total"

		rutaimagenes=os.path.join(request.folder,"uploads",
								str(buscar.created_on.year),str(buscar.created_on.month))
		arch_qr=os.path.split(arch_pdf)[1]
		arch_qr="{}_0001.png_crop.png".format(os.path.join("/tmp",arch_qr))
		#datos de los archivos
		s_pdf=open(arch_pdf,"rb")
		s_xml=open(arch_xml,"rb")
		s_qr=open(arch_qr,"rb")
		#Reubicando las imagenes		
		db.tbl_factelectronica.arch_siesa.uploadfolder=rutaimagenes
		db.tbl_factelectronica.arch_xml.uploadfolder=rutaimagenes
		db.tbl_factelectronica.arch_qr.uploadfolder=rutaimagenes
		db(db.tbl_factelectronica.nrofac==buscar.nrofac).update( 
				fecfac=datos["FecFac"],
				nitfac=datos["NitFac"],
				valimp=datos["ValOtroIm"],
				cufe=datos["CUFE"],
				rutaimgs=rutaimagenes,
				arch_xml=db.tbl_factelectronica.arch_xml.store(s_xml,arch_xml),
				arch_siesa=db.tbl_factelectronica.arch_siesa.store( s_pdf,archivo),
				arch_qr=db.tbl_factelectronica.arch_qr.store(s_qr,arch_qr),
				estado=estado)
		##db.commit()
	else:
		estado='Electronica'
		rutaimagenes=os.path.join(request.folder,"uploads",str(request.now.year),str(request.now.month))
		#Ruta de los archivos
		arch_qr=os.path.split(arch_pdf)[1]
		arch_qr="{}_0001.png_crop.png".format(os.path.join("/tmp",arch_qr))
		#datos de los archivos
		s_pdf=open(arch_pdf,"rb")
		s_xml=open(arch_xml,"rb")
		s_qr=open(arch_qr,"rb")
		#Reubicando las imagenes		
		db.tbl_factelectronica.arch_siesa.uploadfolder=rutaimagenes
		db.tbl_factelectronica.arch_xml.uploadfolder=rutaimagenes
		db.tbl_factelectronica.arch_qr.uploadfolder=rutaimagenes
		db.tbl_factelectronica.insert( 
				nrofac=datos["NumFac"],
				prefijo=datos["Prefijo"],
				fecfac=datos["FecFac"],
				nitfac=datos["NitFac"],
				valfac=datos["ValFac"],
				valiva=datos["ValIva"],
				valtot=datos["ValFacIm"],
				valimp=datos["ValOtroIm"],
				cufe=datos["CUFE"],
				docadq=datos["DocAdq"],
				rutaimgs=rutaimagenes,
				arch_xml=db.tbl_factelectronica.arch_xml.store(s_xml,arch_xml),
				arch_siesa=db.tbl_factelectronica.arch_siesa.store( s_pdf,arch_pdf),
				arch_qr=db.tbl_factelectronica.arch_qr.store(s_qr,arch_qr),
				estado=estado)
		
		##Crear PDF
		if estado=="Imprimir":
			factura = db(db.tbl_factelectronica.nrofac==datos["NumFac"]).select().first()
			detalle = db(db.tbl_detalle.idfact==factura.id).select()

	db.commit()
	return locals()




##################3
def procesarfactura(arch):
	import os
	if not os.path.isfile(arch):return "No Exite archivo [{}]".format(arch)
	archivo=open(arch,"rb")
	inicio="M"
	finpag="P"
	cuenta=0
	procesar=False
	datos={}
	detalle=[]
	pibote=True




	for linea in archivo.readlines():
		#Inicio Pagina
		print cuenta,linea

		if linea.find(inicio)>-1:
			procesar=True
			cuenta=1
			continue

		if not procesar: continue
		#Eliminar fin de linea y retorno de carro
		linea=linea.replace("\n","")
		linea=linea.replace("\r","")

		if cuenta>=5 and cuenta <=6:#Extaer Resolucion
			if datos.has_key("resoluicion"):
				datos["resoluicion"]+=linea[51:106].strip()
			else:
				datos["resoluicion"]=linea[51:106].strip()
		
		elif cuenta==8: datos["ciudad"]=linea[76:]
		
		elif cuenta==9:	datos["nomb_cliente"]=linea[:41].strip()
		
		elif cuenta==10: datos["resp_cliente"]=linea[:41].strip()
		
		elif cuenta==11:
			datos["direccion"]=linea[:46].strip()
		
		elif cuenta==12:
			temp=linea[:23].strip()
			datos["nit"]=temp.split("-")[0]
			datos['telefono']=linea[25:36].strip()
		
		elif cuenta==13:
			datos["ciiu"]=linea[23:].strip()

		elif cuenta==14:
			datos["barrio"]=linea.strip()
		#######################################################
		#Detalle
		elif cuenta>=15 and cuenta <=49:
			#print cuenta,linea
			linea=linea.strip()
			if len(linea)<1:
				cuenta +=1
				continue
			linea=linea.replace(",","")
			#if cuenta % 2 ==0  :#impar
			if pibote:
				detalle.append(linea[:7].strip())
				detalle.append(linea[7:48].strip())
				detalle.append(float(linea[48:60].strip()))
				detalle.append(float(linea[60:75].strip()))
				detalle.append(float(linea[75:].strip()))
				pibote=False
			else:
				pibote=True
				detalle.append(linea[7:53].strip())
				if datos.has_key("detalle"):
					datos["detalle"].append(detalle)
				else:
					datos["detalle"]=[detalle]
				detalle=[]

		#######################################################
		#Totales
		elif cuenta==50:
			#print datos['detalle']
			#break 
			#print cuenta,linea
			datos["son"]=linea.strip()
		elif cuenta==51:
			#print cuenta,linea
			datos["son"]+="{} ".format(linea[:50].strip())
			datos["dctos"]=linea[69:].strip()
		elif cuenta==52: datos["son"]+="{} ".format(linea[:50].strip())
		elif cuenta==53:
			datos["son"]+="{} ".format(linea[:50].strip())
			datos["subtotal"]=float(linea[69:].strip().replace(",",""))
		elif cuenta==54:
			datos["observaciones"]=linea[:50].strip()
			datos["iva"]=float(linea[69:].strip().replace(",",""))
		elif cuenta==55:
			datos["observaciones"]+="{} ".format(linea[:50].strip())
			datos["retfte"]=float(linea[69:].strip())
		elif cuenta==56:
			datos["observaciones"]+="{} ".format(linea[:50].strip())
			datos["retica"]=float(linea[69:].strip().replace(",",""))
		elif cuenta==57:
			datos["observaciones"]+="{} ".format(linea[:50].strip())
			datos["Totales"]=float(linea[69:].strip().replace(",",""))
		elif cuenta==59:
			linea=linea.replace("P","")
			datos["nrofac"]=linea[69:].strip()
			###########################################
			#Guarda pagina
			consulta=db.tbl_factelectronica.nrofac==datos["nrofac"]
			consulta&=db.tbl_factelectronica.prefijo==datos["ciudad"][:3]
			consulta=db(consulta).select().first()
			print "Guardar datos"
			if consulta: #actualiza
				idfactura=consulta.id
				
				if consulta.estado == 'Cguno':
					db.tbl_novedades.insert(
						idfact=idfactura,
						novedad="Se actualizan los datos de Cguno")
					estado='Cguno'
					db.commit()

				elif  consulta.estado == 'Electronica':
					db.tbl_novedades.insert(
						idfact=idfactura,
						novedad="Se actualiza, a estado de imprimir")
					estado='Imprimir'
					db.commit()

				elif consulta.estado=='imprimir':
					db.tbl_novedades.insert(
						idfact=idfactura,
						novedad="Ya se recibieron los datos de Cguno se actualizan")
					estado='Imprimir'
					db.commit()

				elif consulta.estado=='Impresa':
					db.tbl_novedades.insert(
						idfact=idfactura,
						novedad="No se puede actulizar ya fue impresa")
					db.commit()
					return "No se actualiza ya fue impresa"


				db(db.tbl_factelectronica.id == idfactura).update(
					docadq=datos["nit"],
					son=datos["son"],
					valfac=datos["subtotal"],
					valiva=datos["iva"],
					valtot=datos["Totales"],
					valretica=datos["retica"],
					valretfte=datos["retfte"],
					valdctos=datos["dctos"],
					empresa=datos["nomb_cliente"],
					representante=datos["resp_cliente"],
					telefono=datos['telefono'],
					direccion=datos["direccion"],
					ciudad=datos["ciudad"],
					barrio=datos["barrio"],
					observaciones=datos["observaciones"],
					resolucion=datos["resoluicion"],
					ciiu=datos["ciiu"],					
					)
				db.commit()
				#se deshabilitan los anterios detalles... No se borran !!
				db(db.tbl_detalle.idfact==idfactura).update(is_active=False)
				db.commit()
				for item in datos["detalle"]:
					db.tbl_detalle.insert(
						idfact=idfactura,
						item=item[0],
						detalle=item[1],
						detalle1=item[5],
						cantidad=item[2],
						unitario=item[3],
						valortotal=item[4],
						)
					db.commit()


			else:#crea
				idfactura=db.tbl_factelectronica.insert(
					nrofac=datos["nrofac"],
					###prefijo=datos["ciudad"][:3],
					docadq=datos["nit"],
					son=datos["son"],
					valfac=datos["subtotal"],
					valiva=datos["iva"],
					valtot=datos["Totales"],
					valretica=datos["retica"],
					valretfte=datos["retfte"],
					valdctos=datos["dctos"],
					empresa=datos["nomb_cliente"],
					representante=datos["resp_cliente"],
					telefono=datos['telefono'],
					direccion=datos["direccion"],
					ciudad=datos["ciudad"],
					barrio=datos["barrio"],
					observaciones=datos["observaciones"],
					resolucion=datos["resoluicion"],
					ciiu=datos["ciiu"],
					estado= 'Cguno'
					)
				db.commit()
				#print datos['detalle']
				for item in datos["detalle"]:
					db.tbl_detalle.insert(
						idfact=idfactura,	item=item[0],
						detalle=item[1],	detalle1=item[5],
						cantidad=item[2],	unitario=item[3],
						valortotal=item[4],
						)
					db.commit()
			#Verificar Prefijo
			rangos=db(db.tbl_tbl_rangos).select()
			nrofac=int(datos["nrofac"].strip())
			paso=False
			for rango in rangos:
				if nrofac >=rango.inicio or nrofac<=rango.fin:
					db(db.tbl_factelectronica.id==idfactura).update(prefijo=rango.id_prefijos)
					db.commit()
					paso=True
					break
			if not paso:
				Novedades(idfactura,"Nro factura {} fuera del Rango de Factacion".format(nrofac) )

			#
			#iniciar pagina
			procesar=False
			detalle=[]
			cuenta=0
			datos={}
			pibote=True
			continue
		cuenta +=1

	return "OK"

def Novedades(idfactura,novedad):
	usrs_admin=db.auth_group.role=="Administrador"
	usrs_admin &=db.auth_membership.group_id==db.auth_group.id
	usrs_admin=db(usrs_admin).select(db.auth_membership.user_id)
	#for usuario in  usrs_admin:
	#	print usuario.user_id
	#return
	hijo=None
	for usuario in  usrs_admin:
		if hijo:
			hijo = db.tbl_novedades.insert(
				idfact=idfactura,
				propietario=usuario.user_id,
				novedad=novedad,
				hijo=hijo,
				vista=False)
		else:
			hijo = db.tbl_novedades.insert(
				idfact=idfactura,
				propietario=usuario.user_id,
				novedad=novedad,
				vista=False)
		db.commit()


if __name__ == '__main__':
	procesarfactura('/home/marco/Clientes/atlas/facturacionelectronicaatlas/tmp/F2S-aMatJi')