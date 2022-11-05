from odoo import models, fields, api

class AmazonStatisticsLine(models.Model):
    _name = "amazon.statistics.line"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Amazon Statistics Line"

    name = fields.Many2one(
        "amazon.statistics",
        ondelete = "cascade"
    )
    name_test = fields.Many2one(
        "amazon.statistics",
        ondelete = "cascade"
    )
    parent = fields.Char()
    product = fields.Many2one(
        "product.template"
    )
    date = fields.Date()
    updates = fields.Char()

    one_vote_ratings_new = fields.Float(
        compute = "_compute_one_vote_ratings_new",
        store = True,
        digits = (12, 4)
    )
    one_star_ratings = fields.Float(
        digits = (12, 4)
    )
    one_star_reviews = fields.Float(
        digits = (12, 4)
    )
    one_star_reviews_new = fields.Float(
        compute = "_compute_one_star_reviews_new",
        store = True,
        digits = (12, 4)
    )
    total_one_star_reviews = fields.Float(
        compute = "_compute_total_one_star_reviews",
        store = True,
        digits = (12, 4)
    )
    one_star_value = fields.Float(
        compute = "_compute_one_star_value",
        store = True,
        group_operator = "avg",
        digits = (12, 4)
    )

    two_votes_ratings_new = fields.Float(
        compute = "_compute_two_votes_ratings_new",
        store = True,
        digits = (12, 4)
    )
    two_stars_ratings = fields.Float(
        digits = (12, 4)
    )
    two_stars_reviews = fields.Float(
        digits = (12, 4)
    )
    two_stars_reviews_new = fields.Float(
        compute = "_compute_two_stars_reviews_new",
        store = True,
        digits = (12, 4)
    )
    total_two_stars_reviews = fields.Float(
        compute = "_compute_total_two_stars_reviews",
        store = True,
        digits = (12, 4)
    )
    two_stars_value = fields.Float(
        compute = "_compute_two_stars_value",
        store = True,
        group_operator = "avg",
        digits = (12, 4)
    )

    three_votes_ratings_new = fields.Float(
        compute = "_compute_three_votes_ratings_new",
        store = True,
        digits = (12, 4)
    )
    three_stars_ratings = fields.Float(
        digits = (12, 4)
    )
    three_stars_reviews = fields.Float(
        digits = (12, 4)
    )
    three_stars_reviews_new = fields.Float(
        compute = "_compute_three_stars_reviews_new",
        store = True,
        digits = (12, 4)
    )
    total_three_stars_reviews = fields.Float(
        compute = "_compute_total_three_stars_reviews",
        store = True,
        digits = (12, 4)
    )
    three_stars_value = fields.Float(
        compute = "_compute_three_stars_value",
        store = True,
        group_operator = "avg",
        digits = (12, 4)
    )

    four_votes_ratings_new = fields.Float(
        compute = "_compute_four_votes_ratings_new",
        store = True,
        digits = (12, 4)
    )
    four_stars_ratings = fields.Float(
        digits = (12, 4)
    )
    four_stars_reviews = fields.Float(
        digits = (12, 4)
    )
    four_stars_reviews_new = fields.Float(
        compute = "_compute_four_stars_reviews_new",
        store = True,
        digits = (12, 4)
    )
    total_four_stars_reviews = fields.Float(
        compute = "_compute_total_four_stars_reviews",
        store = True,
        digits = (12, 4)
    )
    four_stars_value = fields.Float(
        compute = "_compute_four_stars_value",
        store = True,
        group_operator = "avg",
        digits = (12, 4)
    )

    five_votes_ratings_new = fields.Float(
        compute = "_compute_five_votes_ratings_new",
        store = True,
        digits = (12, 4)
    )
    five_stars_ratings = fields.Float(
        digits = (12, 4)
    )
    five_stars_reviews = fields.Float(
        digits = (12, 4)
    )
    five_stars_reviews_new = fields.Float(
        compute = "_compute_five_stars_reviews_new",
        store = True,
        digits = (12, 4)
    )
    total_five_stars_reviews = fields.Float(
        compute = "_compute_total_five_stars_reviews",
        store = True,
        digits = (12, 4)
    )
    five_stars_value = fields.Float(
        compute = "_compute_five_stars_value",
        store = True,
        group_operator = "avg",
        digits = (12, 4)
    )

    general_reviews_statistics = fields.Float(
        compute = "_compute_general_reviews_statistics",
        store = True,
        group_operator = "avg",
        digits = (12, 4)
    )

    daily_total_reviews = fields.Float(
        compute = "_compute_daily_total_reviews",
        store = True,
        digits = (12, 4)
    )

    main_stat = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )

    five_reviews_perc = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    four_reviews_perc = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    three_reviews_perc = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    two_reviews_perc = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    one_reviews_perc = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    
    da_five_perc = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    
    freshness = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    absorbency = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    quality_price = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    comfort = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    hydration = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    solar_protection = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    softness = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    easy_to_use = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    light = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    style = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    perfume = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )

    ncx_rate_perc = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    total_orders = fields.Float(
        digits = (12, 4)
    )
    returns = fields.Float(
        digits = (12, 4)
    )

    performance_quality_inadequate = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    defective_item_perc = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    damage_item_perc = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    inaccurate_website_description_perc = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    wrong_item_was_sent_perc = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )
    missing_parts_accessories_perc = fields.Float(
        group_operator = "avg",
        digits = (12, 4)
    )

    freshdesk_buyer_messages = fields.Char()
    amazon_buyer_messages = fields.Char()

    average = fields.Float(
        related = "name.average",
        store = True,
        digits = (12, 4)
    )
    average_test = fields.Float(
        related = "name.average_test",
        store = True,
        digits = (12, 4)
    )

    @api.depends("total_one_star_reviews", "total_two_stars_reviews",
                 "total_three_stars_reviews", "total_four_stars_reviews",
                 "total_five_stars_reviews")
    def _compute_daily_total_reviews(self):
        for line in self:
            line.daily_total_reviews = line.total_one_star_reviews + \
                                       line.total_two_stars_reviews + \
                                       line.total_three_stars_reviews + \
                                       line.total_four_stars_reviews + \
                                       line.total_five_stars_reviews

    @api.depends("one_star_ratings")
    def _compute_one_vote_ratings_new(self):
        lines = []

        for line in self:
            line.one_vote_ratings_new = 0
            lines.append(line)

        for index in range(len(lines)):
            if index > 0:
                if lines[index].one_star_ratings > lines[index - 1].one_star_ratings:
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
                if lines[index].two_stars_ratings > lines[index - 1].two_stars_ratings:
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
                if lines[index].three_stars_ratings > lines[index - 1].three_stars_ratings:
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
                if lines[index].four_stars_ratings > lines[index - 1].four_stars_ratings:
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
                if lines[index].five_stars_ratings > lines[index - 1].five_stars_ratings:
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
                if lines[index].one_star_reviews > lines[index - 1].one_star_reviews:
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
                if lines[index].two_stars_reviews > lines[index - 1].two_stars_reviews:
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
                if lines[index].three_stars_reviews > lines[index - 1].three_stars_reviews:
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
                if lines[index].four_stars_reviews > lines[index - 1].four_stars_reviews:
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
                if lines[index].five_stars_reviews > lines[index - 1].five_stars_reviews:
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
            line.two_stars_value = 2 * line.total_two_stars_reviews

    @api.depends("total_three_stars_reviews")
    def _compute_three_stars_value(self):
        for line in self:
            line.three_stars_value = 3 * line.total_three_stars_reviews

    @api.depends("total_four_stars_reviews")
    def _compute_four_stars_value(self):
        for line in self:
            line.four_stars_value = 4 * line.total_four_stars_reviews

    @api.depends("total_five_stars_reviews")
    def _compute_five_stars_value(self):
        for line in self:
            line.five_stars_value = 5 * line.total_five_stars_reviews

    @api.depends("one_star_value", "two_stars_value", "three_stars_value",
                 "four_stars_value", "five_stars_value",
                 "total_one_star_reviews", "total_two_stars_reviews",
                 "total_three_stars_reviews", "total_four_stars_reviews",
                 "total_five_stars_reviews")
    def _compute_general_reviews_statistics(self):
        previous_line = None

        for line in self:
            line.general_reviews_statistics = 0

            if line.total_one_star_reviews + line.total_two_stars_reviews \
                 + line.total_three_stars_reviews + line.total_four_stars_reviews \
                 + line.total_five_stars_reviews != 0:
                line.general_reviews_statistics = \
                    (line.one_star_value + line.two_stars_value
                     + line.three_stars_value + line.four_stars_value
                     + line.five_stars_value) / \
                    (line.total_one_star_reviews + line.total_two_stars_reviews
                     + line.total_three_stars_reviews + line.total_four_stars_reviews
                     + line.total_five_stars_reviews)

            if line.general_reviews_statistics == 0:
                if previous_line is not None:
                    line.general_reviews_statistics = previous_line.general_reviews_statistics

            previous_line = line

    # @api.depends("general_reviews_statistics")
    # def _compute_main_stat(self):
    #     previous_line = None
    #
    #     for line in self:
    #         line.main_stat = line.general_reviews_statistics
    #
    #         if previous_line is not None:
    #             line.main_stat = previous_line.general_reviews_statistics
    #
    #         previous_line = line

    #     lines = []
    #     general_reviews_statistics_list = []
    #
    #     for line in self:
    #         line.main_stat = 0
    #
    #         if line.general_reviews_statistics != 0:
    #             lines.append(line)
    #             general_reviews_statistics_list.append(
    #                 line.general_reviews_statistics
    #             )
    #
    #     for index in range(len(lines)):
    #         if index > 0:
    #             if len(general_reviews_statistics_list[:index]) != 1:
    #                 lines[index].main_stat = \
    #                     sum(general_reviews_statistics_list[:index]) / \
    #                     (len(general_reviews_statistics_list[:index]) - 1)
    #             else:
    #                 lines[index].main_stat = lines[index].general_reviews_statistics
