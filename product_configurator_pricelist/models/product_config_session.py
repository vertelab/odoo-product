from odoo import api, fields, models
from odoo.tools import float_round


class ProductConfigSession(models.Model):
    _inherit = "product.config.session"

    def _get_session_pricelist(self):
        self.ensure_one()
        sale_line = self.env["sale.order.line"].search(
            [("config_session_id", "=", self.id)], limit=1
        )
        if sale_line and sale_line.order_id.pricelist_id:
            return sale_line.order_id.pricelist_id
        default_order_id = self.env.context.get("default_order_id")
        if default_order_id:
            order = self.env["sale.order"].browse(default_order_id)
            if order.pricelist_id:
                return order.pricelist_id
        partner = self._get_session_partner()
        if partner.property_product_pricelist:
            return partner.property_product_pricelist
        return self.env.user.property_product_pricelist

    @api.depends("product_tmpl_id")
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

    def _get_session_partner(self):
        self.ensure_one()
        sale_line = self.env["sale.order.line"].search(
            [("config_session_id", "=", self.id)], limit=1
        )
        if sale_line and sale_line.order_id.partner_id:
            return sale_line.order_id.partner_id
        default_order_id = self.env.context.get("default_order_id")
        if default_order_id:
            order = self.env["sale.order"].browse(default_order_id)
            if order.partner_id:
                return order.partner_id
        return self.env.user.partner_id

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
                partner = session._get_session_partner()
                price = session.get_cfg_price(pricelist=pricelist, partner=partner)
                if pricelist:
                    session.currency_id = pricelist.currency_id
            else:
                price = 0.00
            session.price = price

    def get_cfg_price(self, value_ids=None, custom_vals=None, pricelist=None, partner=None, date=None, quantity=1.0):
        product_tmpl = self.product_tmpl_id

        if value_ids is None:
            value_ids = self.value_ids.ids

        if not pricelist:
            pricelist = self._get_session_pricelist()

        if not partner:
            partner = self._get_session_partner()

        if not date:
            date = fields.Date.today()

        ptav_lines = self.env["product.template.attribute.value"].search([
            ("product_attribute_value_id", "in", value_ids),
            ("product_tmpl_id", "=", product_tmpl.id),
        ])
        base_product = product_tmpl._get_variant_for_combination(ptav_lines) or product_tmpl.product_variant_id
        if pricelist and base_product:
            base_price = pricelist._get_product_price(
                base_product, quantity, date=date
            )
        else:
            base_price = product_tmpl.list_price

        attr_val_obj = self.env["product.attribute.value"]
        av_ids = attr_val_obj.browse(value_ids)
        extra_prices = attr_val_obj.get_attribute_value_extra_prices(
            product_tmpl_id=product_tmpl.id,
            pt_attr_value_ids=av_ids,
            pricelist=pricelist,
            partner=partner,
            date=date,
            quantity=quantity,
        )
        price_extra = sum(extra_prices.values())

        total = base_price + price_extra
        price_precision = self.env["decimal.precision"].precision_get("Product Price")
        total = float_round(total, precision_digits=price_precision)

        return total
