import datetime

from odoo import models, fields, api

class EmployeesStatistics(models.Model):
    _name = "employees.statistics"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Employees Statistics"

    name = fields.Many2one(
        "hr.employee",
        required = True
    )
    job_position = fields.Many2one(
        "hr.job",
        related = "name.job_id"
    )
    statistics_lines = fields.One2many(
        "employees.statistics.line",
        "name"
    )
    chart_start = fields.Date()
    chart_end = fields.Date()
    start_date = fields.Date(
        compute = "_compute_start_date"
    )

    def _compute_start_date(self):
        for line in self:
            line.start_date = datetime.datetime.now()

    def graph_view_action(self):
        return {
            'name': 'Employee\'s Statistics Chart',
            'view_type': 'graph',
            'view_mode': 'graph',
            'res_model': 'employees.statistics.line',
            'type': 'ir.actions.act_window',
            'context': {
                'graph_measure': 'value',
                'graph_mode': 'line',
                'graph_groupbys': ['week']
            },
            'domain': [
                '&', '&',
                ('date', '>=', self.chart_start),
                ('date', '<=', self.chart_end),
                ('name', 'ilike', self.name.name)
            ]
        }

    def tree_view_action(self):
        return {
            'name': 'Employee\'s Statistics List',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'employees.statistics.line',
            'type': 'ir.actions.act_window',
            'context': {
                'group_by': 'week'
            },
            'domain': [
                ('name', 'ilike', self.name.name)
            ],
            'target': 'current'
        }
