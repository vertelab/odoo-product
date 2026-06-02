from odoo import api, fields, models


class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Extra Price Product",
        help="If set, this product's pricelist price will be used "
        "as the extra price, respecting quantity discounts, "
        "currency conversions and promotions.",
    )

    use_product_price = fields.Boolean(
        string="Use product price",
        compute="_compute_use_product_price",
        store=True,
        readonly=False,
        help="If enabled, the extra price will be taken from the linked product's price.\n"
        "If disabled, the static 'price_extra' value below will be used.",
    )

    @api.depends("product_id")
    def _compute_use_product_price(self):
        for ptav in self:
            ptav.use_product_price = bool(ptav.product_id)
