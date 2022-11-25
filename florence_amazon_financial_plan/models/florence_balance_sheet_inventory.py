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
        related = "product_id.sale_ok"
    )
    can_be_used = fields.Boolean(
        related = "product_id.can_be_used"
    )

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id
