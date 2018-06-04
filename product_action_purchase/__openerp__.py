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

{
    'name': 'Product Action purchase',
    'version': '0.1',
    'category': 'product',
    'summary': 'Actions on products that will happen on a date (purchase)',
    'description': """
Product Action
==============

Adds purchase actions

Financed by Dermanord AB
       """,
    'author': 'Vertel AB',
    'website': 'http://www.vertel.se',
    'depends': ['product_action','purchase'],
    'data': ['product_view.xml'],
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
