from odoo import models, fields, api


class FlorenceBalanceSheet(models.Model):
    _name = "florence.balance.sheet"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Balance Sheet"

    name = fields.Char(
        required = True
    )
    products_cash = fields.Float(
        compute = "_compute_products_cash"
    )
    inventory_value = fields.Float(
        compute = "_compute_inventory_value"
    )
    amazon_products_cash = fields.Float(
        compute = "_compute_amazon_products_cash"
    )
    other_value = fields.Float(
        compute = "_compute_other_value"
    )
    balance_sheet_lines = fields.One2many(
        "florence.balance.sheet.line",
        "name"
    )
    notebook_invisible = fields.Boolean(
        default = False
    )
    balance_sheet_more_lines = fields.One2many(
        "florence.balance.sheet.more",
        "name"
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )
    total = fields.Float(
        compute = "_compute_total"
    )

    @api.depends("products_cash", "inventory_value",
                 "amazon_products_cash", "other_value")
    def _compute_total(self):
        for line in self:
            line.total = line.products_cash + line.inventory_value \
                         + line.amazon_products_cash + line.other_value

    def _compute_other_value(self):
        for line in self:
            line.other_value = 0

            if len(line.balance_sheet_more_lines) > 0:
                for balance_sheet_more_line in line.balance_sheet_more_lines:
                    line.other_value += balance_sheet_more_line.value

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

    def _compute_products_cash(self):
        for line in self:
            line.products_cash = 0

            for fp in self.env["amazon.financial.plan"].search([]):
                line.products_cash += fp.total_to_use

    def _compute_inventory_value(self):
        for line in self:
            line.inventory_value = 0

            for quant in self.env["stock.quant"].search([]):
                line.inventory_value += quant.value

    @api.depends("balance_sheet_lines")
    def _compute_amazon_products_cash(self):
        for line in self:
            line.amazon_products_cash = 0

            if len(line.balance_sheet_lines) > 0:
                for balance_sheet_line in line.balance_sheet_lines:
                    line.amazon_products_cash += \
                        balance_sheet_line.price_unit * balance_sheet_line.quantity

    def show_notebook_action(self):
        for line in self:
            line.notebook_invisible = False

    def hide_notebook_action(self):
        for line in self:
            line.notebook_invisible = True
