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
from openerp.tools.safe_eval import safe_eval
import time
import datetime
import dateutil
import pytz

common_eval_vars = """
Available variables:
* env: Odoo environment.
* time: time python module.
* datetime: datetime python module.
* dateutil: dateutil python module.
* timezone: pytz.timezone python module."""


import logging
_logger = logging.getLogger(__name__)

class product_product(models.Model):
    _inherit = 'product.product'

    action_ids = fields.One2many(comodel_name='product.action',inverse_name='product_id',)
    @api.one
    def _action_no(self):
        self.action_no = len(self.action_ids)
    action_no = fields.Integer(compute='_action_no',string='Actions')
    
class product_action(models.Model):
    _name = 'product.action'

    product_id = fields.Many2one(comodel_name="product.product")
    date = fields.Date(required=True)
    action_type = fields.Selection([('sale_ok','Can be Sold'),('state','State change'),('product_manager','Product Manager'),('code','Code')])
    @api.one
    def _action_str(self):
        if self.action_type == 'sale_ok':
            self.action_str = _('On') if self.onoff else _('Off')
        if self.action_type == 'state':
            _logger.warn([text for type,text in self.fields_get(['state'])['state']['selection'] if type == 'draft'])
            self.action_str = [text for type,text in self.fields_get(['state'])['state']['selection'] if type == self.state][0] if self.state else ''
        if self.action_type == 'product_manager':
            self.action_str = self.product_manager.name if self.product_manager else ''
        if self.action_type == 'code':
            self.action_str = self.code[:25] if self.code else ''
    action_str = fields.Char(string="Action",compute='_action_str')
    product_manager = fields.Many2one(comodel_name="res.users")
    code = fields.Text(string='Code', help="Python code that will be executed. Any variables defined here will be available during code evaluation.\n%s\n*" % common_eval_vars)
    onoff =   fields.Boolean(string="New state")
    state =   fields.Selection(selection=[('draft', 'In Development'),('sellable','Normal'),('end','End of Lifecycle'),('obsolete','Obsolete')],string="New state")

    @api.model
    def get_eval_context(self, **kw):
        context = {
            # python libs
            'time': time,
            'datetime': datetime,
            'dateutil': dateutil,
            # NOTE: only `timezone` function. Do not provide the whole `pytz` module as users
            #       will have access to `pytz.os` and `pytz.sys` to do nasty things...
            'timezone': pytz.timezone,
            # orm
            'env': self.env,
        }
        context.update(kw)
        return context

    @api.one
    def do_action(self):
        if self.action_type == 'sale_ok':
            self.product_id.sale_ok = self.onoff
        if self.action_type == 'product_manager':
            self.product_id.product_manager = self.product_manager
        if self.action_type == 'state':
            self.product_id.state = self.state
        if self.action_type == 'code':
            safe_eval(self.code, self.get_eval_context(),mode='exec')
        
    @api.model
    def cron_job(self):
        _logger.error('---->>>> cron for product.action')
        for action in self.env['product.action'].search([('date','=',fields.Date.today())]):
         
            action_type = [text for type,text in action.fields_get(['action_type'])['action_type']['selection'] if type == action.action_type][0] if action.action_type else ''
            try:
                self.do_action()
                self.env['mail.message'].create({
                    'body': _("{type} <a href='/web#model={model}&id={id}'>action</a> was successfully fired ({action_str})\n").format(type=action_type,model=action._name,id=action.id,action_str=action.action_str),
                    'subject': 'Product Action %s' % action_type,
                    'author_id': self.env['res.users'].browse(self.env.uid).partner_id.id,
                    'res_id': action.product_id.id,
                    'model': action.product_id._name,
                    'type': 'notification',})
            except Exception as e:
                self.env['mail.message'].create({
                    'body': _("Error {error} occured with {type} <a href='/web#model={model}&id={id}'>action</a> fired\n").format(type=action_type,error=e,model=action._name,id=action.id),
                    'subject': 'Product Action %s' % action_type,
                    'author_id': self.env['res.users'].browse(self.env.uid).partner_id.id,
                    'res_id': action.product_id.id,
                    'model': action.product_id._name,
                    'type': 'notification',})
