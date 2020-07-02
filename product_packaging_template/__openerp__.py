# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2016- Vertel AB (<http://vertel.se>).
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
{
    'name': 'Product Packaging Template',
    'version': '0.1',
    'summary': 'Implements a templating system for packaging.',
    'category': 'stock',
    'description': """Financed by Dermanord-Svensk Hudvård AB""",
    'author': 'Vertel AB',
        'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': ['product_packaging', 'sale'],
    'data': [
        'wizard/apply_packaging_template_view.xml',
        'views/product_view.xml',
        'views/sale_view.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
}
