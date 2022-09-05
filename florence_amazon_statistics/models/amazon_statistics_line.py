from odoo import models, fields, api

class AmazonStatisticsLine(models.Model):
    _name = "amazon.statistics.line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Amazon Statistics Line"

    name = fields.Many2one(
        "amazon.statistics"
    )
    parent = fields.Char()
    product = fields.Many2one(
        "product.template"
    )
    date = fields.Date()

    one_vote_ratings_new = fields.Float(
        compute = "_compute_one_vote_ratings_new"
    )
    one_star_ratings = fields.Float()
    one_star_reviews = fields.Float()
    total_one_star_reviews = fields.Float()
    one_star_value = fields.Float()

    two_votes_ratings_new = fields.Float()
    two_stars_ratings = fields.Float()
    two_stars_reviews = fields.Float()
    two_stars_reviews_new = fields.Float()
    total_two_stars_reviews = fields.Float()
    two_stars_value = fields.Float()

    three_votes_ratings_new = fields.Float()
    three_stars_ratings = fields.Float()
    three_stars_reviews = fields.Float()
    three_stars_reviews_new = fields.Float()
    total_three_stars_reviews = fields.Float()
    three_stars_value = fields.Float()

    four_votes_ratings_new = fields.Float()
    four_stars_ratings = fields.Float()
    four_stars_reviews = fields.Float()
    four_stars_reviews_new = fields.Float()
    total_four_stars_reviews = fields.Float()
    four_stars_value = fields.Float()

    five_votes_ratings_new = fields.Float()
    five_stars_ratings = fields.Float()
    five_stars_reviews = fields.Float()
    five_stars_reviews_new = fields.Float()
    total_five_stars_reviews = fields.Float()
    five_stars_value = fields.Float()

    daily_main_stat = fields.Float()
    weekly_main_stat = fields.Float()
    monthly_main_stat = fields.Float()

    five_reviews_perc = fields.Float()
    four_reviews_perc = fields.Float()
    three_reviews_perc = fields.Float()
    two_reviews_perc = fields.Float()
    one_reviews_perc = fields.Float()
    
    da_five_perc = fields.Float()
    
    freshness = fields.Float()
    absorbency = fields.Float()
    quality_price = fields.Float()
    comfort = fields.Float()
    hydration = fields.Float()
    solar_protection = fields.Float()

    ncx_rate_perc = fields.Float()
    total_orders = fields.Float()
    returns = fields.Float()

    performance_quality_inadequate = fields.Float()
    defective_item_perc = fields.Float()
    damage_item_perc = fields.Float()
    inaccurate_website_description_perc = fields.Float()
    wrong_item_was_sent_perc = fields.Float()
    missing_parts_accessories_perc = fields.Float()

    @api.depends("one_star_ratings")
    def _compute_one_vote_ratings_new(self):
        for line in self:
            line.one_vote_ratings_new = 0
