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
        compute = "_compute_start_date",
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
    is_bom_present = fields.Boolean(
        compute = "_compute_is_bom_present"
    )
    product_updated_cost = fields.Float(
        compute = "_compute_product_updated_cost"
    )
    product_last_manufacturer = fields.Char(
        compute = "_compute_product_last_manufacturer"
    )
    product_updated_qty = fields.Float(
        compute = "_compute_product_updated_qty"
    )

    @api.depends("costs_lines")
    def _compute_total_costs(self):
        for line in self:
            line.total_costs = 0

            for costs_line in line.costs_lines:
                if costs_line.price_finished:
                    line.total_costs += costs_line.price_finished

    def _compute_start_date(self):
        for line in self:
            line.start_date = datetime.now()

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

    @api.depends("name")
    def _compute_is_bom_present(self):
        for line in self:
            line.is_bom_present = True if line.name.bom_count >= 1 else False

    @api.depends("name")
    def _compute_product_updated_cost(self):
        for line in self:
            line.product_updated_cost = 0

            for bom_id in line.name.bom_ids:
                for bom_line_id in bom_id.bom_line_ids:
                    for seller_id in bom_line_id.product_id.seller_ids:
                        line.product_updated_cost += seller_id.price
                        break

    @api.depends("name")
    def _compute_product_last_manufacturer(self):
        for line in self:
            line.product_last_manufacturer = False

            for bom_id in line.name.bom_ids:
                for bom_line_id in bom_id.bom_line_ids:
                    for seller_id in bom_line_id.product_id.seller_ids:
                        line.product_last_manufacturer = seller_id.name.name
                        break

    @api.depends("name")
    def _compute_product_updated_qty(self):
        for line in self:
            line.product_updated_qty = 0

            for bom_id in line.name.bom_ids:
                for bom_line_id in bom_id.bom_line_ids:
                    for seller_id in bom_line_id.product_id.seller_ids:
                        line.product_updated_qty = seller_id.min_qty
                        break
