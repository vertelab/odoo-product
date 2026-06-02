from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends(
        "config_session_id",
        "config_session_id.value_ids",
        "config_session_id.product_tmpl_id",
        "order_id.pricelist_id",
        "product_id",
        "product_uom_qty",
        "product_uom",
        "tax_id",
        "company_id",
    )
    def _compute_price_unit(self):
        for line in self:
            if line.config_session_id:
                session = line.config_session_id
                pricelist = line.order_id.pricelist_id

                qty = line.product_uom_qty or 1.0
                date = line.order_id.date_order or fields.Date.today()

                total = session.get_cfg_price(
                    pricelist=pricelist,
                    partner=line.order_id.partner_id,
                    date=date,
                    quantity=qty,
                )

                session.price = total
                if pricelist:
                    session.currency_id = pricelist.currency_id

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
