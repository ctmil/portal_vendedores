{
    'name': 'Portal - Vendedores',
    'category': 'Sales',
    'version': '0.1',
    'depends': ['base','account','sale','product','stock','l10nar_percepciones_manuales','account_voucher','sale_stock'],
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
