from odoo import models, fields


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
