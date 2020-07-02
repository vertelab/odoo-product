# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2020- Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
import openerp.exceptions

import logging
_logger = logging.getLogger(__name__)

class ProductPackaging(models.Model):
    _inherit = 'product.packaging'
    
    packaging_template_id = fields.Many2one(comodel_name='product.packaging.template', string='Packaging Template')
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='Unit of Measure',
        help="The unit of measure representing this package.")

class ProductPackagingTemplate(models.Model):
    _name = 'product.packaging.template'
    _description = 'Packaging Template'
    _order = 'priority DESC'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    # Package data
    qty = fields.Float(string='Quantity by Package', required=True)
    ul = fields.Many2one(
        comodel_name='product.ul',
        string='Package Logistic Unit',
        required=True)
    # Pallet data
    ul_container = fields.Many2one(
        comodel_name='product.ul',
        string='Pallet Logistic Unit')
    ul_qty = fields.Integer(string='Package by layer')
    rows = fields.Integer(string='Number of layers', required=True)
    weight = fields.Float(string='Total Package Weight')
    # Product matching data
    priority = fields.Integer(
        string='Priority',
        help="Decides priority of packaging templates.",
        default=20)
    sequence = fields.Integer(
        string='Sequence',
        help="Gives the sequence order when displaying a list of packaging.",
        default=1)
    allow_multiple = fields.Boolean(
        string='Allow Multiple Package Types',
        help="Check this box if this package type if this package should be allowed "
        "to be used among others. Leave empty if this must be the only package.")
    volume = fields.Float(string='Volume')
    # DFP data
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='Unit of Measure',
        help="The unit of measure representing this package.")

    @api.model
    def match_packaging_template(self, product):
        """Match a product to a packaging template."""
        result = self.browse()
        for template in self.search(self._match_packaging_template_domain(product)):
            if not template.allow_multiple:
                if not result:
                    # First match doesn't allow multiple packages. No need to look further.
                    return template
                # This match doesn't allow multiple packages, but isn't foirst match. Ignore it.
            else:
                # This match allows multiple. Add it to the result set.
                result |= template
        return result
    
    @api.model
    def _match_packaging_template_domain(self, product):
        """Return a domain to match a product to packaging templates."""
        return [('volume', '=', product.volume)]

    @api.multi
    def _apply_packaging_template_domain(self, product):
        """Return a domain to find package data that matches this template."""
        return [
            ('name', '=', self.description),
            ('qty', '=', self.qty),
            ('ul', '=', self.ul.id),
            ('ul_container', '=', self.ul_container.id),
            ('ul_qty', '=', self.ul_qty),
            ('rows', '=', self.rows),
            ('weight', '=', self.weight),
            ('uom_id', '=', self.uom_id.id),
            ('product_id', '=', product.id),
            ('product_tmpl_id', '=', False),
        ]

    @api.multi
    def _apply_packaging_template_values(self, product):
        """Return the create/write values for this packaging template."""
        return {
            'name': self.description,
            'qty': self.qty,
            'ul': self.ul.id,
            'ul_container': self.ul_container.id,
            'ul_qty': self.ul_qty,
            'rows': self.rows,
            'weight': self.weight,
            'uom_id': self.uom_id.id,
            'packaging_template_id': self.id,
            'product_id': product.id,
            'product_tmpl_id': product.product_tmpl_id.id,
        }

    @api.multi
    def apply_packaging_template(self, product):
        """Apply a packaging template to a product.
        :param product: The product to update packaging data for.
        """
        values = self._apply_packaging_template_values(product)
        # Try to find package created from this template
        packaging = self.env['product.packaging'].search(
            [
                ('packaging_template_id', '=', self.id),
                ('product_id', '=', product.id),
                ('product_tmpl_id', '=', product.product_tmpl_id.id),
            ], limit=1)
        if not packaging:
            # Try to find a package that matches this template
            domain = self._apply_packaging_template_domain(product)
            packaging = self.env['product.packaging'].search(domain, limit=1)
        if packaging:
            packaging.write(values)
        else:
            packaging.create(values)
        return packaging

    @api.model
    def apply_packaging_templates(self, product, templates=None, clear=False):
        """Apply all matching packaging templates to a product.
        :param product: The product to update packaging data for.
        :param templates: Specific templates to apply. Will override automatic matching.
        :param clear: Set to True to clear any other packaging data from this product.
        """
        # Find templates
        templates = templates or self.match_packaging_template(product)
        if not templates:
            return
        packagings = self.env['product.packaging']
        # Apply templates
        for template in templates:
            packagings |= template.apply_packaging_template(product)
        if clear:
            # Clear extra packaging data
            extra_packaging = packagings.search([
                ('id', 'not in', packagings._ids),
                ('product_id', '=', product.id),
                ('product_tmpl_id', '=', product.product_tmpl_id.id)])
            if extra_packaging:
                extra_packaging.unlink()
    
    @api.one
    def update_packaging_data(self):
        """Update all packaging data connected to this template."""
        products = self.env['product.product'].search([
            ('packaging_ids.packaging_template_id', '=', self.id)])
        for product in products:
            self.apply_packaging_templates(product, self)

class Product(models.Model):
    _inherit='product.product'

    uom_ids = fields.Many2many(comodel_name='product.uom', string='Units of Measure', compute='_compute_uom_ids', store=True)

    @api.one
    @api.depends('uom_id', 'packaging_ids.uom_id')
    def _compute_uom_ids(self):
        """Limit available UoMs to packaging UoMs or same category as default UoM if
        packaging data is missing."""
        uoms = self.env['product.uom']
        uoms |= self.uom_id
        packaging_uoms = self.mapped('packaging_ids.uom_id')
        if packaging_uoms:
            uoms |= packaging_uoms
        else:
            uoms |= self.env['product.uom'].search(
                [('category_id', '=', self.uom_id.category_id.id)])
        self.uom_ids = uoms

    @api.multi
    def apply_packaging_templates(self, templates=None, clear=False):
        packaging_template = self.env['product.packaging.template']
        for product in self:
            packaging_template.apply_packaging_templates(product, templates, clear)
