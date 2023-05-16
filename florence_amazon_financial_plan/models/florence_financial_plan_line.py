from odoo import models, fields


class FlorenceFinancialPlanLine(models.Model):
    _name = "florence.financial.plan.line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Financial Plan Line"

    date = fields.Date()
    basics_id = fields.Many2one(
        "florence.financial.plan",
        ondelete = "cascade"
    )
    emergencies_id = fields.Many2one(
        "florence.financial.plan",
        ondelete = "cascade"
    )
    div1_id = fields.Many2one(
        "florence.financial.plan",
        ondelete = "cascade"
    )
    div2_id = fields.Many2one(
        "florence.financial.plan",
        ondelete = "cascade"
    )
    div3_id = fields.Many2one(
        "florence.financial.plan",
        ondelete = "cascade"
    )
    div4_id = fields.Many2one(
        "florence.financial.plan",
        ondelete = "cascade"
    )
    div5_id = fields.Many2one(
        "florence.financial.plan",
        ondelete = "cascade"
    )
    div6_id = fields.Many2one(
        "florence.financial.plan",
        ondelete = "cascade"
    )
    div7_id = fields.Many2one(
        "florence.financial.plan",
        ondelete = "cascade"
    )
    expenses_id = fields.Many2one(
        "florence.financial.plan",
        ondelete = "cascade"
    )
    item = fields.Char()
    is_deductible = fields.Boolean(
        default = False
    )
    quantity = fields.Float()
    monthly = fields.Float(
        string = "Monthly Cost"
    )
    approved = fields.Float(
        string = "Approved Cost"
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref("base.main_company").currency_id
