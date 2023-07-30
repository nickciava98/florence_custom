from odoo.exceptions import ValidationError

from odoo import models, fields, api, _


class EmployeesStatisticsBenchmark(models.Model):
    _name = "employees.statistics.benchmark"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Employees Statistics Benchmark"

    name = fields.Char(
        copy=False
    )
    job_position = fields.Many2one(
        "hr.job",
        required=True
    )

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
