import calendar
import datetime

from odoo import models, fields, api


class FlorenceFinancialPlanLine(models.Model):
    _name = "florence.financial.plan.line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Financial Plan Line"
    _rec_name = "item"

    parent_id = fields.Many2one(
        "florence.financial.plan",
        ondelete="cascade",
        compute="_compute_parent_id",
        store=True
    )
    date = fields.Date(
        compute="_compute_date",
        store=True
    )
    basics_id = fields.Many2one(
        "florence.financial.plan",
        ondelete="cascade"
    )
    emergencies_id = fields.Many2one(
        "florence.financial.plan",
        ondelete="cascade"
    )
    div1_id = fields.Many2one(
        "florence.financial.plan",
        ondelete="cascade"
    )
    div2_id = fields.Many2one(
        "florence.financial.plan",
        ondelete="cascade"
    )
    div3_id = fields.Many2one(
        "florence.financial.plan",
        ondelete="cascade"
    )
    div4_id = fields.Many2one(
        "florence.financial.plan",
        ondelete="cascade"
    )
    div4a_id = fields.Many2one(
        "florence.financial.plan",
        ondelete="cascade"
    )
    div5_id = fields.Many2one(
        "florence.financial.plan",
        ondelete="cascade"
    )
    div6_id = fields.Many2one(
        "florence.financial.plan",
        ondelete="cascade"
    )
    div7_id = fields.Many2one(
        "florence.financial.plan",
        ondelete="cascade"
    )
    expenses_id = fields.Many2one(
        "florence.financial.plan",
        ondelete="cascade"
    )
    item = fields.Char()
    product = fields.Many2one(
        "product.product"
    )
    is_deductible = fields.Boolean(
        default=False
    )
    quantity = fields.Float(
        default=.0
    )
    moq = fields.Float(
        default=.0,
        string="MOQ"
    )
    is_single_cost = fields.Boolean(
        default=False,
        string="Single Cost?"
    )
    monthly = fields.Float(
        default=.0,
        string="Monthly Cost"
    )
    monthly_computed = fields.Float(
        compute="_compute_monthly_computed",
        string="Computed Monthly"
    )
    total_to_compute = fields.Float(
        compute="_compute_total_to_compute",
    )
    approved = fields.Float(
        default=.0,
        string="Approved Cost"
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="parent_id.currency_id"
    )

    @api.depends("is_single_cost", "monthly", "monthly_computed", "approved")
    def _compute_total_to_compute(self):
        for line in self:
            approved = line.approved if line.is_single_cost else .0
            line.total_to_compute = sum([line.monthly, line.monthly_computed, approved])

    @api.depends("basics_id", "emergencies_id", "div1_id", "div2_id", "div3_id",
                 "div4_id", "div4a_id", "div5_id", "div6_id", "div7_id", "expenses_id")
    def _compute_parent_id(self):
        for line in self:
            line.parent_id = line.basics_id or line.emergencies_id or line.div1_id or line.div2_id \
                             or line.div3_id or line.div4_id or line.div4a_id or line.div5_id \
                             or line.div6_id or line.div7_id or line.expenses_id

    @api.depends("basics_id", "emergencies_id", "div1_id", "div2_id", "div3_id",
                 "div4_id", "div4a_id", "div5_id", "div6_id", "div7_id", "expenses_id")
    def _compute_date(self):
        for line in self:
            line.date = line.basics_id.date \
                if line.basics_id else line.emergencies_id.date \
                if line.emergencies_id else line.div1_id.date \
                if line.div1_id else line.div2_id.date \
                if line.div2_id else line.div3_id.date \
                if line.div3_id else line.div4_id.date \
                if line.div4_id else line.div5_id.date \
                if line.div5_id else line.div6_id.date \
                if line.div6_id else line.div7_id.date \
                if line.div7_id else datetime.datetime.today()

    @api.depends("product", "date", "moq")
    def _compute_monthly_computed(self):
        for line in self:
            line.monthly_computed = .0

            if line.date and line.product:
                year = line.date.strftime("%Y")
                month = line.date.strftime("%m")
                last_day = str(calendar.monthrange(int(year), int(month))[1])
                domain = [
                    "&",
                    ("date", "<=", year + "-" + month + "-" + last_day), ("component", "=", line.product.id)
                ]
                fp_costs_line_id = self.env["florence.fp.costs.line"].search(domain, order="date desc", limit=1)

                if fp_costs_line_id:
                    line.monthly_computed = line.moq * fp_costs_line_id.cost \
                        if fp_costs_line_id.component.id != fp_costs_line_id.name.name.id \
                        else line.moq * fp_costs_line_id.name.total \
                        if fp_costs_line_id.component.id == fp_costs_line_id.name.name.id else .0
