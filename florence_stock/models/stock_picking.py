from odoo import models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    bill_ids = fields.Many2many(
        "account.move",
        "stock_picking_account_move_rel",
        domain="[('move_type', 'in', ('in_invoice', 'in_refund', 'in_receipt'))]",
        string="Bills"
    )
    purchase_order_ids = fields.Many2many(
        "purchase.order",
        "stock_picking_purchase_order_rel",
        string="Purchases"
    )


from odoo.addons.sale_stock.models.stock import StockPicking
from odoo.addons.stock.models.stock_picking import Picking

def _action_done(self):
    res = Picking._action_done(self)
    sale_order_lines_vals = []

    for move in self.move_lines:
        sale_order = move.picking_id.sale_id

        if not sale_order or move.location_dest_id.usage != "customer" or move.sale_line_id or not move.quantity_done:
            continue

        product = move.product_id
        so_line_vals = {
            "move_ids": [(4, move.id, 0)],
            "name": product.display_name,
            "order_id": sale_order.id,
            "product_id": product.id,
            "product_uom_qty": .0,
            "qty_delivered": move.quantity_done,
            "product_uom": move.product_uom.id,
        }

        if product.invoice_policy == "delivery":
            so_line = sale_order.order_line.filtered(lambda sol: sol.product_id == product)

            if so_line:
                so_line_vals["price_unit"] = so_line[0].price_unit

        elif product.invoice_policy == "order":
            so_line_vals["price_unit"] = .0

        sale_order_lines_vals.append(so_line_vals)

    if sale_order_lines_vals:
        self.env["sale.order.line"].with_context(force_create=True).create(sale_order_lines_vals)

    return res

StockPicking._action_done = _action_done
