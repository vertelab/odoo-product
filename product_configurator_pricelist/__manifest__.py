{
    'name': 'Product: Configurator Pricelist',
    'version': '18.0.1.0.0',
    'summary': 'Apply pricelists to products created with OCA product configurator.',
    'description': '''
Configurator Pricelist
======================

    Bridges OCA's product_configurator with Odoo's pricelist engine.
            Pricelist rules now apply to configured products both during
            configuration and on sale order lines.

    Features:

        - UI Integration: Extends 1 view(s) in the Odoo interface.
        - Extends Odoo: Builds on product.attribute.value, product.config.session, product.product, product.template.attribute.value.
    ''',
    'category': 'Sales',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-product/product_configurator_pricelist',
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
