# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2017- Vertel AB (<http://vertel.se>).
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
import logging
_logger = logging.getLogger(__name__)


class object_crm_campaign(models.Model):
    _inherit = 'object.crm.campaign'

    object_id = fields.Reference(selection_add=[('product.template', 'Product Template'), ('product.product', 'Product Variant'), ('product.public.category', 'Product Category')])
    @api.one
    @api.onchange('object_id')
    def get_object_value(self):
        if self.object_id:
            if self.object_id._name == 'product.template' or self.object_id._name == 'product.product':
                self.res_id = self.object_id.id
                self.name = self.object_id.name
                self.description = self.object_id.description_sale
                self.image = self.object_id.image
            if self.object_id._name == 'product.public.category':
                self.res_id = self.object_id.id
                self.name = self.object_id.name
                self.description = self.object_id.description
                self.image = self.object_id.image
        return super(object_crm_campaign, self).get_object_value()


class product_public_category(models.Model):
    _inherit = 'product.public.category'

    description = fields.Text(string='Description')