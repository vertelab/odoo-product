from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends(
        "config_session_id",
        "config_session_id.product_id",
        "product_id",
        "product_uom",
        "product_uom_qty",
        "tax_id",
        "company_id",
        "order_id",
    )
    def _compute_price_unit(self):
        for line in self:
            if line.config_session_id:
                if line.product_id and line.order_id.pricelist_id:
                    partner = line.order_id.partner_id
                    price = line.order_id.pricelist_id._get_product_price(
                        line.product_id,
                        line.product_uom_qty or 1.0,
                        partner,
                        date=line.order_id.date_order
                        or fields.Date.context_today(line),
                        uom_id=line.product_uom.id if line.product_uom else False,
                    )
                else:
                    price = line.config_session_id.price
                line.price_unit = self.env[
                    "account.tax"
                ]._fix_tax_included_price_company(
                    price,
                    line.product_id.taxes_id,
                    line.tax_id,
                    line.company_id,
                )
            else:
                super(SaleOrderLine, line)._compute_price_unit()
