# -*- coding: utf-8 -*-

def cambioaiu():
	checkAIU=request.vars.checkAIU
	if checkAIU:
		AIU=True
	else:
		AIU=False

	return XML('ALERT("Estado AIU={}");'.format(AIU))



def lstSucursales():
	consulta=db().select(db.tbl_prefijos.id,db.tbl_prefijos.ciudad,db.tbl_prefijos.prefijo, orderby=db.tbl_prefijos.ciudad)
	salida=DIV (
  				DIV ("Sucursales",_class="card-header"),
  				_class="card bg-light mb-3 border-primary")
 	temp=[]
	for item in consulta:
		temp.append(A(item.ciudad,
							_href=URL('index',vars=dict(prefijo=item.prefijo)),
							_class="btn btn-outline-primary"
							),
					)
	
	if temp:
		salida.append(DIV(temp,_class="card-body"))
	return salida

def linkimg(titulo,id,tipo):

	salida = A(
				SPAN(XML("&ensp;"),_class="icon magnifier icon-zoom-in glyphicon glyphicon-zoom-in"),
				titulo,
				_class='button btn btn-default btn-secondary',
				_href=URL("verimagenes",
						user_signature=True,
						vars=dict(imagen=id,tipo=tipo)
						),
				_target="_blank"

			)
	return salida

def lst_impresoras():
	salida =SELECT([OPTION(grupo.nombre,_value=grupo.id) for grupo in db().select(db.tbl_impresoras.ALL)],
                            _name="id_impresora",_class="generic-widget form-control")
	return salida

@auth.requires_login()
def index():
	idprefijo=request.vars.prefijo or 'CAL'
	estado=request.vars.estado or 'Imprimir'

	impresoras=lst_impresoras()

	estados=DIV()
	if estado !="Imprimir":
		estados.append(A("Imprimir",
							_href=URL('index',vars=dict(prefijo=idprefijo,estado="Imprimir")),
							_class="btn btn-outline-primary"
							))
	if estado !="Electronica":
		estados.append(A("Electronica",
							_href=URL('index',vars=dict(prefijo=idprefijo,estado="Electronica")),
							_class="btn btn-outline-primary"
							))
	if estado !="Cguno":
		estados.append(A("Cguno 746",
							_href=URL('index',vars=dict(prefijo=idprefijo,estado="Cguno")),
							_class="btn btn-outline-primary"
							))
	
	if estado !="Impresa":
		estados.append(A("Impresas",
							_href=URL('index',vars=dict(prefijo=idprefijo,estado="Impresa")),
							_class="btn btn-outline-primary"
							))
	
	sucursales=lstSucursales()
	consulta=db.tbl_factelectronica.prefijo==idprefijo
	consulta &=db.tbl_factelectronica.estado==estado
	formulario=db(consulta).select(orderby=db.tbl_factelectronica.created_on)

	links = [
              #lambda row: linkimg("Siesa", row.id,"siesa",row.Arch Pdf),
              #lambda row: linkimg("QR",  row.id, "qr" ),
              #lambda row: linkimg("XML", row.id, "xml"),
              lambda row: linkimg("PDF", row.id, "pdf"),
            ]

	campos= [db.tbl_factelectronica.nrofac,
			db.tbl_factelectronica.prefijo,
			db.tbl_factelectronica.docadq,
			db.tbl_factelectronica.empresa,
			db.tbl_factelectronica.valtot,
			#db.tbl_factelectronica.arch_qr,
			#db.tbl_factelectronica.arch_xml,
			#db.tbl_factelectronica.arch_pdf,

    		]

	selectable = lambda ids : redirect(URL('default',
                                         'asociar_multiples',
                                         vars=dict(id=ids)))
	formulario=SQLFORM.grid(consulta,
				links=links,
				fields=campos,
				deletable=False,
				editable=False,
				details=False,
				paginate=20,
				create=False,
				user_signature=True,
				maxtextlength=40,
				csv=False,
				selectable=selectable,
				)



	return locals()

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
	if not request.env.request_method == 'GET': raise HTTP(403)
	return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
	response.view = 'generic.html' # use a generic view
	tablename = request.args(0)
	if not tablename in db.tables: raise HTTP(403)
	grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
	return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
	auth.wikimenu() # add the wiki to the menu
	return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
	"""
	exposes:
	http://..../[app]/default/user/login
	http://..../[app]/default/user/logout
	http://..../[app]/default/user/register
	http://..../[app]/default/user/profile
	http://..../[app]/default/user/retrieve_password
	http://..../[app]/default/user/change_password
	http://..../[app]/default/user/bulk_register
	use @auth.requires_login()
		@auth.requires_membership('group name')
		@auth.requires_permission('read','table name',record_id)
	to decorate functions that need access control
	also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
	"""
	return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
	"""
	allows downloading of uploaded files
	http://..../[app]/default/download/[filename]
	"""
	return response.download(request, db)

def subirPDF():
	from glob import glob
	import os
	#archivos=glob('/home/www-data/paso/*.pdf')
	archivos=glob('/home/marco/Clientes/atlas/facturacionelectronicaatlas/*.pdf')
	formulario=UL(_class="list-group")
	for archivo in archivos:
		archivo=os.path.split(archivo)[-1]
		formulario.append(LI(A(archivo,_href=URL("procPDF",vars=dict(archivo=archivo))),
							_class="list-group-item")
						)
	formulario=FORM(formulario)
	return dict(formulario=formulario)

def procPDF():
	import f2s_funciones
	import os
	archivo =request.vars.archivo or redirect(URL('subirPDF'))
	#archivo="/home/www-data/paso/{}".format(archivo)
	archivo="/home/marco/Clientes/atlas/facturacionelectronicaatlas/{}".format(archivo)
	if not os.path.isfile(archivo):
		redirect(URL('subirPDF'))

	#ruta para guardar los pdf e imagenes
	imgpng=f2s_funciones.GeneraPNG(archivo)
	datos=f2s_funciones.ExtraerQR(imgpng)
	if not datos:
		redirect(URL('subirPDF'))
	

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

		rutaimagenes=os.path.join(request.folder,"uploads",str(buscar.created_on.year),str(buscar.created_on.month))
		arch_qr=os.path.split(archivo)[1]
		arch_qr="{}_0001.png_crop.png".format(os.path.join("/tmp",arch_qr))
		arch_xml="{}xml".format(archivo[:-3])
		#datos de los archivos
		s_pdf=open(archivo,"rb")
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
		arch_qr=os.path.split(archivo)[1]
		arch_qr="{}_0001.png_crop.png".format(os.path.join("/tmp",arch_qr))
		arch_xml="{}xml".format(archivo[:-3])
		#datos de los archivos
		s_pdf=open(archivo,"rb")
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
				arch_siesa=db.tbl_factelectronica.arch_siesa.store( s_pdf,archivo),
				arch_qr=db.tbl_factelectronica.arch_qr.store(s_qr,arch_qr),
				estado=estado)
		##db.commit()
		##Crear PDF
		if estado=="Imprimir":
			factura = db(db.tbl_factelectronica.nrofac==datos["NumFac"]).select().first()
			detalle = db(db.tbl_detalle.idfact==factura.id).select()




	return locals()

def prueba():
	import os
	archivo="/home/www-data/imagenes/frmFactura.pdf"
	stream=open(archivo,"rb")
	db.tbl_factelectronica.arch_pdf.uploadfolder=os.path.join(request.folder,"uploads","2018")
	db.tbl_factelectronica.insert(arch_pdf=db.tbl_factelectronica.arch_pdf.store(stream, archivo))
	return os.path.join(request.folder,"uploads","2018")

def pruebas():
	import os
	buscar=db(db.tbl_factelectronica.nrofac=="748535").select().first()
	rutaimagenes=os.path.join(request.folder,"uploads",str(buscar.created_on.year),
								str(buscar.created_on.month),buscar.arch_siesa)
	x=A("ARG",_href=URL("VerPDFs",vars=dict(ruta=rutaimagenes)),_target="_blank")
	#db.tbl_factelectronica.arch_xml.uploadfolder=
	return locals()
def VerPDFs():
	ruta=request.vars.ruta
	pdf=F2s_VerPDF(ruta)
	return pdf


def verimagenes():
	idfact = request.vars.imagen#
	tipo = request.vars.tipo
	factura = db(db.tbl_factelectronica.id==idfact).select().first()
	detalle = db((db.tbl_detalle.idfact==factura.id)&(db.tbl_detalle.is_active==True)).select()
	salida = F2s_CrearPDF(factura,detalle)
	salida ="{}.nuevo.pdf".format(salida)
	pdf =F2s_VerPDF(salida)
	return pdf

