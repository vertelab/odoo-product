from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class ESRSLine(models.Model):
    _inherit = 'esrs.line'
    _description = 'scaffold_test.scaffold_test'

    is_computed = fields.Boolean()

 