import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FlorenceBalanceSheet(models.Model):
    _name = "florence.balance.sheet"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Balance Sheet"

    name = fields.Char(
        copy = False
    )
    date = fields.Date(
        default = datetime.datetime.now()
    )

    def _default_products_cash(self):
        products_cash = 0

        for fp in self.env["amazon.financial.plan"].search([]):
            products_cash += fp.total_to_use

        return products_cash

    products_cash = fields.Float(
        default = _default_products_cash,
        readonly = True,
        copy = False
    )
    inventory_value = fields.Float(
        compute = "_compute_inventory_value",
        store = True
    )
    amazon_products_cash = fields.Float(
        compute = "_compute_amazon_products_cash"
    )
    other_value = fields.Float(
        compute = "_compute_other_value"
    )
    balance_sheet_lines = fields.One2many(
        "florence.balance.sheet.line",
        "name",
        copy = True
    )
    notebook_invisible = fields.Boolean(
        default = False
    )
    balance_sheet_more_lines = fields.One2many(
        "florence.balance.sheet.more",
        "name",
        copy = True
    )

    def _default_balance_sheet_inventory_lines(self):
        balance_sheet_inventory_lines = [(5, 0, 0)]

        for item in self.env["stock.quant"].search(
                [("location_id.is_valuable_stock", "=", True)]):
            balance_sheet_inventory_lines.append((
                0, 0, {
                    "product_id": item.product_id,
                    "location_id": item.location_id,
                    "lot_id": item.lot_id,
                    "available_quantity": item.available_quantity,
                    "value": item.value,
                    "sale_ok": item.sale_ok,
                    "can_be_used": item.can_be_used
                }
            ))

        return balance_sheet_inventory_lines

    balance_sheet_inventory_lines = fields.One2many(
        "florence.balance.sheet.inventory",
        "name",
        default = _default_balance_sheet_inventory_lines
    )
    balance_sheet_inventory_more_lines = fields.One2many(
        "florence.balance.sheet.inventory.more",
        "name",
        copy = True
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )
    total = fields.Float(
        compute = "_compute_total"
    )

    @api.depends("balance_sheet_inventory_lines", "balance_sheet_inventory_more_lines")
    def _compute_inventory_value(self):
        for line in self:
            line.inventory_value = 0

            if len(line.balance_sheet_inventory_lines) > 0:
                for bs_inv_line in line.balance_sheet_inventory_lines:
                    line.inventory_value += bs_inv_line.value

            if len(line.balance_sheet_inventory_more_lines) > 0:
                for bs_inv_line in line.balance_sheet_inventory_more_lines:
                    line.inventory_value += bs_inv_line.value

    @api.depends("products_cash", "inventory_value",
                 "amazon_products_cash", "other_value")
    def _compute_total(self):
        for line in self:
            line.total = line.products_cash + line.inventory_value \
                         + line.amazon_products_cash + line.other_value

    @api.depends("balance_sheet_more_lines")
    def _compute_other_value(self):
        for line in self:
            line.other_value = 0

            if len(line.balance_sheet_more_lines) > 0:
                for balance_sheet_more_line in line.balance_sheet_more_lines:
                    line.other_value += balance_sheet_more_line.value

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

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

    @api.constrains("name")
    def _constrains_name(self):
        for line in self:
            if not line.name:
                raise ValidationError(
                    _("Name must be filled!")
                )

    _sql_constraint = [
        ("unique_name", "unique(name)", _("Name must be unique!"))
    ]
