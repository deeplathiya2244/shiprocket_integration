# -*- coding: utf-8 -*-
{
    'name': "Laxicon Shiprocket",
    'version': "1.1",
    'sequence': 1,
    'description': "Shiprocket Integration platform.",
    'summary': "The Shiprocket API",
    'author': 'Laxicon Solution',
    'website': "https://www.laxicon.in",
    'depends': ['sale'],
    'data': [
        # data
        'data/data.xml',
        # Security
        'security/ir.model.access.csv',
        # Wizards
        # Views
        'views/authenticate_view.xml',
        'views/dashboard.xml',
        'views/order_inherited_view.xml',
        'views/channel_data.xml',
        # Reports
        # Menus
        'views/menus.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
