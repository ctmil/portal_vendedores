{
    'name': 'Portal - Vendedores',
    'category': 'Sales',
    'version': '0.1',
    'depends': ['base','sale','product','stock','l10nar_percepciones_manuales','account'],
    'data': [
	'security/security.xml',
	'security/ir.model.access.csv',
	'portal_view.xml',
    ],
    'demo': [
    ],
    'qweb': [],
    'installable': True,
}
