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


class ProductPackagingTemplateApply(models.TransientModel):
    _name = 'product.packaging.template.apply'
    _description = 'Apply Packaging Template'

    product_ids = fields.Many2many(
        comodel_name='product.product',
        string='Products',
        default=lambda self: self.default_product_ids(),
        required=True)
    overwrite = fields.Boolean(
        string='Overwrite',
        help="Check this to completely replace current packaging data.")
    template_ids = fields.Many2many(
        comodel_name='product.packaging.template',
        relation='packaging_template_apply_rel_ppt',
        string='Packaging Templates',
        help="Set this field if you want to specify a template for these products. Leave this empty to use the automatic matching functions.")
    
    @api.model
    def default_product_ids(self):
        model = self.env.context.get('active_model')
        ids = self.env.context.get('active_ids')
        if not ids:
            raise Warning(_("Can not find ids to launch Apply Packaging Template wizard!"))
        if model == 'product.template':
            products = self.env['product.product'].search([('product_tmpl_id', 'in', ids)])
        elif model == 'product.product':
            products = self.env['product.product'].browse(ids)
        else:
            raise Warning(_("Can not find model to launch Apply Packaging Template wizard!"))
        return products

    @api.one
    def apply_templates(self):
        self.product_ids.apply_packaging_templates(self.template_ids, self.overwrite)
