from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo import fields

@tagged('post_install', '-at_install')
class TestUseProductPriceFlag(TransactionCase):

    def setUp(self):
        super().setUp()
        # Create a product template with attributes
        self.attr_color = self.env['product.attribute'].create({
            'name': 'Color',
            'create_variant': 'always',
        })
        self.val_red = self.env['product.attribute.value'].create({
            'name': 'Red',
            'attribute_id': self.attr_color.id,
        })
        self.val_blue = self.env['product.attribute.value'].create({
            'name': 'Blue',
            'attribute_id': self.attr_color.id,
        })

        self.product_tmpl = self.env['product.template'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'attribute_line_ids': [(0, 0, {
                'attribute_id': self.attr_color.id,
                'value_ids': [(6, 0, [self.val_red.id, self.val_blue.id])],
            })],
        })

        # Get PTAVs
        self.ptav_red = self.env['product.template.attribute.value'].search([
            ('product_tmpl_id', '=', self.product_tmpl.id),
            ('product_attribute_value_id', '=', self.val_red.id),
        ])
        self.ptav_blue = self.env['product.template.attribute.value'].search([
            ('product_tmpl_id', '=', self.product_tmpl.id),
            ('product_attribute_value_id', '=', self.val_blue.id),
        ])

        # Create a linked product for extra pricing
        self.extra_product = self.env['product.product'].create({
            'name': 'Extra Product',
            'list_price': 50.0,
        })

        # Set up a pricelist
        self.pricelist = self.env['product.pricelist'].create({
            'name': 'Test Pricelist',
            'currency_id': self.env.company.currency_id.id,
        })

    def test_static_price_extra_when_flag_disabled(self):
        """When use_product_price=False, extra price should come from static price_extra."""
        self.ptav_red.write({
            'price_extra': 25.0,
            'use_product_price': False,
            'product_id': False,
        })

        extra_prices = self.env['product.attribute.value'].get_attribute_value_extra_prices(
            product_tmpl_id=self.product_tmpl.id,
            pt_attr_value_ids=self.val_red,
            pricelist=self.pricelist,
        )
        self.assertEqual(extra_prices.get(self.val_red.id), 25.0)

    def test_product_price_when_flag_enabled(self):
        """When use_product_price=True and product_id set, extra price should come from product."""
        self.ptav_red.write({
            'price_extra': 10.0,
            'use_product_price': True,
            'product_id': self.extra_product.id,
        })

        extra_prices = self.env['product.attribute.value'].get_attribute_value_extra_prices(
            product_tmpl_id=self.product_tmpl.id,
            pt_attr_value_ids=self.val_red,
            pricelist=self.pricelist,
        )
        self.assertEqual(extra_prices.get(self.val_red.id), 50.0)

    def test_compute_flag_true_when_product_set(self):
        """Test that setting product_id computes use_product_price=True."""
        ptav = self.ptav_blue
        ptav.product_id = self.extra_product
        # Recompute
        ptav._compute_use_product_price()
        self.assertTrue(ptav.use_product_price)

    def test_compute_flag_false_when_product_cleared(self):
        """Test that clearing product_id computes use_product_price=False."""
        ptav = self.ptav_blue
        ptav.write({'product_id': self.extra_product.id})
        ptav._compute_use_product_price()
        self.assertTrue(ptav.use_product_price)

        ptav.product_id = False
        ptav._compute_use_product_price()
        self.assertFalse(ptav.use_product_price)

    def test_variant_price_extra_computed_correctly(self):
        """End-to-end test that product.product.price_extra reflects the flag."""
        self.ptav_red.write({
            'price_extra': 30.0,
            'use_product_price': False,
            'product_id': False,
        })
        self.ptav_blue.write({
            'price_extra': 0.0,
            'use_product_price': True,
            'product_id': self.extra_product.id,
        })

        # Get variant with red
        red_variant = self.product_tmpl._get_variant_for_combination(self.ptav_red)
        blue_variant = self.product_tmpl._get_variant_for_combination(self.ptav_blue)

        if red_variant:
            red_variant.invalidate_cache(['price_extra'])
            self.assertEqual(red_variant.price_extra, 30.0)

        if blue_variant:
            blue_variant.invalidate_cache(['price_extra'])
            self.assertEqual(blue_variant.price_extra, 50.0)
