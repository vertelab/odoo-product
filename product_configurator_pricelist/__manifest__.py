{
    'name': 'Product: Configurator Pricelist',
    'version': '1.0',
    'summary': 'Apply pricelists to products created with OCA product configurator',
    'description': """
        Bridges OCA's product_configurator with Odoo's pricelist engine.
        Pricelist rules now apply to configured products both during
        configuration and on sale order lines.
    """,
    'category': 'Sales',
    'author': 'Vertel AB',
    'website': 'https://vertel.se',
    'license': 'AGPL-3',
    'depends': [
        'product_configurator',
        'product_configurator_sale',
        'sale',
        'product',
    ],
    'data': [
        'views/product_attribute_value_views.xml',
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'auto_install': False,
}
