from odoo import api, fields, models


class ProductConfigSession(models.Model):
    _inherit = "product.config.session"

    def _get_session_pricelist(self):
        self.ensure_one()
        sale_line = self.env["sale.order.line"].search(
            [("config_session_id", "=", self.id)], limit=1
        )
        if sale_line and sale_line.order_id.pricelist_id:
            return sale_line.order_id.pricelist_id
        return self.env.user.property_product_pricelist

    def _compute_currency_id(self):
        main_company = self.env["res.company"]._get_main_company()
        for session in self:
            pricelist = session._get_session_pricelist()
            if pricelist:
                session.currency_id = pricelist.currency_id
            else:
                template = session.product_tmpl_id
                session.currency_id = (
                    template.company_id.sudo().currency_id.id
                    or main_company.currency_id.id
                )

    @api.depends(
        "value_ids",
        "product_tmpl_id.list_price",
        "product_tmpl_id.attribute_line_ids",
        "product_tmpl_id.attribute_line_ids.value_ids",
        "product_tmpl_id.attribute_line_ids.product_template_value_ids",
        "product_tmpl_id.attribute_line_ids.product_template_value_ids.price_extra",
    )
    def _compute_cfg_price(self):
        for session in self:
            if session.product_tmpl_id:
                pricelist = session._get_session_pricelist()
                price = session.get_cfg_price(pricelist=pricelist)
            else:
                price = 0.00
            session.price = price

    def get_cfg_price(self, value_ids=None, custom_vals=None, pricelist=None):
        if pricelist is None:
            pricelist = self._get_session_pricelist()

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

        total = base_price + price_extra

        if pricelist and self.currency_id and pricelist.currency_id != self.currency_id:
            total = pricelist.currency_id._convert(
                total,
                self.currency_id,
                product_tmpl.company_id or self.env.company,
                fields.Date.today(),
            )

        return total
