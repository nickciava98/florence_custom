from odoo import models, fields, api
from odoo.exceptions import ValidationError
import math


class ForecastConfiguration(models.Model):
    _name = "forecast.configuration"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Forecast Configuration"

    name = fields.Char(
        default = "Forecast Configuration"
    )
    user_id = fields.Many2one(
        "res.users",
        string = "Email From"
    )
    partner_id = fields.Many2one(
        "res.partner"
    )
    partner_ids = fields.Many2many(
        "res.partner",
        "res_partner_forecast_configuration_rel",
        string = "Partner To"
    )
    months_treshold = fields.Float(
        default = 2.0,
        help = "Minimum Months Autonomy Allowed for Stock items"
    )

    @api.constrains("months_treshold")
    def _constrains_months_treshold(self):
        for line in self:
            if line.months_treshold < 0.0 or math.isclose(line.months_treshold, 0.0):
                raise ValidationError(
                    "Months Treshold must be greater than zero!"
                )

    def send_stock_forecast_reminder_action(self):
        for conf in self.search([]):
            for partner in conf.partner_ids:
                conf.partner_id = partner

                self.env.ref(
                    "florence_stock.stock_forecast_reminder_mail_template"
                ).send_mail(conf.id, force_send = True)
