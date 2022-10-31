from odoo import models, fields


class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"

    fiscal_position_id = fields.Many2one(
        "account.fiscal.position",
        string = "Fiscal Position",
        domain = "[('company_id', '=', company_id)]",
        check_company = True,
        help = "Fiscal positions are used to adapt taxes "
               "and accounts for particular customers or sales orders/invoices. "
               "The default value comes from the customer."
    )
