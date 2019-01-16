# -*- coding: utf-8 -*-
#Definicion de Rangos y prefijos
@auth.requires(lambda: auth.has_membership('Administrador') or auth.has_membership ('Super'))
def prefijos():
	csv=False
	links= [lambda registro: A(SPAN(_class="icon pen icon-pencil glyphicon glyphicon-pencil"),
							'Rangos', 
							_class="button btn btn-default btn-secondary", 
							_href=URL('rangos',vars=dict(id=registro.id)))]
	formulario=SQLFORM.grid(db.tbl_prefijos,
	    links=links,
	    orderby=db.tbl_prefijos.ciudad,
	    paginate=20,
	    editable=True,
	    deletable=False,
	    details=False,
	    create=True,
	    csv=csv,
        advanced_search=False,
	    maxtextlength=60,
	    user_signature=True
    )
	return dict(formulario=formulario)
@auth.requires(lambda: auth.has_membership('Administrador') or auth.has_membership ('Super'))
def rangos():
	csv=False
	idprefijo=request.vars.id or redirect(URL("prefijos"))
	ciudad=db(db.tbl_prefijos.id==idprefijo).select().first()
	db.tbl_rangos.id_prefijos.default=idprefijo
	db.tbl_rangos.id_prefijos.writable=False
	#db.tbl_rangos.id_prefijos.readable=False
	formulario=SQLFORM.grid(db.tbl_rangos.id_prefijos==idprefijo,
	    paginate=20,
	    editable=True,
	    deletable=False,
	    details=False,
	    create=True,
	    csv=csv,
        advanced_search=False,
	    maxtextlength=60,
	    user_signature=True
	)
	return dict(formulario=formulario,ciudad=ciudad)
#### Define servidores de correo
@auth.requires(lambda: auth.has_membership('Administrador') or auth.has_membership ('Super'))
def correo():
	if auth.has_membership("Administrador"):
		csv=True
	else:
		csv=False
	links= [lambda registro: A(SPAN(_class="icon pen icon-pencil glyphicon glyphicon-pencil"),
							' Prueba Correo', 
							_class="button btn btn-default btn-secondary", 
							_href=URL('pruebacorreo',vars=dict(id=registro.id)))]

	formulario=SQLFORM.grid(db.tbl_correo,
		paginate=20,
		links=links,
	    editable=True,
	    deletable=False,
	    details=False,
	    create=True,
	    csv=csv,
        advanced_search=False,
	    maxtextlength=60,
	    user_signature=True 
	)
	return(dict(formulario=formulario))

@auth.requires(lambda: auth.has_membership('Administrador') or auth.has_membership ('Super'))
def pruebacorreo():
	idservcorreo=request.vars.id or redirect(URL("correo"))
	import f2s_imap
	consulta=db(db.tbl_correo.id==idservcorreo).select().first()
	obcorreo=f2s_imap.ObjImap( "/tmp", 
						servidor=consulta.servidor, 
						puerto=consulta.puerto, 
						login=consulta.usuario, 
						password=consulta.password,
						bandeja=consulta.bandeja,
						)
	obcorreo.Procesar()
	return locals()

#Administracion de usuarios y grupos
@auth.requires(lambda: auth.has_membership('Administrador') or auth.has_membership ('Super'))
def usuarios():
	import numpy as np

	super =db(db.auth_group.role=="Super").select(db.auth_group.id).first()
	consulta = db(db.auth_membership.group_id != super.id).select(orderby=db.auth_membership.group_id)
	formulario = np.array([consulta])
	formulario=formulario.T

	#formulario=TABLE()

	#for registro in consulta:

	return(dict(formulario=formulario))
#Activar Servicio Correo
def VerificarSerCorreo():
	consulta=db.scheduler_task.task_name=="Servicio Correo"
	verificar=db(consulta).select().first()
	if not verificar:
		proceso=planificador.queue_task("ServicioCorreo",timeout=5000,period=60,repeats=0,
										task_name="Servicio Correo")
		return "Creado"
	return "Existe"

def ServicioCorreo():
	estado=VerificarSerCorreo()
	consulta=db.scheduler_task.task_name=="Servicio Correo"
	campos =[db.scheduler_task.application_name,
			db.scheduler_task.task_name,
			db.scheduler_task.status,
			db.scheduler_task.function_name,
			db.scheduler_task.enabled,
			db.scheduler_task.start_time
			]

	formulario=SQLFORM.grid(consulta,
				fields=campos)

	return locals()


