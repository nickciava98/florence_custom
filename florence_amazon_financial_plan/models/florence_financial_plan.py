from odoo import models, fields, api
import datetime


class FlorenceFinancialPlan(models.Model):
    _name = "florence.financial.plan"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence Financial Plan"

    name = fields.Char(
        required = True
    )
    date = fields.Date(
        default = datetime.datetime.now(),
        required = True,
        string = "Original Date"
    )
    date_str = fields.Char(
        compute = "_compute_date_str",
        store = True,
        string = "Date"
    )
    gi = fields.Float(
        string = "G.I.",
        compute = "_compute_gi"
    )
    vat = fields.Float(
        compute = "_compute_vat",
        string = "VAT"
    )
    cgi = fields.Float(
        string = "C.G.I.",
        compute = "_compute_cgi"
    )
    perc = fields.Float(
        string = "10% C.G.I.",
        compute = "_compute_perc"
    )
    monthly_total = fields.Float(
        compute = "_compute_monthly_total"
    )
    approved_total = fields.Float(
        compute = "_compute_approved_total"
    )
    disbursment = fields.Float(
        compute = "_compute_disbursment"
    )
    surplus = fields.Float(
        compute = "_compute_surplus"
    )
    pending = fields.Float(
        copy = True
    )

    basics = fields.One2many(
        "florence.financial.plan.line",
        "basics_id",
        copy = True
    )
    basics_condition = fields.Char(
        string = "Basics - Condition",
        copy = True
    )
    emergencies = fields.One2many(
        "florence.financial.plan.line",
        "emergencies_id",
        copy = True
    )
    emergencies_condition = fields.Char(
        string = "Emergencies - Condition",
        copy = True
    )
    div1 = fields.One2many(
        "florence.financial.plan.line",
        "div1_id",
        copy = True
    )
    div1_condition = fields.Char(
        string = "DIV1 - Condition",
        copy = True
    )
    div2 = fields.One2many(
        "florence.financial.plan.line",
        "div2_id",
        copy = True
    )
    div2_condition = fields.Char(
        string = "DIV2 - Condition",
        copy = True
    )
    div3 = fields.One2many(
        "florence.financial.plan.line",
        "div3_id",
        copy = True
    )
    div3_condition = fields.Char(
        string = "DIV3 - Condition",
        copy = True
    )
    div4 = fields.One2many(
        "florence.financial.plan.line",
        "div4_id",
        copy = True
    )
    div4_condition = fields.Char(
        string = "DIV4 - Condition",
        copy = True
    )
    div5 = fields.One2many(
        "florence.financial.plan.line",
        "div5_id",
        copy = True
    )
    div5_condition = fields.Char(
        string = "DIV5 - Condition",
        copy = True
    )
    div6 = fields.One2many(
        "florence.financial.plan.line",
        "div6_id",
        copy = True
    )
    div6_condition = fields.Char(
        string = "DIV6 - Condition",
        copy = True
    )
    div7 = fields.One2many(
        "florence.financial.plan.line",
        "div7_id",
        copy = True
    )
    div7_condition = fields.Char(
        string = "DIV7 - Condition",
        copy = True
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )
    amz_total_it = fields.Float(
        default = 0
    )
    amz_vat_it = fields.Float(
        default = 0
    )
    amz_net_it = fields.Float(
        compute = "_compute_amz_net_it",
        store = True,
        string = "Amazon IT Net Income"
    )
    amz_total_fr = fields.Float(
        default = 0
    )
    amz_vat_fr = fields.Float(
        default = 0
    )
    amz_net_fr = fields.Float(
        compute = "_compute_amz_net_fr",
        store = True,
        string = "Amazon FR Net Income"
    )
    amz_total_de = fields.Float(
        default = 0
    )
    amz_vat_de = fields.Float(
        default = 0
    )
    amz_net_de = fields.Float(
        compute = "_compute_amz_net_de",
        store = True,
        string = "Amazon DE Net Income"
    )
    amz_total_es = fields.Float(
        default = 0
    )
    amz_vat_es = fields.Float(
        default = 0
    )
    amz_net_es = fields.Float(
        compute = "_compute_amz_net_es",
        store = True,
        string = "Amazon ES Net Income"
    )
    amz_total_uk = fields.Float(
        default = 0
    )
    amz_vat_uk = fields.Float(
        default = 0
    )
    amz_net_uk = fields.Float(
        compute = "_compute_amz_net_uk",
        store = True,
        string = "Amazon UK Net Income"
    )

    @api.depends("date")
    def _compute_date_str(self):
        for line in self:
            line.date_str = ""

            if line.date:
                line.date_str = line.date.strftime("%m/%d/%Y")

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

    @api.depends("amz_total_it", "amz_total_fr",
                 "amz_total_de", "amz_total_es",
                 "amz_total_uk")
    def _compute_gi(self):
        for line in self:
            line.gi = line.amz_total_it + line.amz_total_fr \
                      + line.amz_total_de + line.amz_total_es \
                      + line.amz_total_uk

    @api.depends("amz_vat_it", "amz_vat_fr",
                 "amz_vat_de", "amz_vat_es",
                 "amz_vat_uk")
    def _compute_vat(self):
        for line in self:
            line.vat = line.amz_vat_it + line.amz_vat_fr \
                       + line.amz_vat_de + line.amz_vat_es \
                       + line.amz_vat_uk

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref("base.main_company").currency_id

    @api.depends("cgi")
    def _compute_perc(self):
        for line in self:
            line.perc = 0

            if line.cgi:
                line.perc = 0.1 * line.cgi

    @api.depends("gi", "vat")
    def _compute_cgi(self):
        for line in self:
            line.cgi = 0

            if line.gi and line.vat:
                line.cgi = line.gi - line.vat

    @api.depends("cgi", "perc")
    def _compute_disbursment(self):
        for line in self:
            line.disbursment = 0

            if line.cgi and line.perc:
                line.disbursment = line.cgi - line.perc

    @api.depends("basics", "emergencies",
                 "div1", "div2", "div3", "div4", "div5", "div6", "div7")
    def _compute_monthly_total(self):
        for line in self:
            line.monthly_total = 0

            if len(line.basics) > 0:
                for item in line.basics:
                    line.monthly_total += item.monthly
            if len(line.emergencies) > 0:
                for item in line.emergencies:
                    line.monthly_total += item.monthly
            if len(line.div1) > 0:
                for item in line.div1:
                    line.monthly_total += item.monthly
            if len(line.div2) > 0:
                for item in line.div2:
                    line.monthly_total += item.monthly
            if len(line.div3) > 0:
                for item in line.div3:
                    line.monthly_total += item.monthly
            if len(line.div4) > 0:
                for item in line.div4:
                    line.monthly_total += item.monthly
            if len(line.div5) > 0:
                for item in line.div5:
                    line.monthly_total += item.monthly
            if len(line.div6) > 0:
                for item in line.div6:
                    line.monthly_total += item.monthly
            if len(line.div7) > 0:
                for item in line.div7:
                    line.monthly_total += item.monthly

    @api.depends("basics", "emergencies",
                 "div1", "div2", "div3", "div4", "div5", "div6", "div7")
    def _compute_approved_total(self):
        for line in self:
            line.approved_total = 0

            if len(line.basics) > 0:
                for item in line.basics:
                    line.approved_total += item.approved
            if len(line.emergencies) > 0:
                for item in line.emergencies:
                    line.approved_total += item.approved
            if len(line.div1) > 0:
                for item in line.div1:
                    line.approved_total += item.approved
            if len(line.div2) > 0:
                for item in line.div2:
                    line.approved_total += item.approved
            if len(line.div3) > 0:
                for item in line.div3:
                    line.approved_total += item.approved
            if len(line.div4) > 0:
                for item in line.div4:
                    line.approved_total += item.approved
            if len(line.div5) > 0:
                for item in line.div5:
                    line.approved_total += item.approved
            if len(line.div6) > 0:
                for item in line.div6:
                    line.approved_total += item.approved
            if len(line.div7) > 0:
                for item in line.div7:
                    line.approved_total += item.approved

    @api.depends("disbursment", "approved_total")
    def _compute_surplus(self):
        for line in self:
            line.surplus = line.disbursment - line.approved_total
