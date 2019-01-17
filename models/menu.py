# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------
response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------
def list_menu_prefijos():
    buscar =db(db.tbl_prefijos.id>0).select()
    salida =[]
    for item in buscar:
        salida.append((item.ciudad, False, URL('default','index',vars=dict(prefijo=item.prefijo))))
    return salida

if auth.has_membership("Administrador") or auth.has_membership("Super"):
    response.menu += [
        (T('Administrar'), False, '#',[
            (T('Prefijo'), False, URL('administrar', 'prefijos')),
            (T('Correo'), False, URL('administrar', 'correo')),
            (T('Impresoras'), False, URL('administrar', 'Impresoras')),
            ])
        ]

response.menu += [
        (T('Sucursales'), False, '#',list_menu_prefijos())
        ]


_app = request.application
super=[        (T('Super'), False, '#', [
            (T('Design'), False, URL('admin', 'default', 'design/%s' % _app)),
            (T('Controller'), False,
             URL(
                 'admin', 'default', 'edit/%s/controllers/%s.py' % (_app, request.controller))),
            (T('View'), False,
             URL(
                 'admin', 'default', 'edit/%s/views/%s' % (_app, response.view))),
            (T('DB Model'), False,
             URL(
                 'admin', 'default', 'edit/%s/models/db.py' % _app)),
            (T('Menu Model'), False,
             URL(
                 'admin', 'default', 'edit/%s/models/menu.py' % _app)),
            (T('Config.ini'), False,
             URL(
                 'admin', 'default', 'edit/%s/private/appconfig.ini' % _app)),
            (T('Layout'), False,
             URL(
                 'admin', 'default', 'edit/%s/views/layout.html' % _app)),
            (T('Stylesheet'), False,
             URL(
                 'admin', 'default', 'edit/%s/static/css/web2py-bootstrap3.css' % _app)),
            (T('Database'), False, URL(_app, 'appadmin', 'index')),
            (T('Errors'), False, URL(
                'admin', 'default', 'errors/' + _app)),
            (T('About'), False, URL(
                'admin', 'default', 'about/' + _app)),
        ]),
    ]


