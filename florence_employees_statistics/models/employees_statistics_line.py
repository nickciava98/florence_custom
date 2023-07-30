import locale
from datetime import datetime, timedelta

from odoo import models, fields, api


class EmployeesStatisticsLine(models.Model):
    _name = "employees.statistics.line"
    _description = "Employees Statistics Line"

    name = fields.Many2one(
        "employees.statistics",
        ondelete="cascade"
    )
    job_position = fields.Many2one(
        "hr.job",
        related="name.job_position"
    )
    benchmark = fields.Many2one(
        "employees.statistics.benchmark",
        domain="[('job_position', '=', job_position)]"
    )
    date = fields.Date()
    value = fields.Float(
        digits=(12, 4)
    )
    week = fields.Char(
        compute="_compute_week",
        store=True
    )

    @api.depends("date")
    def _compute_week(self):
        locale.setlocale(locale.LC_TIME, "en_US.UTF-8")

        for line in self:
            line.week = ""

            if line.date:
                dt = datetime.strptime(str(line.date), "%Y-%m-%d")
                start = dt - timedelta(days=dt.weekday())
                end = start + timedelta(days=6)

                line.week = datetime.strptime(str(line.date), "%Y-%m-%d").strftime("%B") \
                            + " " + str(datetime.strptime(str(line.date), "%Y-%m-%d").year) \
                            + ", " + start.strftime("%d") + "-" + end.strftime("%d")
