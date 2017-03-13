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

class crm_tracking_campaign(models.Model):
    _inherit = 'crm.tracking.campaign'

    color = fields.Integer('Color Index')
    date_start = fields.Date(string='Start Date')
    date_stop = fields.Date(string='Start Stop')
    product_ids = fields.One2many(comodel_name='product.crm.campaign', inverse_name='campaign_id', string='Products')
    description = fields.Text(string = 'Description')
    @api.one
    def _product_names(self):
        self.product_names = ', '.join(self.product_ids.mapped('name'))
    product_names = fields.Char(compute='_product_names')
    @api.one
    def _product_count(self):
        self.product_count = len(self.product_ids)
    product_count = fields.Integer(compute='_product_count')


class product_crm_campaign(models.Model):
    _name = 'product.crm.campaign'

    name = fields.Char(related='product_id.name')
    sequence = fields.Integer(string='Sequence')
    color = fields.Integer('Color Index')
    product_categ_id = fields.Many2one(comodel_name='product.category', related='product_id.categ_id', string='Category', store=True)
    campaign_id = fields.Many2one(comodel_name='crm.tracking.campaign', string='Campaign')
    product_id = fields.Many2one(comodel_name='product.template', string='Product')


class product_template(models.Model):
    _inherit = 'product.template'

    campaign_ids = fields.One2many(comodel_name='product.crm.campaign', inverse_name='product_id', string='Campaigns')
