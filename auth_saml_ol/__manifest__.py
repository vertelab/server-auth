# Copyright (C) 2010-2016 XCG Consulting <http://odoo.consulting>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Saml2 Authentication Onelogin',
    'version': '12.0.1.0.0',
    'category': 'Tools',
    'author': 'Vertel AB, XCG Consulting, Odoo Community Association (OCA)',
    'website': 'https://vertel.se',
    'license': 'AGPL-3',
    'depends': [
        'base_setup',
        'web',
    ],
    "external_dependencies": {
        "python": ["onelogin"],
    },
    "demo": [
        'demo/auth_saml.xml',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/auth_saml.xml',
        'views/base_settings.xml',
        'views/res_users.xml',
    ],
    'installable': True,
    'auto_install': False,
}
