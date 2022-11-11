from odoo import models, fields, api


class FlorenceBalanceSheetLine(models.Model):
    _name = "florence.balance.sheet.line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Balance Sheet Line"

    name = fields.Many2one(
        "florence.balance.sheet"
    )
    product_id = fields.Many2one(
        "product.product"
    )
    amazon_marketplace = fields.Selection(
        [("UK", "UK"),
         ("EU", "EU")]
    )
    quantity = fields.Float()
    price_unit = fields.Float(
        compute = "_compute_price_unit",
        digits = (12, 4)
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

    @api.depends("product_id")
    def _compute_price_unit(self):
        for line in self:
            line.price_unit = 0

            if line.product_id:
                line.price_unit = self.env["florence.fp.costs"].search(
                    [("name", "=", line.product_id.id)]
                ).total
