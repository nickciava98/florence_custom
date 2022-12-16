from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import datetime


class EmployeesStatistics(models.Model):
    _name = "employees.statistics"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Employees Statistics"

    name = fields.Many2one(
        "hr.employee",
        copy = False
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
    benchmark = fields.Many2one(
        "employees.statistics.benchmark",
        domain = "[('job_position', '=', job_position)]"
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
                '&', '&', '&',
                ('date', '>=', self.chart_start),
                ('date', '<=', self.chart_end),
                ('name', '=', self.name.name),
                ('benchmark', '=', self.benchmark.id)
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
                ('name', '=', self.name.name)
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
