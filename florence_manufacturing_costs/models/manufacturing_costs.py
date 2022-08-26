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
    super_product = fields.Many2one(
        "product.template",
        tracking = True,
        compute = "_compute_super_product"
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
    last_price_invoiced = fields.Float(
        compute = "_compute_last_price_invoiced"
    )
    last_price_packaging = fields.Float(
        compute = "_compute_last_price_packaging"
    )
    last_price_total = fields.Float(
        compute = "_compute_last_price_total"
    )
    last_price_public = fields.Float(
        compute = "_compute_last_price_public"
    )
    product_last_manufacturer = fields.Char(
        compute = "_compute_product_last_manufacturer"
    )
    product_updated_qty = fields.Float(
        compute = "_compute_product_updated_qty"
    )

    @api.depends("name")
    def _compute_super_product(self):
        for line in self:
            line.super_product = self.env["product.product"].search([("id", "=", line.name.id)]).product_tmpl_id

    @api.depends("costs_lines")
    def _compute_total_costs(self):
        for line in self:
            line.total_costs = 0

            for costs_line in line.costs_lines:
                if costs_line.price_total:
                    line.total_costs += costs_line.price_total + costs_line.other_costs

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
    def _compute_last_price_invoiced(self):
        for line in self:
            line.last_price_invoiced = 0

            for bill in self.env["account.move"].search([("is_manufacturing_bill", "=", True)]):
                for invoice_line in bill.invoice_line_ids:
                    if invoice_line.product_id == line.name:
                        line.last_price_invoiced = invoice_line.price_unit
                        break

                if line.last_price_invoiced > 0:
                    break

    @api.depends("name")
    def _compute_last_price_packaging(self):
        for line in self:
            line.last_price_packaging = 0

            for bom_id in line.name.bom_ids:
                for bom_line_id in bom_id.bom_line_ids:
                    for bill in self.env["account.move"].search([("is_manufacturing_bill", "=", True)]):
                        for invoice_line in bill.invoice_line_ids:
                            if invoice_line.product_id == bom_line_id.product_id:
                                line.last_price_packaging = invoice_line.price_unit
                                break

                        if line.last_price_packaging > 0:
                            break

    @api.depends("last_price_invoiced", "last_price_packaging")
    def _compute_last_price_total(self):
        for line in self:
            line.last_price_total = line.last_price_invoiced + line.last_price_packaging

    @api.depends("name")
    def _compute_last_price_public(self):
        for line in self:
            if line.name.lst_price:
                line.last_price_public = line.name.lst_price
            else:
                line.last_price_public = line.name.list_price

    @api.depends("name")
    def _compute_product_last_manufacturer(self):
        for line in self:
            line.product_last_manufacturer = ""

            for bill in self.env["account.move"].search([("is_manufacturing_bill", "=", True)]):
                for invoice_line in bill.invoice_line_ids:
                    if invoice_line.product_id == line.name:
                        line.product_last_manufacturer = invoice_line.partner_id.name
                        break

                if len(line.product_last_manufacturer) > 0:
                    break

    @api.depends("name")
    def _compute_product_updated_qty(self):
        for line in self:
            line.product_updated_qty = 0

            for bill in self.env["account.move"].search([("is_manufacturing_bill", "=", True)]):
                for invoice_line in bill.invoice_line_ids:
                    if invoice_line.product_id == line.name:
                        line.product_updated_qty = invoice_line.quantity
                        break

                if line.product_updated_qty > 0:
                    break
