from odoo import models, fields, api, exceptions, _
from datetime import datetime

class AmazonStatistics(models.Model):
    _name = "amazon.statistics"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Amazon Statistics"

    name = fields.Selection(
        [("IT", "Amazon IT"),
         ("FR", "Amazon FR"),
         ("DE", "Amazon DE"),
         ("ES", "Amazon ES"),
         ("UK", "Amazon UK")],
        required = True,
        string = "Marketplace",
        tracking = True
    )
    product = fields.Many2one(
        "product.template",
        required = True,
        tracking = True
    )
    statistics_lines = fields.One2many(
        "amazon.statistics.line",
        "name"
    )
    statistics_lines_test = fields.One2many(
        "amazon.statistics.line",
        "name_test"
    )
    start_date = fields.Date(
        compute = "_compute_start_date"
    )
    average = fields.Float(
        compute = "_compute_average",
        store = True,
        group_operator = "avg"
    )
    avg_stars = fields.Selection(
        [("0", "Zero Stars"),
         ("1", "One Star"),
         ("2", "Two Stars"),
         ("3", "Three Stars"),
         ("4", "Four Stars"),
         ("5", "Five Stars")],
        compute = "_compute_avg_stars",
        store = True
    )
    average_test = fields.Float(
        compute = "_compute_average_test",
        store = True
    )
    avg_stars_test = fields.Selection(
        [("0", "Zero Stars"),
         ("1", "One Star"),
         ("2", "Two Stars"),
         ("3", "Three Stars"),
         ("4", "Four Stars"),
         ("5", "Five Stars")],
        compute = "_compute_avg_stars_test",
        store = True,
        group_operator = "avg"
    )
    date_from = fields.Date()
    date_to = fields.Date()
    date_from_test = fields.Date()
    date_to_test = fields.Date()
    group_by = fields.Selection(
        [("day", "Daily Statistics"),
         ("week", "Weekly Statistics"),
         ("month", "Monthly Statistics")]
    )
    group_by_test = fields.Selection(
        [("day", "Daily Statistics"),
         ("week", "Weekly Statistics"),
         ("month", "Monthly Statistics")]
    )

    @api.depends("average")
    def _compute_avg_stars(self):
        for line in self:
            line.avg_stars = str(int(line.average))

    @api.depends("average_test")
    def _compute_avg_stars_test(self):
        for line in self:
            line.avg_stars_test = str(int(line.average_test))

    @api.onchange("name")
    def _onchange_name(self):
        for line in self:
            if len(line.statistics_lines) > 0:
                for statistics_line in line.statistics_lines:
                    statistics_line.parent = line.name
            if len(line.statistics_lines_test) > 0:
                for statistics_line_test in line.statistics_lines_test:
                    statistics_line_test.parent = line.name

    @api.onchange("product")
    def _onchange_product(self):
        for line in self:
            if len(line.statistics_lines) > 0:
                for statistics_line in line.statistics_lines:
                    statistics_line.product = line.product
            if len(line.statistics_lines_test) > 0:
                for statistics_line_test in line.statistics_lines_test:
                    statistics_line_test.product = line.product

    @api.depends("statistics_lines", "date_from", "date_to")
    def _compute_average(self):
        for line in self:
            line.average = 0
            statistics_lines = []

            if len(line.statistics_lines) > 0 \
                    and line.date_from and line.date_to:
                for statistics_line in line.statistics_lines:
                    if statistics_line.date \
                        and statistics_line.date >= line.date_from \
                        and statistics_line.date <= line.date_to:
                        statistics_lines.append(statistics_line)

                if len(statistics_lines) > 0:
                    line.average = statistics_lines[-1].main_stat

    @api.depends("statistics_lines_test", "date_from_test", "date_to_test")
    def _compute_average_test(self):
        for line in self:
            line.average_test = 0
            statistics_lines = []

            if len(line.statistics_lines_test) > 0 \
                and line.date_from_test and line.date_to_test:
                for statistics_line in line.statistics_lines_test:
                    if statistics_line.date \
                        and statistics_line.date >= line.date_from_test \
                        and statistics_line.date <= line.date_to_test:
                        statistics_lines.append(statistics_line)

                if len(statistics_lines) > 0:
                    line.average_test = statistics_lines[-1].main_stat

    def _compute_start_date(self):
        for line in self:
            line.start_date = datetime.now()

    def dashboard_view_action(self):
        if self.group_by == "day":
            return {
                'name': 'Statistics Dashboard',
                'view_type': 'dashboard',
                'view_mode': 'dashboard',
                'res_model': 'amazon.statistics.line',
                'type': 'ir.actions.act_window',
                'domain': [
                    '&', '&', '&', '&',
                    ('name_test', '=', False),
                    ('product', '=', self.product.id),
                    ('parent', '=', self.name),
                    ('date', '>=', self.date_from),
                    ('date', '<=', self.date_to)
                ],
                'context': {
                    'graph_measure': 'main_stat',
                    'graph_mode': 'line'
                }
            }

        return {
            'name': 'Statistics Dashboard',
            'view_type': 'dashboard',
            'view_mode': 'dashboard',
            'res_model': 'amazon.statistics.line',
            'type': 'ir.actions.act_window',
            'domain': [
                '&', '&', '&', '&',
                ('name_test', '=', False),
                ('product', '=', self.product.id),
                ('parent', '=', self.name),
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to)
            ],
            'context': {
                'graph_measure': 'main_stat',
                'graph_mode': 'line',
                'graph_groupbys': ['date:' + self.group_by]
            }
        }

    def graph_view_action(self):
        if self.group_by == "day":
            return {
                'name': 'Statistics Analysis',
                'view_type': 'graph',
                'view_mode': 'graph',
                'res_model': 'amazon.statistics.line',
                'type': 'ir.actions.act_window',
                'domain': [
                    '&', '&', '&', '&',
                    ('name_test', '=', False),
                    ('product', '=', self.product.id),
                    ('parent', '=', self.name),
                    ('date', '>=', self.date_from),
                    ('date', '<=', self.date_to)
                ],
                'context': {
                    'graph_measure': 'main_stat',
                    'graph_mode': 'line'
                }
            }

        return {
            'name': 'Statistics Analysis',
            'view_type': 'graph',
            'view_mode': 'graph',
            'res_model': 'amazon.statistics.line',
            'type': 'ir.actions.act_window',
            'domain': [
                '&', '&', '&', '&',
                ('name_test', '=', False),
                ('product', '=', self.product.id),
                ('parent', '=', self.name),
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to)
            ],
            'context': {
                'graph_measure': 'main_stat',
                'graph_mode': 'line',
                'graph_groupbys': ['date:' + self.group_by]
            }
        }

    def graph_test_view_action(self):
        if self.group_by_test == "day":
            return {
                'name': 'Statistics Test Analysis',
                'view_type': 'graph',
                'view_mode': 'graph',
                'res_model': 'amazon.statistics.line',
                'type': 'ir.actions.act_window',
                'domain': [
                    '&', '&', '&', '&',
                    ('name', '=', False),
                    ('product', '=', self.product.id),
                    ('parent', '=', self.name),
                    ('date', '>=', self.date_from_test),
                    ('date', '<=', self.date_to_test)
                ],
                'context': {
                    'graph_measure': 'main_stat',
                    'graph_mode': 'line'
                }
            }

        return {
            'name': 'Statistics Test Analysis',
            'view_type': 'graph',
            'view_mode': 'graph',
            'res_model': 'amazon.statistics.line',
            'type': 'ir.actions.act_window',
            'domain': [
                '&', '&', '&', '&',
                ('name', '=', False),
                ('product', '=', self.product.id),
                ('parent', '=', self.name),
                ('date', '>=', self.date_from_test),
                ('date', '<=', self.date_to_test)
            ],
            'context': {
                'graph_measure': 'main_stat',
                'graph_mode': 'line',
                'graph_groupbys': ['date:' + self.group_by_test]
            }
        }

    def tree_view_action(self):
        if self.group_by == "day":
            return {
                'name': 'Statistics List',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'view_id': False,
                'res_model': 'amazon.statistics.line',
                'type': 'ir.actions.act_window',
                'domain': [
                    '&', '&', '&', '&',
                    ('name_test', '=', False),
                    ('product', '=', self.product.id),
                    ('parent', '=', self.name),
                    ('date', '>=', self.date_from),
                    ('date', '<=', self.date_to)
                ],
                'target': 'current'
            }

        return {
            'name': 'Statistics List',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'amazon.statistics.line',
            'type': 'ir.actions.act_window',
            'context': {
                'group_by': ['date:' + self.group_by]
            },
            'domain': [
                '&', '&', '&', '&',
                ('name_test', '=', False),
                ('product', '=', self.product.id),
                ('parent', '=', self.name),
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to)
            ],
            'target': 'current'
        }

    def tree_test_view_action(self):
        if self.group_by_test == "day":
            return {
                'name': 'Statistics Test List',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'view_id': False,
                'res_model': 'amazon.statistics.line',
                'type': 'ir.actions.act_window',
                'domain': [
                    '&', '&', '&', '&',
                    ('name', '=', False),
                    ('product', '=', self.product.id),
                    ('parent', '=', self.name),
                    ('date', '>=', self.date_from_test),
                    ('date', '<=', self.date_to_test)
                ],
                'target': 'current'
            }

        return {
            'name': 'Statistics Test List',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'amazon.statistics.line',
            'type': 'ir.actions.act_window',
            'context': {
                'group_by': ['date:' + self.group_by_test]
            },
            'domain': [
                '&', '&', '&', '&',
                ('name', '=', False),
                ('product', '=', self.product.id),
                ('parent', '=', self.name),
                ('date', '>=', self.date_from_test),
                ('date', '<=', self.date_to_test)
            ],
            'target': 'current'
        }

    def pivot_view_action(self):
        return {
            'name': 'Statistics Dashboard',
            'view_type': 'pivot',
            'view_mode': 'pivot',
            'res_model': 'amazon.statistics.line',
            'type': 'ir.actions.act_window',
            'domain': [
                '&', '&', '&', '&',
                ('name_test', '=', False),
                ('product', '=', self.product.id),
                ('parent', '=', self.name),
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to)
            ]
        }

    def pivot_test_view_action(self):
        return {
            'name': 'Statistics Dashboard',
            'view_type': 'pivot',
            'view_mode': 'pivot',
            'res_model': 'amazon.statistics.line',
            'type': 'ir.actions.act_window',
            'domain': [
                '&', '&', '&', '&',
                ('name', '=', False),
                ('product', '=', self.product.id),
                ('parent', '=', self.name),
                ('date', '>=', self.date_from_test),
                ('date', '<=', self.date_to_test)
            ]
        }

    def update_values_action(self):
        for line in self:
            line.statistics_lines_test = [(5, 0, 0)]

            if len(line.statistics_lines) > 0:
                for statistics_line in line.statistics_lines:
                    self.write({
                        "statistics_lines_test": [
                            (0, 0, {
                                "name": False,
                                "name_test": statistics_line.name,
                                "parent": statistics_line.parent,
                                "product": statistics_line.product.id,
                                "date": statistics_line.date,
                                "one_vote_ratings_new": statistics_line.one_vote_ratings_new,
                                "one_star_ratings": statistics_line.one_star_ratings,
                                "one_star_reviews": statistics_line.one_star_reviews,
                                "one_star_reviews_new": statistics_line.one_star_reviews_new,
                                "total_one_star_reviews": statistics_line.total_one_star_reviews,
                                "one_star_value": statistics_line.one_star_value,
                                "two_votes_ratings_new": statistics_line.two_votes_ratings_new,
                                "two_stars_ratings": statistics_line.two_stars_ratings,
                                "two_stars_reviews": statistics_line.two_stars_reviews,
                                "two_stars_reviews_new": statistics_line.two_stars_reviews_new,
                                "total_two_stars_reviews": statistics_line.total_two_stars_reviews,
                                "two_stars_value": statistics_line.two_stars_value,
                                "three_votes_ratings_new": statistics_line.three_votes_ratings_new,
                                "three_stars_ratings": statistics_line.three_stars_ratings,
                                "three_stars_reviews": statistics_line.three_stars_reviews,
                                "three_stars_reviews_new": statistics_line.three_stars_reviews_new,
                                "total_three_stars_reviews": statistics_line.total_three_stars_reviews,
                                "three_stars_value": statistics_line.three_stars_value,
                                "four_votes_ratings_new": statistics_line.four_votes_ratings_new,
                                "four_stars_ratings": statistics_line.four_stars_ratings,
                                "four_stars_reviews": statistics_line.four_stars_reviews,
                                "four_stars_reviews_new": statistics_line.four_stars_reviews_new,
                                "total_four_stars_reviews": statistics_line.total_four_stars_reviews,
                                "four_stars_value": statistics_line.four_stars_value,
                                "five_votes_ratings_new": statistics_line.five_votes_ratings_new,
                                "five_stars_ratings": statistics_line.five_stars_ratings,
                                "five_stars_reviews": statistics_line.five_stars_reviews,
                                "five_stars_reviews_new": statistics_line.five_stars_reviews_new,
                                "total_five_stars_reviews": statistics_line.total_five_stars_reviews,
                                "five_stars_value": statistics_line.five_stars_value,
                                "general_reviews_statistics": statistics_line.general_reviews_statistics,
                                "daily_total_reviews": statistics_line.daily_total_reviews,
                                "main_stat": statistics_line.main_stat,
                                "five_reviews_perc": statistics_line.five_reviews_perc,
                                "four_reviews_perc": statistics_line.four_reviews_perc,
                                "three_reviews_perc": statistics_line.three_reviews_perc,
                                "two_reviews_perc": statistics_line.two_reviews_perc,
                                "one_reviews_perc": statistics_line.one_reviews_perc,
                                "da_five_perc": statistics_line.da_five_perc,
                                "freshness": statistics_line.freshness,
                                "absorbency": statistics_line.absorbency,
                                "quality_price": statistics_line.quality_price,
                                "comfort": statistics_line.comfort,
                                "hydration": statistics_line.hydration,
                                "solar_protection": statistics_line.solar_protection,
                                "softness": statistics_line.softness,
                                "easy_to_use": statistics_line.easy_to_use,
                                "light": statistics_line.light,
                                "style": statistics_line.style,
                                "perfume": statistics_line.perfume,
                                "ncx_rate_perc": statistics_line.ncx_rate_perc,
                                "total_orders": statistics_line.total_orders,
                                "returns": statistics_line.returns,
                                "performance_quality_inadequate": statistics_line.performance_quality_inadequate,
                                "defective_item_perc": statistics_line.defective_item_perc,
                                "damage_item_perc": statistics_line.damage_item_perc,
                                "inaccurate_website_description_perc": statistics_line.inaccurate_website_description_perc,
                                "wrong_item_was_sent_perc": statistics_line.wrong_item_was_sent_perc,
                                "missing_parts_accessories_perc": statistics_line.missing_parts_accessories_perc
                            })
                        ]
                    })
