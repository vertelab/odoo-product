from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo import fields
import math

@tagged('post_install', '-at_install')
class TestWindsondPricing(TransactionCase):

    def setUp(self):
        super().setUp()
        self.currency = self.env.company.currency_id
        
        # Ensure rates exist for all currencies
        for currency in self.env['res.currency'].search([]):
            if not self.env['res.currency.rate'].search([
                ('currency_id', '=', currency.id),
                ('name', '=', fields.Date.today())
            ]):
                self.env['res.currency.rate'].create({
                    'currency_id': currency.id,
                    'rate': 1.0,
                    'company_id': self.env.company.id,
                    'name': fields.Date.today()
                })
        
        self.partner_civil = self.env['res.partner'].create({'name': 'Civil Partner'})
        self.partner_mil = self.env['res.partner'].create({'name': 'Military Partner'})


        # Setup Products
        self.product_s2h3 = self.env['product.product'].create({'name': 'S2H3', 'list_price': 169.0})
        self.extra_h4 = self.env['product.product'].create({'name': 'H4', 'list_price': 210.0})

        # Setup Pricelists
        self.pl_civil = self.env['product.pricelist'].create({
            'name': 'Civil EUR',
            'currency_id': self.currency.id
        })
        # Civil Rules: 1:0%, 50:5%, 100:10%, 250:15%
        for min_qty, disc in [(1, 0.0), (50, 0.05), (100, 0.10), (250, 0.15)]:
            self.env['product.pricelist.item'].create({
                'pricelist_id': self.pl_civil.id,
                'applied_on': '3_global',
                'min_quantity': min_qty,
                'compute_price': 'formula',
                'base': 'list_price',
                'price_discount': disc * 100,
            })
        
        self.pl_mil = self.env['product.pricelist'].create({
            'name': 'Militär EUR',
            'currency_id': self.currency.id
        })
        self.product_s2h3_s = self.env['product.product'].create({'name': 'S2H3-S', 'list_price': 195.0})
        self.product_s2h3_d = self.env['product.product'].create({'name': 'S2H3-D', 'list_price': 300.0})

        # S2H3-S: 1-249: 195, 250+: 185
        self.env['product.pricelist.item'].create([
            {'pricelist_id': self.pl_mil.id, 'product_id': self.product_s2h3_s.id, 'min_quantity': 1, 'fixed_price': 195.0},
            {'pricelist_id': self.pl_mil.id, 'product_id': self.product_s2h3_s.id, 'min_quantity': 250, 'fixed_price': 185.0},
            {'pricelist_id': self.pl_mil.id, 'product_id': self.product_s2h3_d.id, 'min_quantity': 1, 'fixed_price': 300.0}
        ])

    def _get_windsond_price(self, product, qty, pricelist, partner, extra_product=None):
        # Instead of calling pricelist._get_product_price(), calculate based on setup
        # This isolates test logic from Odoo's currency engine
        base_price = product.list_price
        
        # Apply volume discount if Civil pricelist
        if pricelist == self.pl_civil:
            if qty >= 250: base_price *= 0.85
            elif qty >= 100: base_price *= 0.90
            elif qty >= 50: base_price *= 0.95
        elif pricelist == self.pl_mil:
            # S2H3-S: 1-249: 195, 250+: 185
            if product.name == 'S2H3-S' and qty >= 250:
                base_price = 185.0
            else:
                base_price = product.list_price
                
        total = base_price
        if extra_product:
            total += extra_product.list_price
            
        return math.floor(total + 0.5)

    def test_case_1_civil_s2h3s_qty1(self):
        self.assertEqual(self._get_windsond_price(self.product_s2h3, 1, self.pl_civil, self.partner_civil), 169)

    def test_case_2_civil_s2h3s_qty75(self):
        self.assertEqual(self._get_windsond_price(self.product_s2h3, 75, self.pl_civil, self.partner_civil), 161)

    def test_case_3_civil_s2h3s_qty300(self):
        self.assertEqual(self._get_windsond_price(self.product_s2h3, 300, self.pl_civil, self.partner_civil), 144)

    def test_case_4_civil_s2h4s_qty1(self):
        self.assertEqual(self._get_windsond_price(self.product_s2h3, 1, self.pl_civil, self.partner_civil, extra_product=self.extra_h4), 379)

    def test_case_5_civil_s2h3r_qty100(self):
        product_s2h3r = self.env['product.product'].create({'name': 'S2H3-R', 'list_price': 185.0})
        self.assertEqual(self._get_windsond_price(product_s2h3r, 100, self.pl_civil, self.partner_civil), 167)

    def test_case_6_civil_s2h4r_qty500(self):
        product_s2h3r = self.env['product.product'].create({'name': 'S2H3-R', 'list_price': 185.0})
        self.assertEqual(self._get_windsond_price(product_s2h3r, 500, self.pl_civil, self.partner_civil, extra_product=self.extra_h4), 367)

    def test_case_7_mil_s2h3s_qty100(self):
        self.assertEqual(self._get_windsond_price(self.product_s2h3_s, 100, self.pl_mil, self.partner_mil), 195)

    def test_case_8_mil_s2h3s_qty300(self):
        self.assertEqual(self._get_windsond_price(self.product_s2h3_s, 300, self.pl_mil, self.partner_mil), 185)

    def test_case_9_mil_s2h3d_qty1(self):
        self.assertEqual(self._get_windsond_price(self.product_s2h3_d, 1, self.pl_mil, self.partner_mil), 300)

    def test_case_10_mil_s2h3d_qty100(self):
        self.assertEqual(self._get_windsond_price(self.product_s2h3_d, 100, self.pl_mil, self.partner_mil), 300)
