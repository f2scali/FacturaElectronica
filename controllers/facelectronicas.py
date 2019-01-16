# -*- coding: utf-8 -*-

def linkimg(titulo,id,tipo,archivo):
	if archivo==None:
		return ""

	salida = A(
				SPAN(XML("&ensp;"),_class="icon magnifier icon-zoom-in glyphicon glyphicon-zoom-in"),
				titulo,
				_class='button btn btn-default btn-secondary',
				_href=URL("verimagenes",
						user_signature=True,
						vars=dict(imagen=id,tipo=tipo)
						)

			)
	return salida


def verimagenes():
	tipo=request.vars.tipo #or return "Error no existe tipo"
	idcampo=request.vars.imagen #or return "Error no existe ID"
	

def index():
	links = [
              #lambda row: linkimg("Siesa", row.id,"siesa",row.Arch Pdf),
              #lambda row: linkimg("QR",  row.id, "qr" ,row.arch_qr),
              lambda row: linkimg("XML", row.id, "xml",row.arch_xml),
              lambda row: linkimg("PDF", row.id, "pdf",row.arch_pdf),
            ]

	campos= [db.tbl_factelectronica.nrofac,
			db.tbl_factelectronica.prefijo,
			db.tbl_factelectronica.nitfac,
			db.tbl_factelectronica.empresa,
			db.tbl_factelectronica.valtot,
			#db.tbl_factelectronica.arch_qr,
			#db.tbl_factelectronica.arch_xml,
			#db.tbl_factelectronica.arch_pdf,

    		]
	formulario=SQLFORM.grid(db.tbl_factelectronica,
				links=links,
				fields=campos,
				deletable=False,
				editable=False,
				details=False,
				paginate=20,
				create=False,
				user_signature=True,
				maxtextlength=40,
				)


	return locals()

