# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2018 Vertel AB (<http://vertel.se>).
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
    
class product_action(models.Model):
    _inherit = 'product.action'
    
    action_type = fields.Selection(selection_add=[('website_published','Website Published')])
    onoff_website_published = fields.Boolean(string="New state")

    @api.one
    def _action_str(self):
        if self.action_type == 'website_published':
            self.action_str = _('Published') if self.onoff_website_published else _('Not published')
        else:
            super(product_action,self)._action_str()

    @api.one
    def do_action(self):
        if self.action_type == 'website_published':
            self.product_id.website_published = self.action.onoff_website_published
        else:
            super(product_action,self)._do_action()
