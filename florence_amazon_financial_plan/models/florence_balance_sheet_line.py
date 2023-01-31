from odoo import models, fields, api
import datetime


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

    def _compute_price_unit(self):
        for line in self:
            line.price_unit = 0

            if line.product_id:
                for fp in self.env["florence.fp.costs"].search([]):
                    if fp.name.id == line.product_id.id \
                            and datetime.datetime(
                        fp.date.year, fp.date.month, fp.date.day) == datetime.datetime(
                        line.name.date.year, line.name.date.month, line.name.date.day):
                        line.price_unit = fp.total
                        break
