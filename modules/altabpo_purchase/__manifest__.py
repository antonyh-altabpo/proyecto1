# -*- coding: utf-8 -*-
{
    'name': "altabpo compras",

    'summary': """
        personalizaciones compras AltaBPO""",

    'description': """
         Modulo personalizaciones especificas para el modelo de Negocio
    """,
    'author': "Antony H.",
    'company': 'AltaBPO',
    'maintainer': 'Antony H. / AltaBPO',
    'website': "https://www.altabpo.com",
    'category': 'Operations/Purchase',
    'version': '13.0.1.0.0',
    'depends': ['purchase_enterprise', 'altabpo_stock'],

    'data': [
        'security/ir.model.access.csv',
        'views/purchase_statistic.xml',
        'views/account_move.xml',

    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
