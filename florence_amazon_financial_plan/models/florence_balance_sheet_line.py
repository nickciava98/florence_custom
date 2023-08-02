import calendar

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
        compute="_compute_price_unit",
        digits=(12, 4)
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="name.currency_id",
        store=True
    )

    @api.depends("name.date", "product_id")
    def _compute_price_unit(self):
        for line in self:
            line.price_unit = .0

            if line.product_id and line.name.date:
                year = str(line.name.date.year)
                month = str(line.name.date.month)
                last_day = str(calendar.monthrange(int(year), int(month))[1])
                date_from = year + "-" + month + "-01"
                date_to = year + "-" + month + "-" + last_day
                fp_cost_id = self.env["florence.fp.costs"].search(
                    ["&", "&", ("name", "=", line.product_id.id), ("date", ">=", date_from), ("date", "<=", date_to)],
                    limit=1
                )
                line.price_unit = fp_cost_id.total
