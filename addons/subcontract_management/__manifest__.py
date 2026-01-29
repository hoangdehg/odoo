{
    'name': 'Subcontract Management',
    'version': '1.0',
    'summary': 'Manage subcontract orders and materials',
    'description': 'A minimal module for subcontract management',
    'category': 'Subcontract Management',
    'author': 'AZ',
    'depends': ['base', 'stock', 'product'],
    'data': ['views/subcontract_order_views.xml', 'security/ir.model.access.csv', 
             'views/subcontract_order_menus.xml'],   
    'installable': True,
    'application': True,
}
