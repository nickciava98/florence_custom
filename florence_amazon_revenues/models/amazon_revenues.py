from odoo import models, fields, api
from datetime import datetime

class AmazonRevenues(models.Model):
    _name = "amazon.revenues"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Amazon Revenues Model"

    name = fields.Selection(
        [("IT", "Amazon IT"),
         ("FR", "Amazon FR"),
         ("DE", "Amazon DE"),
         ("ES", "Amazon ES"),
         ("UK", "Amazon UK")],
        required = True,
        string = "Marketplace",
        tracking = True
    )
    product = fields.Many2one(
        "product.template",
        required = True,
        tracking = True
    )
    product_updated_price = fields.Float(
        compute = "_compute_product_updated_price",
        digits = (12, 4)
    )
    start_date = fields.Date(
        compute = "_compute_start_date"
    )
    total_probable_income = fields.Float(
        compute = "_compute_total_probable_income",
        store = True,
        string = "Total Probable Income (Odoo)",
        digits = (12, 4)
    )
    total_probable_income_amz = fields.Float(
        compute = "_compute_total_probable_income_amz",
        store = True,
        string = "Total Probable Income (Amazon)",
        digits = (12, 4)
    )
    revenues_line = fields.One2many(
        "amazon.revenues.line",
        "amazon_revenues_line_id"
    )
    revenues_line_test = fields.One2many(
        "amazon.revenues.line",
        "amazon_revenues_line_id_test"
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )
    product_updated_sku_cost = fields.Float(
        compute = "_compute_product_updated_sku_cost",
        digits = (12, 4)
    )
    chart_start = fields.Date()
    chart_end = fields.Date()
    chart_start_test = fields.Date()
    chart_end_test = fields.Date()
    group_by = fields.Selection(
        [("day", "Daily Revenues"),
         ("week", "Weekly Revenues"),
         ("month", "Monthly Revenues")]
    )
    group_by_test = fields.Selection(
        [("day", "Daily Revenues"),
         ("week", "Weekly Revenues"),
         ("month", "Monthly Revenues")]
    )

    @api.onchange("name")
    def _onchange_name(self):
        for line in self:
            if len(line.revenues_line) > 0:
                for revenues_line in line.revenues_line:
                    revenues_line.parent = line.name
            if len(line.revenues_line_test) > 0:
                for revenues_line_test in line.revenues_line_test:
                    revenues_line_test.parent = line.name

    @api.onchange("product")
    def _onchange_product(self):
        for line in self:
            if len(line.revenues_line) > 0:
                for revenues_line in line.revenues_line:
                    revenues_line.product = line.product
            if len(line.revenues_line_test) > 0:
                for revenues_line_test in line.revenues_line_test:
                    revenues_line_test.product = line.product

    @api.depends("product")
    def _compute_product_updated_sku_cost(self):
        for line in self:
            line.product_updated_sku_cost = 0

            if "manufacturing.costs" in self.env:
                for product in self.env["manufacturing.costs"].search(
                        [("super_product", "=", line.product.id)]):
                    line.product_updated_sku_cost = product.price_total_avg

                    if line.product_updated_sku_cost != 0:
                        break

    def _compute_start_date(self):
        for line in self:
            line.start_date = datetime.now()

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

    @api.depends("product")
    def _compute_product_updated_price(self):
        for line in self:
            line.product_updated_price = 0

            if line.product.list_price:
                line.product_updated_price = line.product.list_price
            else:
                line.product_updated_price = line.product.lst_price

    @api.depends("revenues_line")
    def _compute_total_probable_income(self):
        for line in self:
            line.total_probable_income = 0

            for revenues_line in line.revenues_line:
                if revenues_line.probable_income:
                    line.total_probable_income += revenues_line.probable_income

    @api.depends("revenues_line")
    def _compute_total_probable_income_amz(self):
        for line in self:
            line.total_probable_income_amz = 0

            for revenues_line in line.revenues_line:
                if revenues_line.probable_income_amz:
                    line.total_probable_income_amz += revenues_line.probable_income_amz

    def dashboard_view_action(self):
        if self.group_by == "day":
            if self.chart_start or self.chart_end:
                return {
                    'name': 'Revenues Dashboard',
                    'view_type': 'dashboard',
                    'view_mode': 'dashboard',
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'domain': [
                        '&', '&', '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id_test', '=', False),
                        ('parent', '=', self.name),
                        ('date', '>=', self.chart_start),
                        ('date', '<=', self.chart_end)
                    ],
                    'context': {
                        'graph_measure': 'probable_income',
                        'graph_mode': 'line'
                    }
                }
            else:
                return {
                    'name': 'Revenues Dashboard',
                    'view_type': 'dashboard',
                    'view_mode': 'dashboard',
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'domain': [
                        '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id_test', '=', False),
                        ('parent', '=', self.name)
                    ],
                    'context': {
                        'graph_measure': 'probable_income',
                        'graph_mode': 'line'
                    }
                }
        else:
            if self.chart_start or self.chart_end:
                return {
                    'name': 'Revenues Dashboard',
                    'view_type': 'dashboard',
                    'view_mode': 'dashboard',
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'domain': [
                        '&', '&', '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id_test', '=', False),
                        ('parent', '=', self.name),
                        ('date', '>=', self.chart_start),
                        ('date', '<=', self.chart_end)
                    ],
                    'context': {
                        'graph_measure': 'probable_income',
                        'graph_mode': 'line',
                        'graph_groupbys': ['date:' + self.group_by]
                    }
                }
            else:
                return {
                    'name': 'Revenues Dashboard',
                    'view_type': 'dashboard',
                    'view_mode': 'dashboard',
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'domain': [
                        '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id_test', '=', False),
                        ('parent', '=', self.name)
                    ],
                    'context': {
                        'graph_measure': 'probable_income',
                        'graph_mode': 'line',
                        'graph_groupbys': ['date:' + self.group_by]
                    }
                }

    def graph_view_action(self):
        if self.group_by == "day":
            if self.chart_start or self.chart_end:
                return {
                    'name': 'Revenues Analysis',
                    'view_type': 'graph',
                    'view_mode': 'graph',
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'domain': [
                        '&', '&', '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id_test', '=', False),
                        ('parent', '=', self.name),
                        ('date', '>=', self.chart_start),
                        ('date', '<=', self.chart_end)
                    ],
                    'context': {
                        'graph_measure': 'probable_income',
                        'graph_mode': 'line'
                    }
                }
            else:
                return {
                    'name': 'Revenues Analysis',
                    'view_type': 'graph',
                    'view_mode': 'graph',
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'domain': [
                        '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id_test', '=', False),
                        ('parent', '=', self.name)
                    ],
                    'context': {
                        'graph_measure': 'probable_income',
                        'graph_mode': 'line'
                    }
                }
        else:
            if self.chart_start or self.chart_end:
                return {
                    'name': 'Revenues Analysis',
                    'view_type': 'graph',
                    'view_mode': 'graph',
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'domain': [
                        '&', '&', '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id_test', '=', False),
                        ('parent', '=', self.name),
                        ('date', '>=', self.chart_start),
                        ('date', '<=', self.chart_end)
                    ],
                    'context': {
                        'graph_measure': 'probable_income',
                        'graph_mode': 'line',
                        'graph_groupbys': ['date:' + self.group_by]
                    }
                }
            else:
                return {
                    'name': 'Revenues Analysis',
                    'view_type': 'graph',
                    'view_mode': 'graph',
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'domain': [
                        '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id_test', '=', False),
                        ('parent', '=', self.name)
                    ],
                    'context': {
                        'graph_measure': 'probable_income',
                        'graph_mode': 'line',
                        'graph_groupbys': ['date:' + self.group_by]
                    }
                }

    def tree_view_action(self):
        if self.group_by == "day":
            if self.chart_start or self.chart_end:
                return {
                    'name': 'Revenues List',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'view_id': False,
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'domain': [
                        '&', '&', '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id_test', '=', False),
                        ('parent', '=', self.name),
                        ('date', '>=', self.chart_start),
                        ('date', '<=', self.chart_end)
                    ],
                    'target': 'current'
                }
            else:
                return {
                    'name': 'Revenues List',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'view_id': False,
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'domain': [
                        '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id_test', '=', False),
                        ('parent', '=', self.name)
                    ],
                    'target': 'current'
                }
        else:
            if self.chart_start or self.chart_end:
                return {
                    'name': 'Revenues List',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'view_id': False,
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'context': {
                        'group_by': ['date:' + self.group_by]
                    },
                    'domain': [
                        '&', '&', '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id_test', '=', False),
                        ('parent', '=', self.name),
                        ('date', '>=', self.chart_start),
                        ('date', '<=', self.chart_end)
                    ],
                    'target': 'current'
                }
            else:
                return {
                    'name': 'Revenues List',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'view_id': False,
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'context': {
                        'group_by': ['date:' + self.group_by]
                    },
                    'domain': [
                        '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id_test', '=', False),
                        ('parent', '=', self.name)
                    ],
                    'target': 'current'
                }

    def graph_test_view_action(self):
        if self.group_by_test == "day":
            if self.chart_start_test or self.chart_end_test:
                return {
                    'name': 'Revenues Analysis',
                    'view_type': 'graph',
                    'view_mode': 'graph',
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'domain': [
                        '&', '&', '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id', '=', False),
                        ('parent', '=', self.name),
                        ('date', '>=', self.chart_start_test),
                        ('date', '<=', self.chart_end_test)
                    ],
                    'context': {
                        'graph_measure': 'probable_income',
                        'graph_mode': 'line'
                    }
                }
            else:
                return {
                    'name': 'Revenues Analysis',
                    'view_type': 'graph',
                    'view_mode': 'graph',
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'domain': [
                        '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id', '=', False),
                        ('parent', '=', self.name)
                    ],
                    'context': {
                        'graph_measure': 'probable_income',
                        'graph_mode': 'line'
                    }
                }
        else:
            if self.chart_start_test or self.chart_end_test:
                return {
                    'name': 'Revenues Analysis',
                    'view_type': 'graph',
                    'view_mode': 'graph',
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'domain': [
                        '&', '&', '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id', '=', False),
                        ('parent', '=', self.name),
                        ('date', '>=', self.chart_start_test),
                        ('date', '<=', self.chart_end_test)
                    ],
                    'context': {
                        'graph_measure': 'probable_income',
                        'graph_mode': 'line',
                        'graph_groupbys': ['date:' + self.group_by_test]
                    }
                }
            else:
                return {
                    'name': 'Revenues Analysis',
                    'view_type': 'graph',
                    'view_mode': 'graph',
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'domain': [
                        '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id', '=', False),
                        ('parent', '=', self.name)
                    ],
                    'context': {
                        'graph_measure': 'probable_income',
                        'graph_mode': 'line',
                        'graph_groupbys': ['date:' + self.group_by_test]
                    }
                }

    def tree_test_view_action(self):
        if self.group_by_test == "day":
            if self.chart_start_test or self.chart_end_test:
                return {
                    'name': 'Revenues List',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'view_id': False,
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'domain': [
                        '&', '&', '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id', '=', False),
                        ('parent', '=', self.name),
                        ('date', '>=', self.chart_start_test),
                        ('date', '<=', self.chart_end_test)
                    ],
                    'target': 'current'
                }
            else:
                return {
                    'name': 'Revenues List',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'view_id': False,
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'domain': [
                        '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id', '=', False),
                        ('parent', '=', self.name)
                    ],
                    'target': 'current'
                }
        else:
            if self.chart_start_test or self.chart_end_test:
                return {
                    'name': 'Revenues List',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'view_id': False,
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'context': {
                        'group_by': ['date:' + self.group_by_test]
                    },
                    'domain': [
                        '&', '&', '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id', '=', False),
                        ('parent', '=', self.name),
                        ('date', '>=', self.chart_start_test),
                        ('date', '<=', self.chart_end_test)
                    ],
                    'target': 'current'
                }
            else:
                return {
                    'name': 'Revenues List',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'view_id': False,
                    'res_model': 'amazon.revenues.line',
                    'type': 'ir.actions.act_window',
                    'context': {
                        'group_by': ['date:' + self.group_by_test]
                    },
                    'domain': [
                        '&', '&',
                        ('product', '=', self.product.id),
                        ('amazon_revenues_line_id', '=', False),
                        ('parent', '=', self.name)
                    ],
                    'target': 'current'
                }
