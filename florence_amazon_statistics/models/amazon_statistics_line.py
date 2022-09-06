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
    one_star_reviews_new = fields.Float(
        compute = "_compute_one_star_reviews_new"
    )
    total_one_star_reviews = fields.Float(
        compute = "_compute_total_one_star_reviews"
    )
    one_star_value = fields.Float(
        compute = "_compute_one_star_value"
    )

    two_votes_ratings_new = fields.Float(
        compute = "_compute_two_votes_ratings_new"
    )
    two_stars_ratings = fields.Float()
    two_stars_reviews = fields.Float()
    two_stars_reviews_new = fields.Float(
        compute = "_compute_two_stars_reviews_new"
    )
    total_two_stars_reviews = fields.Float(
        compute = "_compute_total_two_stars_reviews"
    )
    two_stars_value = fields.Float(
        compute = "_compute_two_stars_value"
    )

    three_votes_ratings_new = fields.Float(
        compute = "_compute_three_votes_ratings_new"
    )
    three_stars_ratings = fields.Float()
    three_stars_reviews = fields.Float()
    three_stars_reviews_new = fields.Float(
        compute = "_compute_three_stars_reviews_new"
    )
    total_three_stars_reviews = fields.Float(
        compute = "_compute_total_three_stars_reviews"
    )
    three_stars_value = fields.Float(
        compute = "_compute_three_stars_value"
    )

    four_votes_ratings_new = fields.Float(
        compute = "_compute_four_votes_ratings_new"
    )
    four_stars_ratings = fields.Float()
    four_stars_reviews = fields.Float()
    four_stars_reviews_new = fields.Float(
        compute = "_compute_four_stars_reviews_new"
    )
    total_four_stars_reviews = fields.Float(
        compute = "_compute_total_four_stars_reviews"
    )
    four_stars_value = fields.Float(
        compute = "_compute_four_stars_value"
    )

    five_votes_ratings_new = fields.Float(
        compute = "_compute_five_votes_ratings_new"
    )
    five_stars_ratings = fields.Float()
    five_stars_reviews = fields.Float()
    five_stars_reviews_new = fields.Float(
        compute = "_compute_five_stars_reviews_new"
    )
    total_five_stars_reviews = fields.Float(
        compute = "_compute_total_five_stars_reviews"
    )
    five_stars_value = fields.Float(
        compute = "_compute_five_stars_value"
    )

    general_reviews_statistics = fields.Float(
        compute = "_compute_general_reviews_statistics"
    )

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
        lines = []

        for line in self:
            line.one_vote_ratings_new = 0
            lines.append(line)

        for index in range(len(lines)):
            if index > 0:
                lines[index].one_vote_ratings_new = \
                    lines[index].one_star_ratings \
                    - lines[index - 1].one_star_ratings

    @api.depends("two_stars_ratings")
    def _compute_two_votes_ratings_new(self):
        lines = []

        for line in self:
            line.two_votes_ratings_new = 0
            lines.append(line)

        for index in range(len(lines)):
            if index > 0:
                lines[index].two_votes_ratings_new = \
                    lines[index].two_stars_ratings \
                    - lines[index - 1].two_stars_ratings

    @api.depends("three_stars_ratings")
    def _compute_three_votes_ratings_new(self):
        lines = []

        for line in self:
            line.three_votes_ratings_new = 0
            lines.append(line)

        for index in range(len(lines)):
            if index > 0:
                lines[index].three_votes_ratings_new = \
                    lines[index].three_stars_ratings \
                    - lines[index - 1].three_stars_ratings

    @api.depends("four_stars_ratings")
    def _compute_four_votes_ratings_new(self):
        lines = []

        for line in self:
            line.four_votes_ratings_new = 0
            lines.append(line)

        for index in range(len(lines)):
            if index > 0:
                lines[index].four_votes_ratings_new = \
                    lines[index].four_stars_ratings \
                    - lines[index - 1].four_stars_ratings

    @api.depends("five_stars_ratings")
    def _compute_five_votes_ratings_new(self):
        lines = []

        for line in self:
            line.five_votes_ratings_new = 0
            lines.append(line)

        for index in range(len(lines)):
            if index > 0:
                lines[index].five_votes_ratings_new = \
                    lines[index].five_stars_ratings \
                    - lines[index - 1].five_stars_ratings

    @api.depends("one_star_reviews")
    def _compute_one_star_reviews_new(self):
        lines = []

        for line in self:
            line.one_star_reviews_new = 0
            lines.append(line)

        for index in range(len(lines)):
            if index > 0:
                lines[index].one_star_reviews_new = \
                    lines[index].one_star_reviews \
                    - lines[index - 1].one_star_reviews

    @api.depends("two_stars_reviews")
    def _compute_two_stars_reviews_new(self):
        lines = []

        for line in self:
            line.two_stars_reviews_new = 0
            lines.append(line)

        for index in range(len(lines)):
            if index > 0:
                lines[index].two_stars_reviews_new = \
                    lines[index].two_stars_reviews \
                    - lines[index - 1].two_stars_reviews

    @api.depends("three_stars_reviews")
    def _compute_three_stars_reviews_new(self):
        lines = []

        for line in self:
            line.three_stars_reviews_new = 0
            lines.append(line)

        for index in range(len(lines)):
            if index > 0:
                lines[index].three_stars_reviews_new = \
                    lines[index].three_stars_reviews \
                    - lines[index - 1].three_stars_reviews

    @api.depends("four_stars_reviews")
    def _compute_four_stars_reviews_new(self):
        lines = []

        for line in self:
            line.four_stars_reviews_new = 0
            lines.append(line)

        for index in range(len(lines)):
            if index > 0:
                lines[index].four_stars_reviews_new = \
                    lines[index].four_stars_reviews \
                    - lines[index - 1].four_stars_reviews

    @api.depends("five_stars_reviews")
    def _compute_five_stars_reviews_new(self):
        lines = []

        for line in self:
            line.five_stars_reviews_new = 0
            lines.append(line)

        for index in range(len(lines)):
            if index > 0:
                lines[index].five_stars_reviews_new = \
                    lines[index].five_stars_reviews \
                    - lines[index - 1].five_stars_reviews

    @api.depends("one_vote_ratings_new", "one_star_reviews_new")
    def _compute_total_one_star_reviews(self):
        for line in self:
            line.total_one_star_reviews = line.one_vote_ratings_new + line.one_star_reviews_new

    @api.depends("two_votes_ratings_new", "two_stars_reviews_new")
    def _compute_total_two_stars_reviews(self):
        for line in self:
            line.total_two_stars_reviews = line.two_votes_ratings_new + line.two_stars_reviews_new

    @api.depends("three_votes_ratings_new", "three_stars_reviews_new")
    def _compute_total_three_stars_reviews(self):
        for line in self:
            line.total_three_stars_reviews = line.three_votes_ratings_new + line.three_stars_reviews_new

    @api.depends("four_votes_ratings_new", "four_stars_reviews_new")
    def _compute_total_four_stars_reviews(self):
        for line in self:
            line.total_four_stars_reviews = line.four_votes_ratings_new + line.four_stars_reviews_new

    @api.depends("five_votes_ratings_new", "five_stars_reviews_new")
    def _compute_total_five_stars_reviews(self):
        for line in self:
            line.total_five_stars_reviews = line.five_votes_ratings_new + line.five_stars_reviews_new

    @api.depends("total_one_star_reviews")
    def _compute_one_star_value(self):
        for line in self:
            line.one_star_value = 1 * line.total_one_star_reviews

    @api.depends("total_two_stars_reviews")
    def _compute_two_stars_value(self):
        for line in self:
            line.two_stars_value = 1 * line.total_two_stars_reviews

    @api.depends("total_three_stars_reviews")
    def _compute_three_stars_value(self):
        for line in self:
            line.three_stars_value = 1 * line.total_three_stars_reviews

    @api.depends("total_four_stars_reviews")
    def _compute_four_stars_value(self):
        for line in self:
            line.four_stars_value = 1 * line.total_four_stars_reviews

    @api.depends("total_five_stars_reviews")
    def _compute_five_stars_value(self):
        for line in self:
            line.five_stars_value = 1 * line.total_five_stars_reviews

    @api.depends("one_star_value", "two_stars_value", "three_stars_value",
                 "four_stars_value", "five_stars_value",
                 "total_one_star_reviews", "total_two_stars_reviews",
                 "total_three_stars_reviews", "total_four_stars_reviews",
                 "total_five_stars_reviews")
    def _compute_general_reviews_statistics(self):
        for line in self:
            line.general_reviews_statistics = \
                (line.one_star_value + line.two_stars_value
                 + line.three_stars_value + line.four_stars_value
                 + line.five_stars_value) / \
                (line.total_one_star_reviews + line.total_two_stars_reviews
                 + line.total_three_stars_reviews + line.total_four_stars_reviews
                 + line.total_five_stars_reviews)
