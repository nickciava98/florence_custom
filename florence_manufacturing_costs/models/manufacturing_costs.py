from odoo import models, fields, api
from datetime import datetime

class ManufacturingCosts(models.Model):
    _name = "manufacturing.costs"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Manufacturing Costs Model"

    name = fields.Many2one(
        "product.product",
        required = True,
        tracking = True
    )
    total_costs = fields.Float(
        compute = "_compute_total_costs"
    )
    start_date = fields.Date(
        default = datetime.today(),
        required = True
    )
    costs_lines = fields.One2many(
        "manufacturing.costs.line",
        "manufacturing_costs_line_id"
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )

    @api.depends("costs_lines")
    def _compute_total_costs(self):
        for line in self:
            line.total_costs = 0

            for costs_line in line.costs_lines:
                if costs_line.price_finished:
                    line.total_costs += costs_line.price_finished

    @api.onchange("name")
    def _onchange_product(self):
        self.costs_lines = False

        for line in self:
            for seller in line.name.seller_ids:
                self.write(
                    {'costs_lines':
                         [(0, 0,
                           {'date': line.start_date,
                            'manufacturer': seller.name.name,
                            'pcs': seller.min_qty,
                            'currency_id': line.name.currency_id.id,
                            'price_agreed': seller.price,
                            'price_unit': seller.price,
                            'price_finished': seller.price * 1.22}
                           )]
                     })

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

    def write(self, vals):
        return super(ManufacturingCosts, self).write(vals)

    def update_values_action(self):
        costs_lines_dates = []

        for line in self:
            for costs_line in line.costs_lines:
                costs_lines_dates.append(costs_line.date)

        self.costs_lines = False
        costs_lines_updated = []

        costs_lines_dates.append(self.start_date)

        for line in self:
            for seller in line.name.seller_ids:
                costs_lines_updated.append(
                    (0, 0,
                     {'date': line.start_date,
                      'manufacturer': seller.name.name,
                      'pcs': seller.min_qty,
                      'currency_id': line.name.currency_id.id,
                      'price_agreed': seller.price,
                      'price_unit': seller.price,
                      'price_finished': seller.price * 1.22}
                     ))

        self.write({
            "costs_lines": costs_lines_updated
        })
