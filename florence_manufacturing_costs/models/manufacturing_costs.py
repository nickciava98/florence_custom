from odoo import models, fields, api
from datetime import datetime
import base64

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
    last_price_agreed = fields.Float(
        compute = "_compute_last_price_agreed"
    )
    last_price_unit = fields.Float(
        compute = "_compute_last_price_unit"
    )
    last_price_finished = fields.Float(
        compute = "_compute_last_price_finished"
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
    def _compute_last_price_agreed(self):
        for line in self:
            line.last_price_agreed = 0

            for seller_id in line.name.seller_ids:
                line.last_price_agreed = seller_id.price
                break

    @api.depends("name")
    def _compute_last_price_unit(self):
        for line in self:
            line.last_price_unit = 0

            for bom_id in line.name.bom_ids:
                for bom_line_id in bom_id.bom_line_ids:
                    for seller_id in bom_line_id.product_id.seller_ids:
                        line.last_price_unit += seller_id.price
                        break

            for bill in self.env["account.move"].search([("is_manufacturing_bill", "=", True)]):
                for invoice_line in bill.invoice_line_ids:
                    if invoice_line.product_id == line.name:
                        line.last_price_unit += invoice_line.price_unit

    @api.depends("name")
    def _compute_last_price_finished(self):
        for line in self:
            line.last_price_finished = 0

            if line.name.lst_price:
                line.last_price_finished = line.name.lst_price
            else:
                line.last_price_finished = line.name.list_price

    @api.depends("name")
    def _compute_product_last_manufacturer(self):
        for line in self:
            line.product_last_manufacturer = False

            for seller_id in line.name.seller_ids:
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
