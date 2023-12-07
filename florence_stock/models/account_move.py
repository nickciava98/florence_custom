from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    stock_picking_ids = fields.Many2many(
        "stock.picking",
        "account_move_stock_picking_rel",
        compute="_compute_stock_picking_ids",
        string="Deliveries"
    )

    def _compute_stock_picking_ids(self):
        for move in self:
            move.stock_picking_ids = self.env["stock.picking"].search(
                [("bill_ids", "in", move.id)]
            )
