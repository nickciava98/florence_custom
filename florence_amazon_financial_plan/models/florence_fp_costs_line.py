from odoo import models, fields


class FlorenceFpCostsLine(models.Model):
    _name = "florence.fp.costs.line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Florence FP Costs Line"

    name = fields.Many2one(
        "florence.fp.costs",
        ondelete = "cascade"
    )
    component = fields.Many2one(
        "product.product"
    )
    cost = fields.Float(
        digits = (12, 4),
        # compute = "_compute_cost",
        # store = True
    )
    vendor = fields.Many2one(
        "res.partner",
        related = "bill.partner_id"
    )
    bill = fields.Many2one(
        "account.move",
        # compute = "_compute_bill",
        # store = True
    )
    bill_date = fields.Date(
        related = "bill.invoice_date"
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute = "_compute_currency_id"
    )

    # @api.depends("component")
    # def _compute_bill(self):
    #     for line in self:
    #         line.bill = False
    #
    #         if line.component:
    #             year = line.name.date.strftime("%Y")
    #             month = line.name.date.strftime("%m")
    #
    #             for bill in self.env["account.move"].search(
    #                 ["&", "&",
    #                  ("move_type", "=", "in_invoice"),
    #                  ("invoice_date", ">=", year + "-" + month + "-1"),
    #                  ("invoice_date", "<=", year + "-" +  month + "-" + str(calendar.monthrange(int(year), int(month))[1]))],
    #                 order = "name desc"):
    #                 for invoice_line in bill.invoice_line_ids:
    #                     if invoice_line.product_id == line.component:
    #                         line.bill = bill
    #                         break
    #
    #                 if line.bill:
    #                     break
    #
    # @api.depends("component", "bill")
    # def _compute_cost(self):
    #     for line in self:
    #         line.cost = 0
    #
    #         if line.component:
    #             year = line.name.date.strftime("%Y")
    #             month = line.name.date.strftime("%m")
    #
    #             for bill in self.env["account.move"].search(
    #                 ["&", "&",
    #                  ("move_type", "=", "in_invoice"),
    #                  ("invoice_date", ">=", year + "-" + month + "-1"),
    #                  ("invoice_date", "<=", year + "-" + month + "-" + str(calendar.monthrange(int(year), int(month))[1]))],
    #                 order = "name desc"):
    #                 for invoice_line in bill.invoice_line_ids:
    #                     if invoice_line.product_id == line.component:
    #                         line.cost = invoice_line.price_unit
    #                         break
    #
    #                 if line.cost > 0:
    #                     break

    def _compute_currency_id(self):
        for line in self:
            line.currency_id = self.env.ref("base.main_company").currency_id
