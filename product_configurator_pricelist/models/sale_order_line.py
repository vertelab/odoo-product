from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends(
        "config_session_id",
        "config_session_id.value_ids",
        "config_session_id.product_tmpl_id",
        "order_id.pricelist_id",
        "tax_id",
        "company_id",
    )
    def _compute_price_unit(self):
        for line in self:
            if line.config_session_id:
                session = line.config_session_id
                product_tmpl = session.product_tmpl_id
                pricelist = line.order_id.pricelist_id

                base_product = product_tmpl.product_variant_id
                if pricelist and base_product:
                    base_price = pricelist._get_product_price(
                        base_product,
                        1.0,
                        line.order_id.partner_id,
                    )
                else:
                    base_price = product_tmpl.list_price

                attr_val_obj = self.env["product.attribute.value"]
                av_ids = session.value_ids
                extra_prices = attr_val_obj.get_attribute_value_extra_prices(
                    product_tmpl_id=product_tmpl.id,
                    pt_attr_value_ids=av_ids,
                    pricelist=pricelist,
                    partner=line.order_id.partner_id,
                )
                price_extra = sum(extra_prices.values())

                total = base_price + price_extra

                if pricelist and session.currency_id and pricelist.currency_id != session.currency_id:
                    total = pricelist.currency_id._convert(
                        total,
                        session.currency_id,
                        product_tmpl.company_id or line.company_id,
                        fields.Date.today(),
                    )

                line.price_unit = self.env[
                    "account.tax"
                ]._fix_tax_included_price_company(
                    total,
                    line.product_id.taxes_id,
                    line.tax_id,
                    line.company_id,
                )
            else:
                super(SaleOrderLine, line)._compute_price_unit()
