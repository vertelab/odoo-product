# -*- coding: utf-8 -*-
{
    'name': "product_variant_parent_link",

    'summary': """
        links from product variant to product
    """,

    'description': """
        links from product variant to product \n
        v14.0.0.0.1 initial version
    """,

    'author': "Vertel AB",
    'website': "https://vertel.se",
    'license': "AGPL-3",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
