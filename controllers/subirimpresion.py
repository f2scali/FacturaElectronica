# -*- coding: utf-8 -*-
'''Recepcion de impresion para procesar'''
def index():
	archivo = request.vars.archivo
	if archivo:
		proceso=planificador.queue_task("procesarfactura",
										timeout=5000,
										pvars=dict(arch=archivo),
										task_name="Subir %s" % archivo)


		resultado="Web2py proceso [%i]" % proceso
	else:
		resultado="Error: 30256.....!!!!"
	return locals() 
