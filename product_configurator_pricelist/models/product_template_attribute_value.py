from odoo import api, fields, models


class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Extra Price Product",
        help="If set, this product's list price will be used "
        "as the extra price instead of the fixed price_extra.",
    )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.price_extra = self.product_id.list_price
