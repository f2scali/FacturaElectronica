# -*- coding: utf-8 -*-
db.define_table('tbl_factelectronica', 
		Field('nrofac','integer',unique=True, label="Nro. Factura"),
		Field('prefijo'),
		Field('fecfac'),
		Field('nitfac'),
		Field('docadq', label="Nit Cliente"),
		Field('valfac','double'),
		Field('valiva','double'),
		Field('valtot','double', label="Valor Total"),
		Field('valimp','double'),
		Field('valdctos','double'),
		Field('valretica','double'),
		Field('valretfte','double'),
		Field("son"),
		Field("ciiu"),
		Field('cufe'),
		Field('arch_xml','upload'),
		Field('arch_pdf','upload'),
		Field('arch_siesa','upload'),
		Field('arch_qr','upload'),
		Field('empresa'),
		Field('representante'),
		Field('telefono'),
		Field('direccion'),
		Field('ciudad'),
		Field('barrio'),
		Field('observaciones','text'),
		Field('resolucion','text'),
		Field('estado',requires=IS_IN_SET(('Electronica', 'Cguno', 'Imprimir','Impresa'))),
		Field("rutaimgs"),
		Field("formulario"),
		Field("direccion_gen"),
		Field("telefono_gen"),
		auth.signature,
		)

db.define_table('tbl_detalle', 
		Field('idfact','reference tbl_factelectronica'),
		Field('item'),
		Field('detalle'),
		Field('detalle1','text'),
		Field('cantidad','double'),
		Field('unitario','double'),
		Field('valortotal','double'),
		auth.signature,
		)

db.define_table("tbl_novedades",
		Field('idfact','reference tbl_factelectronica'),
		Field('novedad','text'),
		Field('propietario','reference auth_user'),
		Field('vista',"boolean",default=False),
		Field('hijo','reference tbl_novedades'),
		auth.signature,
	)

db.define_table("tbl_prefijos",
		Field("ciudad",required=True,unique=True,requires=IS_NOT_EMPTY()),
		Field("prefijo",required=True,unique=True,requires=IS_NOT_EMPTY()),
		auth.signature,
		format="%(ciudad)s - [%(prefijo)s]"
		)
db.define_table("tbl_rangos",
		Field('id_prefijos','reference tbl_prefijos',label='Ciudad - [prefijo]'),
		Field("inicio","integer",required=True,label="Rango Inicial",requires=IS_NOT_EMPTY()),
		Field("fin","integer",required=True,label="Rango Final",requires=IS_NOT_EMPTY()),
		auth.signature,
		)


db.tbl_factelectronica.arch_pdf.represent= lambda valor,registro:\
	A("Ver imagen",_href=URL('donwload',args=valor))

db.define_table("tbl_impresoras",
	Field("nombre",label="Descripción"),
	Field("ruta",label="Impresora")
	)

db.define_table("tbl_correo",
		Field("servidor",required=True,requires=IS_NOT_EMPTY()),
		Field("puerto",'integer',default=23,requires=IS_NOT_EMPTY()),
		Field("usuario",required=True,requires=IS_NOT_EMPTY()),
		Field("password",required=True,requires=IS_NOT_EMPTY()),
		Field("bandeja",default="INBOX",requires=IS_NOT_EMPTY()),
		Field("activarssl","boolean",default=False,label="Activar SSL"),
		auth.signature,
		)


#db.tbl_factelectronica.truncate()
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
