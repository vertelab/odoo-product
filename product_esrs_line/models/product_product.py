from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'scaffold_test.scaffold_test'

    product_esrs_line_ids = fields.One2many(comodel_name="product.esrs.line",inverse_name="product_id")