from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = ['product.template', 'product.carousel.data']
    _name = 'product.template'

    is_discount = fields.Boolean(string='Discount ?')
    is_best_seller = fields.Boolean(string='Best Seller ?')
    is_new_arrival = fields.Boolean(string='New Arrival ?')
    is_special = fields.Boolean(string='Special For Today ?')
    is_upcoming = fields.Boolean(string='Upcoming Products ?')
    comming_soon_date = fields.Datetime(string='Up Coming Product')
    back_image = fields.Binary(string='Back Image')
