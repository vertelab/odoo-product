# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2017 Vertel AB (<http://vertel.se>).
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
import logging
_logger = logging.getLogger(__name__)

class product_template(models.Model):
    _inherit = 'product.template'

    company_info_name = fields.Char(compute='_company_info')
    company_info_street = fields.Char(compute='_company_info')
    company_info_city = fields.Char(compute='_company_info')
    company_info_state = fields.Char(compute='_company_info')
    company_info_zip = fields.Char(compute='_company_info')
    company_info_country = fields.Char(compute='_company_info')
    company_info_phone = fields.Char(compute='_company_info')
    company_info_email = fields.Char(compute='_company_info')
    company_info_website = fields.Char(compute='_company_info')

    @api.one
    def _company_info(self):
        self.company_info_name = self.company_id.name
        self.company_info_street = self.company_id.street if self.company_id.street else ''
        self.company_info_city = self.company_id.city if self.company_id.city else ''
        self.company_info_state = self.company_id.state_id.name if self.company_id.state_id else ''
        self.company_info_zip = self.company_id.zip if self.company_id.zip else ''
        self.company_info_country = self.company_id.country_id.name if self.company_id.country_id else ''
        self.company_info_phone = self.company_id.phone if self.company_id.phone else ''
        self.company_info_email = self.company_id.email if self.company_id.email else ''
        self.company_info_website = self.company_id.website if self.company_id.website else ''
