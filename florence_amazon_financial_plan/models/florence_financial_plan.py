import calendar
import datetime
import math

from odoo import models, fields, api, _


class FlorenceFinancialPlan(models.Model):
    _name = "florence.financial.plan"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Financial Plan"

    name = fields.Char(
        copy=False
    )
    date = fields.Date(
        default=datetime.datetime.now(),
        required=True,
        string="Original Date"
    )
    date_str = fields.Char(
        compute="_compute_date_str",
        store=True,
        string="Date"
    )
    gi = fields.Float(
        string="G.I.",
        compute="_compute_gi"
    )
    vat = fields.Float(
        compute="_compute_vat",
        string="VAT"
    )
    cgi = fields.Float(
        string="C.G.I.",
        compute="_compute_cgi"
    )
    perc = fields.Float(
        string="10% Shares",
        compute="_compute_perc"
    )
    monthly_total = fields.Float(
        compute="_compute_monthly_total"
    )
    approved_total = fields.Float(
        compute="_compute_approved_total"
    )
    disbursment = fields.Float(
        compute="_compute_disbursment"
    )
    deductible_total = fields.Float(
        compute="_compute_deductible_total"
    )
    taxable = fields.Float(
        compute="_compute_taxable"
    )
    taxes = fields.Float(
        compute="_compute_taxes"
    )
    surplus = fields.Float(
        compute="_compute_surplus"
    )
    pending = fields.Float(
        copy=True
    )

    basics = fields.One2many(
        "florence.financial.plan.line",
        "basics_id",
        copy=True
    )
    basics_condition = fields.Char(
        string="Basics - Condition",
        copy=True
    )
    emergencies = fields.One2many(
        "florence.financial.plan.line",
        "emergencies_id",
        copy=True
    )
    emergencies_condition = fields.Char(
        string="Emergencies - Condition",
        copy=True
    )
    div1 = fields.One2many(
        "florence.financial.plan.line",
        "div1_id",
        copy=True
    )
    div1_condition = fields.Char(
        string="DIV1 - Condition",
        copy=True
    )
    div2 = fields.One2many(
        "florence.financial.plan.line",
        "div2_id",
        copy=True
    )
    div2_condition = fields.Char(
        string="DIV2 - Condition",
        copy=True
    )
    div3 = fields.One2many(
        "florence.financial.plan.line",
        "div3_id",
        copy=True
    )
    div3_condition = fields.Char(
        string="DIV3 - Condition",
        copy=True
    )
    div4 = fields.One2many(
        "florence.financial.plan.line",
        "div4_id",
        copy=True
    )
    div4_condition = fields.Char(
        string="DIV4 - Condition",
        copy=True
    )
    div4a = fields.One2many(
        "florence.financial.plan.line",
        "div4a_id",
        copy=True
    )
    div4a_condition = fields.Char(
        string="DIV4A - Condition",
        copy=True
    )
    div5 = fields.One2many(
        "florence.financial.plan.line",
        "div5_id",
        copy=True
    )
    div5_condition = fields.Char(
        string="DIV5 - Condition",
        copy=True
    )
    div6 = fields.One2many(
        "florence.financial.plan.line",
        "div6_id",
        copy=True
    )
    div6_condition = fields.Char(
        string="DIV6 - Condition",
        copy=True
    )
    div7 = fields.One2many(
        "florence.financial.plan.line",
        "div7_id",
        copy=True
    )
    div7_condition = fields.Char(
        string="DIV7 - Condition",
        copy=True
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute="_compute_currency_id"
    )
    amz_total_it = fields.Float(
        default=.0
    )
    amz_vat_it = fields.Float(
        default=.0
    )
    amz_net_it = fields.Float(
        compute="_compute_amz_net_it",
        store=True,
        string="Amazon IT Net Income"
    )
    amz_total_fr = fields.Float(
        default=.0
    )
    amz_vat_fr = fields.Float(
        default=.0
    )
    amz_net_fr = fields.Float(
        compute="_compute_amz_net_fr",
        store=True,
        string="Amazon FR Net Income"
    )
    amz_total_de = fields.Float(
        default=.0
    )
    amz_vat_de = fields.Float(
        default=.0
    )
    amz_net_de = fields.Float(
        compute="_compute_amz_net_de",
        store=True,
        string="Amazon DE Net Income"
    )
    amz_total_es = fields.Float(
        default=.0
    )
    amz_vat_es = fields.Float(
        default=.0
    )
    amz_net_es = fields.Float(
        compute="_compute_amz_net_es",
        store=True,
        string="Amazon ES Net Income"
    )
    amz_total_uk = fields.Float(
        default=.0
    )
    amz_vat_uk = fields.Float(
        default=.0
    )
    amz_net_uk = fields.Float(
        compute="_compute_amz_net_uk",
        store=True,
        string="Amazon UK Net Income"
    )

    @api.depends("div1", "div2", "div3", "div4", "div4a", "div5", "div6", "div7", "basics", "emergencies")
    def _compute_deductible_total(self):
        for line in self:
            line.deductible_total = .0
            div1 = line.div1.filtered(lambda item: item.is_deductible)
            div2 = line.div2.filtered(lambda item: item.is_deductible)
            div3 = line.div3.filtered(lambda item: item.is_deductible)
            div4 = line.div4.filtered(lambda item: item.is_deductible)
            div5 = line.div5.filtered(lambda item: item.is_deductible)
            div6 = line.div6.filtered(lambda item: item.is_deductible)
            div7 = line.div7.filtered(lambda item: item.is_deductible)
            basics = line.basics.filtered(lambda item: item.is_deductible)
            emergencies = line.emergencies.filtered(lambda item: item.is_deductible)
            line.deductible_total += sum([item.approved for item in div1]) if div1 else .0
            line.deductible_total += sum([item.approved for item in div2]) if div2 else .0
            line.deductible_total += sum([item.approved for item in div3]) if div3 else .0
            line.deductible_total += sum([item.approved for item in div4]) if div4 else .0
            line.deductible_total += sum([item.approved for item in div5]) if div5 else .0
            line.deductible_total += sum([item.approved for item in div6]) if div6 else .0
            line.deductible_total += sum([item.approved for item in div7]) if div7 else .0
            line.deductible_total += sum([item.approved for item in basics]) if basics else .0
            line.deductible_total += sum([item.approved for item in emergencies]) if emergencies else .0

    @api.depends("disbursment", "deductible_total")
    def _compute_taxable(self):
        for line in self:
            line.taxable = line.disbursment - line.deductible_total

    @api.depends("taxable")
    def _compute_taxes(self):
        for line in self:
            line.taxes = .2 * line.taxable

    @api.depends("date")
    def _compute_date_str(self):
        for line in self:
            line.date_str = line.date.strftime("%m/%d/%Y") if line.date else ""

    @api.depends("amz_total_it", "amz_vat_it")
    def _compute_amz_net_it(self):
        for line in self:
            line.amz_net_it = line.amz_total_it - line.amz_vat_it

    @api.depends("amz_total_fr", "amz_vat_fr")
    def _compute_amz_net_fr(self):
        for line in self:
            line.amz_net_fr = line.amz_total_fr - line.amz_vat_fr

    @api.depends("amz_total_de", "amz_vat_de")
    def _compute_amz_net_de(self):
        for line in self:
            line.amz_net_de = line.amz_total_de - line.amz_vat_de

    @api.depends("amz_total_es", "amz_vat_es")
    def _compute_amz_net_es(self):
        for line in self:
            line.amz_net_es = line.amz_total_es - line.amz_vat_es

    @api.depends("amz_total_uk", "amz_vat_uk")
    def _compute_amz_net_uk(self):
        for line in self:
            line.amz_net_uk = line.amz_total_uk - line.amz_vat_uk

    @api.depends("amz_total_it", "amz_total_fr", "amz_total_de", "amz_total_es", "amz_total_uk")
    def _compute_gi(self):
        for line in self:
            line.gi = sum([
                line.amz_total_it, line.amz_total_fr, line.amz_total_de, line.amz_total_es, line.amz_total_uk
            ])

    @api.depends("amz_vat_it", "amz_vat_fr", "amz_vat_de", "amz_vat_es", "amz_vat_uk")
    def _compute_vat(self):
        for line in self:
            line.vat = sum([
                line.amz_vat_it, line.amz_vat_fr, line.amz_vat_de, line.amz_vat_es, line.amz_vat_uk
            ])

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref("base.main_company").currency_id

    @api.depends("cgi")
    def _compute_perc(self):
        for line in self:
            line.perc = .1 * line.cgi if line.cgi else .0

    @api.depends("gi", "vat")
    def _compute_cgi(self):
        for line in self:
            line.cgi = line.gi - line.vat if line.gi and line.vat else .0

    @api.depends("cgi", "perc")
    def _compute_disbursment(self):
        for line in self:
            line.disbursment = line.cgi - line.perc if line.cgi and line.perc else .0

    @api.depends("basics", "emergencies", "div1", "div2", "div3", "div4", "div4a", "div5", "div6", "div7")
    def _compute_monthly_total(self):
        for line in self:
            line.monthly_total = .0
            line.monthly_total += sum([item.total_to_compute for item in line.basics])
            line.monthly_total += sum([item.total_to_compute for item in line.emergencies])
            line.monthly_total += sum([item.total_to_compute for item in line.div1])
            line.monthly_total += sum([item.total_to_compute for item in line.div2])
            line.monthly_total += sum([item.total_to_compute for item in line.div3])
            line.monthly_total += sum([item.total_to_compute for item in line.div4])
            line.monthly_total += sum([item.total_to_compute - item.monthly for item in line.div4a])
            line.monthly_total += sum([item.total_to_compute for item in line.div5])
            line.monthly_total += sum([item.total_to_compute for item in line.div6])
            line.monthly_total += sum([item.total_to_compute for item in line.div7])

    @api.depends("basics", "emergencies", "div1", "div2", "div3", "div4", "div5", "div6", "div7")
    def _compute_approved_total(self):
        for line in self:
            line.approved_total = .0
            line.approved_total += sum([item.approved for item in line.basics])
            line.approved_total += sum([item.approved for item in line.emergencies])
            line.approved_total += sum([item.approved for item in line.div1])
            line.approved_total += sum([item.approved for item in line.div2])
            line.approved_total += sum([item.approved for item in line.div3])
            line.approved_total += sum([item.approved for item in line.div4])
            line.approved_total += sum([item.approved for item in line.div5])
            line.approved_total += sum([item.approved for item in line.div6])
            line.approved_total += sum([item.approved for item in line.div7])

    @api.depends("disbursment", "approved_total")
    def _compute_surplus(self):
        for line in self:
            line.surplus = line.disbursment - line.approved_total

    @api.model_create_multi
    def create(self, vals_list):
        fps = super().create(vals_list)

        for fp in fps:
            fp.create_write_pie_object()

        return fps

    def write(self, vals):
        res = super().write(vals)

        if ("basics" in vals or "emergencies" in vals or "div1" in vals or "div2" in vals or "div3" in vals
                or "div4" in vals or "div5" in vals or "div6" in vals or "div7" in vals or "date" in vals
                or "surplus" in vals or "perc" in vals):
            for fp in self:
                fp.create_write_pie_object()

        return res

    def create_write_pie_object(self):
        production_cost = .0
        remuneration_cost = .0
        running_cost = .0

        if self.div4:
            production_cost += sum([item.approved for item in self.div4])

        if self.basics:
            remuneration_cost += sum([item.approved for item in self.basics if item.item and "Salar" in item.item])
            remuneration_cost += self.perc

        if self.div1:
            running_cost += sum([item.approved for item in self.div1])

        if self.div2:
            running_cost += sum([item.approved for item in self.div2])

        if self.div3:
            running_cost += sum([item.approved for item in self.div3])

        if self.div5:
            running_cost += sum([item.approved for item in self.div5])

        if self.div6:
            running_cost += sum([item.approved for item in self.div6])

        if self.div7:
            running_cost += sum([item.approved for item in self.div7])

        if self.basics:
            running_cost += sum([item.approved for item in self.basics if item.item and "Salar" not in item.item])

        if self.emergencies:
            running_cost += sum([item.approved for item in self.emergencies])

        total_costs = production_cost + remuneration_cost + running_cost + self.surplus
        pie_production_cost = self.env["florence.financial.plan.pie"].sudo().search(
            [("date", "=", self.date), ("name", "=", "Production Cost")], limit=1
        )
        data = {
            "name": "Production Cost",
            "date": self.date,
            "cost": production_cost,
            "percentage": (production_cost / total_costs) * 100 if not math.isclose(total_costs, .0) else .0
        }

        if not pie_production_cost:
            self.env["florence.financial.plan.pie"].sudo().create(data)
        else:
            pie_production_cost.sudo().write(data)

        pie_remuneration_cost = self.env["florence.financial.plan.pie"].sudo().search(
            [("date", "=", self.date), ("name", "=", "Remuneration Cost")], limit=1
        )
        data = {
            "name": "Remuneration Cost",
            "date": self.date,
            "cost": remuneration_cost,
            "percentage": (remuneration_cost / total_costs) * 100 if not math.isclose(total_costs, .0) else .0
        }

        if not pie_remuneration_cost:
            self.env["florence.financial.plan.pie"].sudo().create(data)
        else:
            pie_remuneration_cost.sudo().write(data)

        pie_running_cost = self.env["florence.financial.plan.pie"].sudo().search(
            [("date", "=", self.date), ("name", "=", "Running Cost")]
        )
        data = {
            "name": "Running Cost",
            "date": self.date,
            "cost": running_cost,
            "percentage": (running_cost / total_costs) * 100 if not math.isclose(total_costs, .0) else .0
        }

        if not pie_running_cost:
            self.env["florence.financial.plan.pie"].sudo().create(data)
        else:
            pie_running_cost.sudo().write(data)

        pie_profit = self.env["florence.financial.plan.pie"].sudo().search(
            [("date", "=", self.date), ("name", "=", "Profit")]
        )
        year = self.date.strftime("%Y")
        month = self.date.strftime("%m")
        last_day = str(calendar.monthrange(int(year), int(month))[1])
        new_surplus = sum([
            fp.surplus
            for fp in self.sudo().search(
                [("date", ">=", f"{year}-{month}-01"), ("date", "<=", f"{year}-{month}-{last_day}")]
            )
        ])
        data = {
            "name": "Profit",
            "date": self.date,
            "cost": new_surplus,
            "percentage": (new_surplus / total_costs) * 100 if not math.isclose(total_costs, .0) else .0
        }

        if not pie_profit:
            self.env["florence.financial.plan.pie"].sudo().create(data)
        else:
            pie_profit.sudo().write(data)

    _sql_constraint = [
        ("unique_name", "unique(name)", _("Name must be unique!"))
    ]

    def export_xlsx_action(self):
        fp_ids = [fp.id for fp in self]
        init_form_id = self.env.ref("florence_amazon_financial_plan.export_xlsx_florence_fp_init_view_form")

        return {
            "name": "Export XLSX Amazon VAT",
            "type": "ir.actions.act_window",
            "res_model": "export.xlsx.florence.financial.plan",
            "view_mode": "form",
            "view_type": "tree,form",
            "views": [(init_form_id.id, "form")],
            "context": {
                "default_florence_fp_ids": fp_ids
            },
            "target": "new"
        }


class FlorenceFinancialPlanPie(models.Model):
    _name = "florence.financial.plan.pie"
    _description = "Florence Financial Plan Pie"

    name = fields.Char()
    date = fields.Date()
    cost = fields.Float(
        default=.0,
        group_operator="avg"
    )
    percentage = fields.Float(
        default=.0
    )
