from odoo import models, fields


class DateInterval(models.TransientModel):
    _name = "date.interval"
    _description = "Date Interval"

    marketplace = fields.Char()
    start_date = fields.Date()
    end_date = fields.Date()

    def apply_action(self):
        return {
            'name': self.marketplace,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'amazon.revenues.line',
            'type': 'ir.actions.act_window',
            'domain': [
                '&', '&', '&',
                ('amazon_revenues_line_id_test', '=', False),
                ('parent', '=', self.marketplace.split()[1]),
                ('date', '>=', self.start_date),
                ('date', '<=', self.end_date)
            ],
            'context': {
                'group_by': ['date:day', 'product']
            },
            'target': 'main'
        }
