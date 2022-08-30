from odoo import models, fields, api

class EmployeesStatisticsLine(models.Model):
    _name = "employees.statistics.line"
    _description = "Employees Statistics Line"

    name = fields.Many2one(
        "employees.statistics"
    )
    date = fields.Date()
    benchmark = fields.Many2one(
        "employees.statistics.benchmark"
    )
    value = fields.Float()
