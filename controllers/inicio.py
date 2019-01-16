# -*- coding: utf-8 -*-
def index():

	id_usuario=db.auth_user.insert(first_name="Administrador",
									last_name="Sistema",
									email="admin@gmail.com",
									username="admin",
									password=db.auth_user.password.validate("12345")[0]) 
	id_grupo=auth.add_group('Administrador', 'Parametrizacion de la aplicación')
	auth.add_membership(id_grupo, id_usuario)
	id_usuario=db.auth_user.insert(first_name="super",
									last_name="admin",
									email="soportesimplesoft@gmail.com",
									username="super",
									password=db.auth_user.password.validate("Tetero.2018")[0]) 
	id_grupo=auth.add_group('super', 'Control aplicación')
	auth.add_membership(id_grupo, id_usuario)
