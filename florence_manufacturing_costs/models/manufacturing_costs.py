from odoo import models, fields, api
from datetime import datetime
import calendar


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
        compute = "_compute_super_product",
        store = True
    )
    month = fields.Selection(
        [("1", "January"),
         ("2", "February"),
         ("3", "March"),
         ("4", "April"),
         ("5", "May"),
         ("6", "June"),
         ("7", "July"),
         ("8", "August"),
         ("9", "September"),
         ("10", "October"),
         ("11", "November"),
         ("12", "Dicember")],
        default = str(datetime.now().month),
        required = True,
        tracking = True
    )
    year = fields.Char(
        required = True,
        size = 4,
        tracking = True,
        default = str(datetime.now().year)
    )
    total_costs = fields.Float(
        compute = "_compute_total_costs",
        store = True,
        group_operator = "avg"
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
    last_bill_number = fields.Char(
        compute = "_compute_last_bill_number"
    )

    @api.depends("month", "year", "name")
    def _compute_last_bill_number(self):
        for line in self:
            line.last_bill_number = False

            if line.name:
                for bill in self.env["account.move"].search([("is_manufacturing_bill", "=", True)], order = "name desc"):
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id == line.name \
                                and str(line.month) == str(datetime.strptime(str(bill.invoice_date), "%Y-%m-%d").month) \
                                and str(line.year) == str(datetime.strptime(str(bill.invoice_date), "%Y-%m-%d").year):
                            line.last_bill_number = bill.name
                            break

                    if line.last_bill_number:
                        break

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

    @api.depends("name", "year", "month")
    def _compute_start_date(self):
        for line in self:
            line.start_date = False

            if line.name:
                for bill in self.env["account.move"].search([("is_manufacturing_bill", "=", True)], order = "name desc"):
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id == line.name \
                                and str(line.month) == str(datetime.strptime(str(bill.invoice_date), "%Y-%m-%d").month) \
                                and str(line.year) == str(datetime.strptime(str(bill.invoice_date), "%Y-%m-%d").year):
                            line.start_date = bill.invoice_date
                            break

                    if line.start_date:
                        break

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

    @api.depends("name")
    def _compute_is_bom_present(self):
        for line in self:
            line.is_bom_present = True if line.name.bom_count >= 1 else False

    @api.depends("name", "year", "month")
    def _compute_last_price_invoiced(self):
        for line in self:
            line.last_price_invoiced = 0

            if line.name:
                for bill in self.env["account.move"].search([("is_manufacturing_bill", "=", True)], order = "name desc"):
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id == line.name \
                                and str(line.month) == str(datetime.strptime(str(bill.invoice_date), "%Y-%m-%d").month) \
                                and str(line.year) == str(datetime.strptime(str(bill.invoice_date), "%Y-%m-%d").year):
                            line.last_price_invoiced = invoice_line.price_unit
                            break

                    if line.last_price_invoiced > 0:
                        break

    @api.depends("name", "month")
    def _compute_last_price_packaging(self):
        for line in self:
            line.last_price_packaging = 0

            for bom_id in line.name.bom_ids:
                for bom_line_id in bom_id.bom_line_ids:
                    for bill in self.env["account.move"].search([("is_manufacturing_bill", "=", True)], order = "name desc"):
                        for invoice_line in bill.invoice_line_ids:
                            if invoice_line.product_id == bom_line_id.product_id \
                                    and datetime.strptime(str(bill.invoice_date), "%Y-%m-%d").month <= int(line.month):
                                line.last_price_packaging = \
                                    invoice_line.price_unit \
                                    + ((invoice_line.price_total - invoice_line.price_subtotal) / invoice_line.quantity)
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

    @api.depends("name", "month", "year")
    def _compute_product_last_manufacturer(self):
        for line in self:
            line.product_last_manufacturer = ""

            if line.name:
                for bill in self.env["account.move"].search([("is_manufacturing_bill", "=", True)], order = "name desc"):
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id == line.name and \
                                str(line.month) == str(datetime.strptime(str(bill.invoice_date), "%Y-%m-%d").month) \
                                and str(line.year) == str(datetime.strptime(str(bill.invoice_date), "%Y-%m-%d").year):
                            line.product_last_manufacturer = bill.partner_id.name
                            break

                    if len(line.product_last_manufacturer) > 0:
                        break

    @api.depends("name", "month", "year")
    def _compute_product_updated_qty(self):
        for line in self:
            line.product_updated_qty = 0

            if line.name:
                for bill in self.env["account.move"].search([("is_manufacturing_bill", "=", True)], order = "name desc"):
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id == line.name \
                                and str(line.month) == str(datetime.strptime(str(bill.invoice_date), "%Y-%m-%d").month) \
                                and str(line.year) == str(datetime.strptime(str(bill.invoice_date), "%Y-%m-%d").year):
                            line.product_updated_qty = invoice_line.quantity
                            break

                    if line.product_updated_qty > 0:
                        break

    @api.depends("costs_line", "month", "year", "name",
                 "last_price_packaging", "price_total",
                 "price_public", "currency_id", "start_date",
                 "product_last_manufacturer",
                 "product_updated_qty", "last_price_invoiced")
    def update_values_action(self):
        for line in self:
            if len(line.costs_lines) == 0:
                for bill in self.env["account.move"].search([("is_manufacturing_bill", "=", True)],
                                                            order = "name asc"):
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id == line.name \
                                and str(line.month) == str(datetime.strptime(str(bill.invoice_date), "%Y-%m-%d").month) \
                                and str(line.year) == str(datetime.strptime(str(bill.invoice_date), "%Y-%m-%d").year):
                            self.write({
                                'costs_lines': [
                                    (0, 0, {
                                        'manufacturing_costs_line_id': line.id,
                                        'product': line.name.id,
                                        'bill': bill.name,
                                        'date': bill.invoice_date,
                                        'manufacturer': bill.partner_id.name,
                                        'pcs_invoiced': invoice_line.quantity,
                                        'price_invoiced': invoice_line.price_unit,
                                        'price_packaging': line.last_price_packaging,
                                        'price_total': line.last_price_total,
                                        'price_public': line.last_price_public,
                                        'other_costs': 0,
                                        'currency_id': line.currency_id
                                    })
                                ]})
                            break
            else:
                dates = []
                bills = []

                for costs_line in line.costs_lines:
                    if str(line.month) == str(datetime.strptime(str(line.start_date), "%Y-%m-%d").month) \
                            and str(line.year) == str(datetime.strptime(str(line.start_date), "%Y-%m-%d").year):
                        dates.append(costs_line.date)
                        bills.append(costs_line.bill)

                if len(dates) > 0:
                    if line.start_date != dates[-1] \
                            or (line.start_date == dates[-1] and line.last_bill_number != bills[-1]):
                        self.write({
                            'costs_lines': [
                                (0, 0, {
                                    'manufacturing_costs_line_id': line.id,
                                    'product': line.name.id,
                                    'bill': line.last_bill_number,
                                    'date': line.start_date,
                                    'manufacturer': line.product_last_manufacturer,
                                    'pcs_invoiced': line.product_updated_qty,
                                    'price_invoiced': line.last_price_invoiced,
                                    'price_packaging': line.last_price_packaging,
                                    'price_total': line.last_price_total,
                                    'price_public': line.last_price_public,
                                    'other_costs': 0,
                                    'currency_id': line.currency_id
                                })
                            ]})

    def graph_view_action(self):
        return {
            'name': 'Costs Line Analysis',
            'view_type': 'graph',
            'view_mode': 'graph',
            'res_model': 'manufacturing.costs.line',
            'type': 'ir.actions.act_window',
            'domain': ['&','&','&',
               ('manufacturer', 'ilike', self.product_last_manufacturer),
               ('product', 'ilike', self.name.name),
               ('date','>=',self.year + "-" + self.month + "-1"),
               ('date','<=',self.year + "-" + str(self.month) + "-" + str(calendar.monthrange(int(self.year), int(self.month))[1]))
            ],
            'context': {
                'graph_measure': 'price_total',
                'graph_mode': 'line',
                'graph_groupbys': ['date:day', 'product']
            }
        }
