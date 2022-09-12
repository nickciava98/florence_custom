from odoo import models, fields, api

class EmployeesStatisticsBenchmark(models.Model):
    _name = "employees.statistics.benchmark"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Employees Statistics Benchmark"

    name = fields.Char(
        required = True
    )
    job_position = fields.Many2one(
        "hr.job",
        required = True
    )
