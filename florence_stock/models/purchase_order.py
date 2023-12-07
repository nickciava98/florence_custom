from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    stock_picking_ids = fields.Many2many(
        "stock.picking",
        "purchase_order_stock_picking_rel",
        compute="_compute_stock_picking_ids",
        string="Deliveries"
    )

    def _compute_stock_picking_ids(self):
        for order in self:
            order.stock_picking_ids = self.env["stock.picking"].search(
                [("purchase_order_ids", "in", order.id)]
            )
