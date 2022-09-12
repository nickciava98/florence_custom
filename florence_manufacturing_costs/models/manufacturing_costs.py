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
         ("12", "December")],
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
    last_price_invoiced = fields.Float(
        compute = "_compute_last_price_invoiced"
    )
    last_price_packaging = fields.Float(
        compute = "_compute_last_price_packaging"
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
    last_bill_number = fields.Many2one(
        "account.move",
        compute = "_compute_last_bill_number"
    )
    price_invoiced_avg = fields.Float(
        compute = "_compute_price_invoiced_avg",
        group_operator = "avg",
        store = True
    )
    price_packaging_avg = fields.Float(
        compute = "_compute_price_packaging_avg",
        group_operator = "avg",
        store = True
    )
    price_total_avg = fields.Float(
        compute = "_compute_price_total_avg",
        group_operator = "avg",
        store = True
    )
    other_costs_avg = fields.Float(
        compute = "_compute_other_costs_avg",
        group_operator = "avg",
        store = True
    )

    @api.depends("costs_lines")
    def _compute_price_invoiced_avg(self):
        for line in self:
            line.price_invoiced_avg = 0

            if len(line.costs_lines) > 0:
                price_invoiced_times_pcs_invoiced = 0
                total_pcs_invoiced = 0

                for costs_line in line.costs_lines:
                    price_invoiced_times_pcs_invoiced += costs_line.price_invoiced * costs_line.pcs_invoiced
                    total_pcs_invoiced += costs_line.pcs_invoiced

                if total_pcs_invoiced > 0:
                    line.price_invoiced_avg = price_invoiced_times_pcs_invoiced / total_pcs_invoiced

    @api.depends("costs_lines")
    def _compute_price_packaging_avg(self):
        for line in self:
            line.price_packaging_avg = 0

            if len(line.costs_lines) > 0:
                price_packaging_times_pcs_invoiced = 0
                total_pcs_invoiced = 0

                for costs_line in line.costs_lines:
                    price_packaging_times_pcs_invoiced += costs_line.price_packaging * costs_line.pcs_invoiced
                    total_pcs_invoiced += costs_line.pcs_invoiced

                if total_pcs_invoiced > 0:
                    line.price_packaging_avg = price_packaging_times_pcs_invoiced / total_pcs_invoiced

    @api.depends("costs_lines")
    def _compute_price_total_avg(self):
        for line in self:
            line.price_total_avg = 0

            if len(line.costs_lines) > 0:
                price_total_times_pcs_invoiced = 0
                total_pcs_invoiced = 0

                for costs_line in line.costs_lines:
                    price_total_times_pcs_invoiced += costs_line.price_total * costs_line.pcs_invoiced
                    total_pcs_invoiced += costs_line.pcs_invoiced

                if total_pcs_invoiced > 0:
                    line.price_total_avg = price_total_times_pcs_invoiced / total_pcs_invoiced

    @api.depends("costs_lines")
    def _compute_other_costs_avg(self):
        for line in self:
            line.other_costs_avg = 0

            if len(line.costs_lines) > 0:
                other_costs_times_pcs_invoiced = 0
                total_pcs_invoiced = 0

                for costs_line in line.costs_lines:
                    other_costs_times_pcs_invoiced += costs_line.other_costs * costs_line.pcs_invoiced
                    total_pcs_invoiced += costs_line.pcs_invoiced

                if total_pcs_invoiced > 0:
                    line.other_costs_avg = other_costs_times_pcs_invoiced / total_pcs_invoiced

    def model_search(self, model, domain, order):
        if len(order) > 0:
            return self.env[model].search(
                domain,
                order = order
            )

        return self.env[model].search(
            domain
        )

    @api.depends("month", "year", "name")
    def _compute_last_bill_number(self):
        for line in self:
            line.last_bill_number = False

            if line.name:
                for bill in line.model_search(
                        "account.move",
                        ["&", "&",
                         ("move_type", "=", "in_invoice"),
                         ("invoice_date", ">=", line.year + "-" + str(line.month) + "-1"),
                         ("invoice_date", "<=",
                            line.year + "-"
                            + str(line.month) + "-"
                            + str(calendar.monthrange(int(line.year), int(line.month))[1])
                         ),
                        ],
                        "name desc"
                ):
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id == line.name:
                            line.last_bill_number = bill
                            break

                    if line.last_bill_number:
                        break

    @api.depends("name")
    def _compute_super_product(self):
        for line in self:
            line.super_product = line.model_search(
                "product.product",
                [("id", "=", line.name.id)],
                ""
            ).product_tmpl_id

    @api.depends("name", "year", "month")
    def _compute_start_date(self):
        for line in self:
            line.start_date = False

            if line.name:
                for bill in line.model_search(
                        "account.move",
                        ["&", "&",
                         ("move_type", "=", "in_invoice"),
                         ("invoice_date", ">=", line.year + "-" + str(line.month) + "-1"),
                         ("invoice_date", "<=",
                          line.year + "-"
                          + str(line.month) + "-"
                          + str(calendar.monthrange(int(line.year), int(line.month))[1])
                          ),
                         ],
                        "name desc"
                ):
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id == line.name:
                            line.start_date = bill.invoice_date
                            break

                    if line.start_date:
                        break

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

    @api.depends("name", "year", "month")
    def _compute_last_price_invoiced(self):
        for line in self:
            line.last_price_invoiced = 0

            if line.name:
                for bill in line.model_search(
                        "account.move",
                        ["&", "&",
                         ("move_type", "=", "in_invoice"),
                         ("invoice_date", ">=", line.year + "-" + str(line.month) + "-1"),
                         ("invoice_date", "<=",
                          line.year + "-"
                          + str(line.month) + "-"
                          + str(calendar.monthrange(int(line.year), int(line.month))[1])
                          ),
                         ],
                        "name desc"
                ):
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id == line.name:
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
                    previous_price_packaging = line.last_price_packaging
                    for bill in line.model_search("account.move",
                            ["&",
                             ("move_type", "=", "in_invoice"),
                             ("invoice_date", "<=",
                                 line.year + "-"
                                    + str(line.month) + "-"
                                    + str(calendar.monthrange(int(line.year), int(line.month))[1]))
                            ], "name desc"):
                        for invoice_line in bill.invoice_line_ids:
                            if invoice_line.product_id == bom_line_id.product_id:
                                line.last_price_packaging += \
                                    invoice_line.price_unit \
                                    + ((invoice_line.price_total - invoice_line.price_subtotal) / invoice_line.quantity)
                                break

                        if line.last_price_packaging > previous_price_packaging:
                            break
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
                for bill in line.model_search(
                        "account.move",
                        ["&", "&",
                         ("move_type", "=", "in_invoice"),
                         ("invoice_date", ">=", line.year + "-" + str(line.month) + "-1"),
                         ("invoice_date", "<=",
                          line.year + "-"
                          + str(line.month) + "-"
                          + str(calendar.monthrange(int(line.year), int(line.month))[1])
                          ),
                         ],
                        "name desc"
                ):
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id == line.name:
                            line.product_last_manufacturer = bill.partner_id.name
                            break

                    if len(line.product_last_manufacturer) > 0:
                        break

    @api.depends("name", "month", "year")
    def _compute_product_updated_qty(self):
        for line in self:
            line.product_updated_qty = 0

            if line.name:
                for bill in line.model_search(
                        "account.move",
                        ["&", "&",
                         ("move_type", "=", "in_invoice"),
                         ("invoice_date", ">=", line.year + "-" + str(line.month) + "-1"),
                         ("invoice_date", "<=",
                          line.year + "-"
                          + str(line.month) + "-"
                          + str(calendar.monthrange(int(line.year), int(line.month))[1])
                          ),
                         ],
                        "name desc"
                ):
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id == line.name:
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
                for bill in line.model_search(
                        "account.move",
                        ["&", "&",
                         ("move_type", "=", "in_invoice"),
                         ("invoice_date", ">=", line.year + "-" + str(line.month) + "-1"),
                         ("invoice_date", "<=",
                          line.year + "-"
                          + str(line.month) + "-"
                          + str(calendar.monthrange(int(line.year), int(line.month))[1])
                          ),
                         ],
                        "name asc"
                ):
                    for invoice_line in bill.invoice_line_ids:
                        if invoice_line.product_id == line.name:
                            self.write({
                                'costs_lines': [
                                    (0, 0, {
                                        'product': line.name.id,
                                        'bill': bill.id,
                                        'date': bill.invoice_date,
                                        'manufacturer': bill.partner_id.name,
                                        'pcs_invoiced': invoice_line.quantity,
                                        'price_invoiced': invoice_line.price_unit,
                                        'price_packaging': line.last_price_packaging,
                                        'price_public': line.last_price_public,
                                        'other_costs': 0,
                                        'currency_id': line.currency_id,
                                    })
                                ]})
                            break
            else:
                dates = []
                bills = []

                for costs_line in line.costs_lines:
                    if str(line.month) == str(datetime.strptime(str(costs_line.date), "%Y-%m-%d").month) \
                            and str(line.year) == str(datetime.strptime(str(costs_line.date), "%Y-%m-%d").year):
                        dates.append(costs_line.date)
                        bills.append(costs_line.bill)

                if len(bills) > 0:
                    if line.last_bill_number != bills[-1]:
                        self.write({
                            'costs_lines': [
                                (0, 0, {
                                    'product': line.name.id,
                                    'bill': line.last_bill_number.id,
                                    'date': line.start_date,
                                    'manufacturer': line.product_last_manufacturer,
                                    'pcs_invoiced': line.product_updated_qty,
                                    'price_invoiced': line.last_price_invoiced,
                                    'price_packaging': line.last_price_packaging,
                                    'price_public': line.last_price_public,
                                    'other_costs': 0,
                                    'currency_id': line.currency_id
                                })
                            ]})

    def graph_view_action(self):
        return {
            'name': 'Costs Analysis',
            'view_type': 'graph',
            'view_mode': 'graph',
            'res_model': 'manufacturing.costs.line',
            'type': 'ir.actions.act_window',
            'domain': [
                '&', '&',
                ('date', '>=', self.year + "-" + self.month + "-1"),
                ('date', '<=', self.year + "-" + str(self.month)
                 + "-" + str(calendar.monthrange(int(self.year), int(self.month))[1])),
                ('product', '=', self.name.id)
            ],
            'context': {
                'graph_measure': 'price_total',
                'graph_mode': 'line',
            }
        }
