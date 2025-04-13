# -*- coding: utf-8 -*-
{
    'name': 'Zoo City +',
    'summary': """Zoo City Tutorials""",
    'description': """Building my own zoo city +""",
    'author': 'minhng.info',
    'maintainer': 'minhng.info',
    'website': 'https://minhng.info',
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'zoo',
        'sale_management', # <-- depends on zoo addon
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/zoo_animal_views.xml',
    ],
    'demo': [],
    'css': [],
    # 'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}