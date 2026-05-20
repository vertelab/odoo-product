from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends(
        "config_session_id",
        "config_session_id.price",
        "tax_id",
        "company_id",
    )
    def _compute_price_unit(self):
        for line in self:
            if line.config_session_id:
                line.price_unit = self.env[
                    "account.tax"
                ]._fix_tax_included_price_company(
                    line.config_session_id.price,
                    line.product_id.taxes_id,
                    line.tax_id,
                    line.company_id,
                )
            else:
                super(SaleOrderLine, line)._compute_price_unit()
