import datetime

from odoo import models, fields, api


class FlorenceBalanceSheet(models.Model):
    _name = "florence.balance.sheet"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Balance Sheet"

    def _default_products_cash(self):
        products_cash = .0

        for fp in self.env["amazon.financial.plan"].search([]):
            products_cash += fp.total_to_use

        return products_cash

    def _default_balance_sheet_inventory_lines(self):
        balance_sheet_inventory_lines = [(5, 0, 0)]

        for item in self.env["stock.quant"].search([("location_id.is_valuable_stock", "=", True)]):
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

    name = fields.Char(
        copy=False
    )
    date = fields.Date(
        default=datetime.datetime.now()
    )
    products_cash = fields.Float(
        default=_default_products_cash,
        readonly=True,
        copy=False,
        string="Products Cash (i)"
    )
    inventory_value = fields.Float(
        compute="_compute_inventory_value",
        store=True,
        string="Inventory Value (ii)"
    )
    amazon_products_cash = fields.Float(
        compute="_compute_amazon_products_cash",
        string="Amazon Products Cash (iii)"
    )
    other_value = fields.Float(
        compute="_compute_other_value",
        string="Other Values (iv)"
    )
    balance_sheet_lines = fields.One2many(
        "florence.balance.sheet.line",
        "name",
        copy=True
    )
    notebook_invisible = fields.Boolean(
        default=False
    )
    balance_sheet_more_lines = fields.One2many(
        "florence.balance.sheet.more",
        "name",
        copy=True
    )
    balance_sheet_inventory_lines = fields.One2many(
        "florence.balance.sheet.inventory",
        "name",
        default=_default_balance_sheet_inventory_lines
    )
    balance_sheet_inventory_more_lines = fields.One2many(
        "florence.balance.sheet.inventory.more",
        "name",
        copy=True
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.ref("base.main_company").currency_id
    )
    total = fields.Float(
        compute="_compute_total"
    )

    @api.depends("balance_sheet_inventory_lines", "balance_sheet_inventory_more_lines")
    def _compute_inventory_value(self):
        for line in self:
            line.inventory_value = .0

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
            line.total = sum([line.products_cash, line.inventory_value, line.amazon_products_cash, line.other_value])

    @api.depends("balance_sheet_more_lines")
    def _compute_other_value(self):
        for line in self:
            line.other_value = .0

            if len(line.balance_sheet_more_lines) > 0:
                for balance_sheet_more_line in line.balance_sheet_more_lines:
                    line.other_value += balance_sheet_more_line.value

    @api.depends("balance_sheet_lines")
    def _compute_amazon_products_cash(self):
        for line in self:
            line.amazon_products_cash = .0

            if len(line.balance_sheet_lines) > 0:
                for balance_sheet_line in line.balance_sheet_lines:
                    line.amazon_products_cash += balance_sheet_line.price_unit * balance_sheet_line.quantity

    def show_hide_notebook_action(self):
        self.notebook_invisible = not self.notebook_invisible

    def export_xlsx_action(self):
        init_form_id = self.env.ref("florence_amazon_financial_plan.export_xlsx_balance_sheet_init_view_form")

        return {
            "name": "Export XLSX Balance Sheet",
            "type": "ir.actions.act_window",
            "res_model": "export.xlsx.balance.sheet",
            "view_mode": "form",
            "view_type": "tree,form",
            "views": [(init_form_id.id, "form")],
            "context": {
                "default_balance_sheet_id": self.id
            },
            "target": "new"
        }

    _sql_constraint = [
        ("unique_name", "unique(name)", "Name must be unique!")
    ]
