# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2019- Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

import logging
_logger = logging.getLogger(__name__)

class product_product(models.Model):
    _inherit='product.product'

    packaging_ids = fields.One2many(comodel_name='product.packaging', inverse_name='product_id', string='Logistical Units',
        help="Gives the different ways to package the same product. This has no impact on the picking order and is mainly used if you use the EDI module.")

class product_packaging(models.Model):
    _inherit='product.packaging'

    product_id = fields.Many2one(comodel_name='product.product')
    
    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        if not vals.get('product_tmpl_id') and vals.get('product_id'):
            vals['product_tmpl_id'] = self.env['product.template'].search_read([('product_variant_ids', '=', vals['product_id'])], ['id'])[0]['id']
        return super(product_packaging, self).create(vals)
        


    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
