from odoo import models, fields, api
from datetime import datetime, timedelta
import locale


class EmployeesStatisticsLine(models.Model):
    _name = "employees.statistics.line"
    _description = "Employees Statistics Line"

    name = fields.Many2one(
        "employees.statistics",
        ondelete = "cascade"
    )
    job_position = fields.Many2one(
        "hr.job",
        related = "name.job_position"
    )
    benchmark = fields.Many2one(
        "employees.statistics.benchmark",
        domain = "[('job_position', '=', job_position)]"
    )
    date = fields.Date()
    value = fields.Float()
    week = fields.Char(
        compute = "_compute_week",
        store = True
    )

    def _compute_week(self):
        for line in self:
            odoo_locale = self.env["res.users"].search([("id", "=", line.create_uid.id)]).lang
            locale.setlocale(locale.LC_TIME, odoo_locale + ".UTF-8")
            line.week = ""

            dt = datetime.strptime(str(line.date), "%Y-%m-%d")
            start = dt - timedelta(days = dt.weekday())
            end = start + timedelta(days = 6)

            line.week = datetime.strptime(str(line.date), "%Y-%m-%d").strftime("%B") \
                        + " " + str(datetime.strptime(str(line.date), "%Y-%m-%d").year) \
                        + ", " + start.strftime("%d") + "-" + end.strftime("%d")
