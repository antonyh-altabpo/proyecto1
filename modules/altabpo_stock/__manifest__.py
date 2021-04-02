# -*- coding: utf-8 -*-
{
    'name': "altabpo inventario",

    'summary': """
        personalizaciones inventario AltaBPO""",

    'description': """
        Modulo personalizaciones especificas para el modelo de Negocio
    """,

    'author': "Antony H.",
    'company': 'AltaBPO',
    'maintainer': 'Antony H. / AltaBPO',
    'website': "https://www.altabpo.com",
    'category': 'Warehouse',
    'version': '13.0.1.0.0',
    'depends': ['stock'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_template.xml',
    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
