from odoo import fields, models


class ProductConfigSession(models.Model):
    _inherit = "product.config.session"

    def get_cfg_price(self, value_ids=None, custom_vals=None, pricelist=None):
        if pricelist is None:
            pricelist = self.env.user.property_product_pricelist

        product_tmpl = self.product_tmpl_id

        base_product = product_tmpl.product_variant_id
        if pricelist and base_product:
            base_price = pricelist._get_product_price(
                base_product,
                1.0,
                self.env.user.partner_id,
            )
        else:
            base_price = product_tmpl.list_price

        if value_ids is None:
            value_ids = self.value_ids.ids

        attr_val_obj = self.env["product.attribute.value"]
        av_ids = attr_val_obj.browse(value_ids)
        extra_prices = attr_val_obj.get_attribute_value_extra_prices(
            product_tmpl_id=product_tmpl.id,
            pt_attr_value_ids=av_ids,
            pricelist=pricelist,
        )
        price_extra = sum(extra_prices.values())

        return base_price + price_extra
