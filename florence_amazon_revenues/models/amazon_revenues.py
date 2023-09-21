from datetime import datetime

from odoo.exceptions import ValidationError

from odoo import models, fields, api, _


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
        copy=False,
        string="Marketplace",
        tracking=True
    )
    product = fields.Many2one(
        "product.template",
        required=True,
        tracking=True
    )
    product_updated_price = fields.Float(
        compute="_compute_product_updated_price"
    )
    start_date = fields.Date(
        compute="_compute_start_date"
    )
    total_probable_income = fields.Float(
        compute="_compute_total_probable_income",
        store=True,
        string="Total Probable Income (Odoo)"
    )
    total_probable_income_amz = fields.Float(
        compute="_compute_total_probable_income_amz",
        store=True,
        string="Total Probable Income (Amazon)"
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
        compute="_compute_currency_id"
    )
    product_updated_sku_cost = fields.Float(
        compute="_compute_product_updated_sku_cost"
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
    last_amazon_fees = fields.Float(
        compute="_compute_last_amazon_fees"
    )
    last_ads_total_cost = fields.Float(
        compute="_compute_last_ads_total_cost"
    )
    last_pcs_sold = fields.Float(
        compute="_compute_last_pcs_sold"
    )

    @api.depends("revenues_line")
    def _compute_last_amazon_fees(self):
        for line in self:
            line.last_amazon_fees = line.revenues_line[-1].amazon_fees if line.revenues_line else .0

    @api.depends("revenues_line")
    def _compute_last_ads_total_cost(self):
        for line in self:
            line.last_ads_total_cost = line.revenues_line[-1].ads_total_cost if line.revenues_line else .0

    @api.depends("revenues_line")
    def _compute_last_pcs_sold(self):
        for line in self:
            line.last_pcs_sold = line.revenues_line[-1].pcs_sold if line.revenues_line else .0

    @api.onchange("name")
    def _onchange_name(self):
        for line in self:
            if line.revenues_line:
                for revenues_line in line.revenues_line:
                    revenues_line.parent = line.name

            if line.revenues_line_test:
                for revenues_line_test in line.revenues_line_test:
                    revenues_line_test.parent = line.name

    @api.onchange("product")
    def _onchange_product(self):
        for line in self:
            if line.revenues_line:
                for revenues_line in line.revenues_line:
                    revenues_line.product = line.product

            if line.revenues_line_test:
                for revenues_line_test in line.revenues_line_test:
                    revenues_line_test.product = line.product

    @api.depends("product")
    def _compute_product_updated_sku_cost(self):
        for line in self:
            fp_cost = self.env["florence.fp.costs"].search([]).filtered(
                lambda f: f.name.product_tmpl_id.id == line.product.id
            )
            line.product_updated_sku_cost = fp_cost[0].total if fp_cost else .0

    def _compute_start_date(self):
        for line in self:
            line.start_date = datetime.now()

    @api.depends("product")
    def _compute_product_updated_price(self):
        for line in self:
            line.product_updated_price = line.product.list_price \
                if line.product.list_price > .0 else line.product.lst_price

    @api.depends("revenues_line")
    def _compute_total_probable_income(self):
        for line in self:
            line.total_probable_income = sum([
                revenues_line.probable_income for revenues_line in line.revenues_line.filtered(
                    lambda r: r.probable_income
                )
            ])

    @api.depends("revenues_line")
    def _compute_total_probable_income_amz(self):
        for line in self:
            line.total_probable_income_amz = sum([
                revenues_line.probable_income_amz for revenues_line in line.revenues_line.filtered(
                    lambda r: r.probable_income_amz
                )
            ])

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

    @api.constrains("name")
    def _constrains_name(self):
        for line in self:
            if not line.name:
                raise ValidationError(
                    _("Name must be filled!")
                )

    _sql_constraint = [
        ("unique_name", "unique(name)", _("Name must be unique!"))
    ]
