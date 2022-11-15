from odoo import models, fields, api


class StockQuant(models.Model):
    _inherit = "stock.quant"

    value = fields.Monetary(
        string = "Value",
        compute = "_compute_value",
        groups = "stock.group_stock_manager"
    )

    @api.depends("product_id", "available_quantity")
    def _compute_value(self):
        for line in self:
            line.value = 0

            if line.product_id:
                cost = 0

                for fp in self.env["florence.fp.costs"].search([]):
                    for fp_line in fp.fp_costs_lines:
                        if fp_line.component == line.product_id:
                            cost = fp_line.cost
                            break
                    if cost != 0:
                        break
                if cost != 0:
                    line.value = cost * line.available_quantity
