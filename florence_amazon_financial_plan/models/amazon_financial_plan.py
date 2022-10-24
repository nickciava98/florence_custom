from odoo import models, fields, api
import datetime


class AmazonFinancialPlan(models.Model):
    _name = "amazon.financial.plan"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Amazon Financial Plan"

    name = fields.Char(
        required = True
    )
    date = fields.Date(
        default = datetime.datetime.now(),
        required = True
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )
    total_value = fields.Float(
        compute = "_compute_total_value",
        store = True
    )
    total_used = fields.Float(
        compute = "_compute_total_used",
        store = True
    )
    total_to_use = fields.Float(
        compute = "_compute_total_to_use",
        store = True
    )
    amazon_financial_plan_lines = fields.One2many(
        "amazon.financial.plan.line",
        "name"
    )

    @api.depends("amazon_financial_plan_lines")
    def _compute_total_value(self):
        for line in self:
            line.total_value = 0

            for fp in line.amazon_financial_plan_lines:
                line.total_value += fp.value

    @api.depends("amazon_financial_plan_lines")
    def _compute_total_used(self):
        for line in self:
            line.total_used = 0

            for fp in line.amazon_financial_plan_lines:
                if fp.value_used:
                    line.total_used += fp.value

    @api.depends("amazon_financial_plan_lines")
    def _compute_total_to_use(self):
        for line in self:
            line.total_to_use = 0

            for fp in line.amazon_financial_plan_lines:
                if not fp.value_used:
                    line.total_to_use += fp.value

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref('base.main_company').currency_id

    def fp_by_date_action(self):
        for fp in self.env["amazon.financial.plan.line"].search([("name", "=", self.id)]):
            fp.write({
                'total_used': self.total_used,
                'total_to_use': self.total_to_use
            })

        return {
            'name': 'FP by date',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'amazon.financial.plan.line',
            'type': 'ir.actions.act_window',
            'context': {
                'group_by': ['date:day']
            },
            'domain': [
                ('name', '=', self.id)
            ],
            'target': 'current'
        }

    def fp_by_product_action(self):
        for fp in self.env["amazon.financial.plan.line"].search([("name", "=", self.id)]):
            fp.write({
                'total_used': self.total_used,
                'total_to_use': self.total_to_use
            })

        return {
            'name': 'FP by product',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'amazon.financial.plan.line',
            'type': 'ir.actions.act_window',
            'context': {
                'group_by': ['date:day', 'product_id']
            },
            'domain': [
                ('name', '=', self.id)
            ],
            'target': 'current'
        }
