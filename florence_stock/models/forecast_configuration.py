from odoo import models, fields


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

    def send_stock_forecast_reminder_action(self):
        for conf in self.search([]):
            for partner in conf.partner_ids:
                conf.partner_id = partner

                self.env.ref(
                    "florence_stock.stock_forecast_reminder_mail_template"
                ).send_mail(conf.id, force_send = True)
