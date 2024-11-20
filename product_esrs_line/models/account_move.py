from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'scaffold_test.scaffold_test'

    def action_post(self):

        self.create_esrs_line_transactions()

        super(AccountMove,self).action_post()

    def create_esrs_line_transactions(self):
        self.ensure_one()            
        
        self.env["esrs.line"].search([("account_move_id", "=", self.id),("is_computed", "=", True)]).unlink()

        total_quantity = {}

        for account_move_line_id in self.invoice_line_ids:

            for product_esrs_line_id in account_move_line_id.product_id.product_esrs_line_ids:

                if total_quantity.get(str(product_esrs_line_id.document_csrd_id.id)):
                    total_quantity[str(product_esrs_line_id.document_csrd_id.id)] = total_quantity[str(product_esrs_line_id.document_csrd_id.id)] + (product_esrs_line_id.quantity * account_move_line_id.quantity)

                else:
                    total_quantity[str(product_esrs_line_id.document_csrd_id.id)] = (product_esrs_line_id.quantity * account_move_line_id.quantity)


        for document_csrd_id, quantity in total_quantity.items():

            new_esrs_line = \
            {
                "document_csrd_id": int(document_csrd_id),
                "quantity": quantity,
                "is_computed": True,
            }

            new_record = self.env["esrs.line"].create(new_esrs_line)

            self.esrs_line_ids = [(4,new_record.id)]

