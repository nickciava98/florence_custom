from odoo import models, fields, api


class FlorenceBalanceSheetInventory(models.Model):
    _name = "florence.balance.sheet.inventory"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Balance Sheet Inventory"

    name = fields.Many2one(
        "florence.balance.sheet"
    )
    product_id = fields.Many2one(
        "product.product"
    )
    location_id = fields.Many2one(
        "stock.location"
    )
    lot_id = fields.Many2one(
        "stock.production.lot"
    )
    available_quantity = fields.Float()
    value = fields.Float()
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )
    sale_ok = fields.Boolean(
        string = "Can Be Sold"
    )
    can_be_used = fields.Boolean()

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

    @api.onchange("available_quantity")
    def _onchange_available_quantity(self):
        for line in self:
            if line.product_id:
                cost = .0
                bills = self.env["account.move"].search([("move_type", "=", "in_invoice")], order = "name desc")

                for bill in bills:
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id == line.product_id:
                            cost = invoice_line.price_unit
                            break
                    if cost > 0:
                        break
                if cost > 0:
                    line.value = cost * line.available_quantity


class FlorenceBalanceSheetInventoryMore(models.Model):
    _name = "florence.balance.sheet.inventory.more"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Balance Sheet Inventory More"

    name = fields.Many2one(
        "florence.balance.sheet"
    )
    product_id = fields.Many2one(
        "product.product"
    )
    location = fields.Char()
    lot = fields.Char()
    available_quantity = fields.Float()
    value = fields.Float()
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )
    sale_ok = fields.Boolean(
        string = "Can Be Sold"
    )
    can_be_used = fields.Boolean()

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

    @api.onchange("available_quantity")
    def _onchange_available_quantity(self):
        for line in self:
            if line.product_id:
                cost = .0
                bills = self.env["account.move"].search([("move_type", "=", "in_invoice")], order = "name desc")

                for bill in bills:
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id == line.product_id:
                            cost = invoice_line.price_unit
                            break
                    if cost > 0:
                        break
                if cost > 0:
                    line.value = cost * line.available_quantity
