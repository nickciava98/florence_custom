from odoo import models, fields


class FlorenceFinancialPlanLine(models.Model):
    _name = "florence.financial.plan.line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Financial Plan Line"

    basics_id = fields.Many2one(
        "florence.financial.plan"
    )
    emergencies_id = fields.Many2one(
        "florence.financial.plan"
    )
    div1_id = fields.Many2one(
        "florence.financial.plan"
    )
    div2_id = fields.Many2one(
        "florence.financial.plan"
    )
    div3_id = fields.Many2one(
        "florence.financial.plan"
    )
    div4_id = fields.Many2one(
        "florence.financial.plan"
    )
    div5_id = fields.Many2one(
        "florence.financial.plan"
    )
    div6_id = fields.Many2one(
        "florence.financial.plan"
    )
    div7_id = fields.Many2one(
        "florence.financial.plan"
    )
    item = fields.Char()
    monthly = fields.Float()
    approved = fields.Float()
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref("base.main_company").currency_id