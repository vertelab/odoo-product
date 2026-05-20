from odoo import api, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    @api.model
    def get_attribute_value_extra_prices(
        self, product_tmpl_id, pt_attr_value_ids, pricelist=None
    ):
        extra_prices = {}
        if not pricelist:
            pricelist = self.env.user.partner_id.property_product_pricelist

        ptav_lines = self.env["product.template.attribute.value"].search([
            ("product_attribute_value_id", "in", pt_attr_value_ids.ids),
            ("product_tmpl_id", "=", product_tmpl_id),
        ])
        ptav_by_attr_val = {l.product_attribute_value_id.id: l for l in ptav_lines}

        for attr_val in pt_attr_value_ids:
            extra = 0.0
            ptav = ptav_by_attr_val.get(attr_val.id)

            if ptav and ptav.product_id:
                extra = ptav.product_id.list_price
            elif attr_val.product_id:
                extra = attr_val.product_id.list_price
            elif ptav:
                extra = ptav.price_extra

            if extra:
                extra_prices[attr_val.id] = extra

        return extra_prices
