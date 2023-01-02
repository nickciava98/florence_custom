from odoo import fields, models, api


class ClickFunnel(models.Model):
    _name = "click.funnel"
    _description = "Click Funnel's funnel configuration"

    _sql_constraints = [
        ('click_funnel_id_uniq', 'unique (click_funnel_id, company_id)', 'The click funnel id must be unique per company !'),
    ]

    name = fields.Char(string='Funnel Name', required=True)
    description = fields.Char(string='Description')
    url = fields.Char(string='Funnel URL', required=True)
    active = fields.Boolean(default=True, help="Set active to false to hide the Funnel without removing it.")
    company_id = fields.Many2one(
        'res.company', string='Company',
        required=True,
        default=lambda self: self.env.company.id
    )
    click_funnel_id = fields.Integer(string='Click Funnel ID', required=True, index=True, copy=False)
    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse',
        required=True,
        check_company=True
    )

    journal_id = fields.Many2one('account.journal', store=True, readonly=False,
        compute='_compute_journals_id',
        domain="[('company_id', '=', company_id), ('type', '=', 'sale')]")

    payment_journal_id = fields.Many2one('account.journal', store=True, readonly=False,
        compute='_compute_journals_id',
        domain="[('company_id', '=', company_id), ('type', 'in', ('bank', 'cash'))]")

    user_id = fields.Many2one('res.users', string='Salesman', check_company=True)

    team_id = fields.Many2one('crm.team', string='Sales Team', check_company=True)

    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', check_company=True)

    fiscal_position_id = fields.Many2one(
        'account.fiscal.position', string='Fiscal Position',
        domain="[('company_id', '=', company_id)]", check_company=True,
        help="Fiscal positions are used to adapt taxes and accounts for particular customers or sales orders/invoices."
        "The default value comes from the customer."
    )

    auto_followers = fields.Many2many(
        'res.partner', string='Auto Followers',
        help='Followers added automatically to the sale order',
        check_company=True
    )

    can_confirm_sale = fields.Boolean(string='Automatic Sale Order Confirm')

    can_send_confirmation_email = fields.Boolean(string=' Send Email Confirmation')

    confirmation_email_template_id = fields.Many2one(
        'mail.template',
        domain="[('model', '=', 'sale.order')]",
        help="Email Template to use as Sale Order confirmation. If empty uses the default"
    )

    sale_ids = fields.One2many(
        'sale.order', 'click_funnel_id',
        string='Sale Orders'
    )

    can_create_invoice = fields.Boolean(string='Automatic Create Invoice')

    can_send_invoice_confirmation_email = fields.Boolean(string=' Send Invoice Email Confirmation')

    invoice_email_template_id = fields.Many2one(
        'mail.template',
        domain="[('model', '=', 'account.move')]",
        help="Invoice email template. If empty uses the default"
    )

    lang_id = fields.Many2one('res.lang', string='Language', default=lambda self: self.lang_id.id)

    @api.depends('company_id')
    def _compute_journals_id(self):
        AccountJournal = self.env['account.journal']
        for funnel_id in self:
            funnel_id.journal_id = AccountJournal.search([
                ('type', '=', 'sale'),
                ('company_id', '=', funnel_id.company_id.id),
            ], limit=1)
            funnel_id.payment_journal_id = AccountJournal.search([
                ('type', 'in', ('bank', 'cash')),
                ('company_id', '=', funnel_id.company_id.id),
            ], limit=1)
