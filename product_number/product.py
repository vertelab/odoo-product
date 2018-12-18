# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2004-2018 Vertel AB (<http://vertel.se>).
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

from odoo import api, models, fields, _
import logging
_logger = logging.getLogger(__name__)

class product_product(models.Model):
    _inherit ='product.product'

    @api.model
    def generate_new_product_no(self):
        return self.env['ir.sequence'].get('product.product.no')

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        if not vals.get('default_code'):
            vals['default_code'] = self.generate_new_product_no()
        return super(product_product, self).create(vals)