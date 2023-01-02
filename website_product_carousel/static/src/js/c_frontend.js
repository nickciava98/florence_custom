odoo.define('website_product_carousel.carousel_frontend', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var publicWidget = require('web.public.widget');
    publicWidget.registry.js_get_objects = publicWidget.Widget.extend({
        disabledInEditableMode: !1,
        selector: ".js_get_objects", start: function () {
            this.redraw()
        }, destroy: function () {
            this.clean(), this._super.apply(this, arguments)
        }, redraw: function (t) {
            this.clean(t), this.build(t)
        }, clean: function (t) {
            this.$target.empty()
        }, carousel_view: function (t) {
            $(".owl-carousel").owlCarousel({
                loop: !0,
                margin: 10,
                responsiveClass: !0,
                dots: !1,
                nav: !0,
                pagination: !1,
                autoplay: !0,
                responsive: {
                    480: {items: 1},
                    768: {items: this.$target.data("objects_in_slide_tablet")},
                    979: {items: this.$target.data("objects_in_slide_tablet")},
                    479: {items: this.$target.data("objects_in_slide_mobile")},
                    320: {items: this.$target.data("objects_in_slide_mobile")},
                    1199: {items: this.$target.data("objects_in_slide")}
                }
            })
        }, build: function (t) {
            var e = this, i = e.$target.data("objects_limit"), a = e.$target.data("filter_by_filter_id"),
                s = e.$target.data("objects_in_slide"), o = e.$target.data("product_view"),
                n = e.$target.data("split_product_object");
            e.$target.attr("contentEditable", !1), s || (s = 3), i || (i = 6), n || (n = 1), ajax.jsonRpc("/render_product_carousel_slider/product_slider/", "call", {
                product_view: o,
                filter_id: a,
                objects_in_slide: s,
                limit: i,
                product_row: n
            }).then(function (t) {
                $(t).appendTo(e.$target), e.carousel_view(t)
            }).then(function () {
                e.loading(t)
            })
        }, loading: function (t) {
        }
    });
});
(function ($) {
    $.fn.countdown = function (options, callback) {
        var settings = $.extend({
            date: null,
            offset: null,
            day: 'Day',
            days: 'Days',
            hour: 'Hour',
            hours: 'Hours',
            minute: 'Minute',
            minutes: 'Minutes',
            second: 'Second',
            seconds: 'Seconds'
        }, options);

        // Throw error if date is not set
        if (!settings.date) {
            $.error('Date is not defined.');
        }

        // Throw error if date is set incorectly
        if (!Date.parse(settings.date)) {
            $.error('Incorrect date format, it should look like this, 12/24/2012 12:00:00.');
        }

        // Save container
        var container = this;
        /**
         * Change client's local date to match offset timezone
         * @return {Object} Fixed Date object.
         */
        var currentDate = function () {
            // get client's current date
            var date = new Date();

            // turn date to utc
            var utc = date.getTime() + (date.getTimezoneOffset() * 60000);

            // set new Date object
            var new_date = new Date(utc + (3600000 * settings.offset));

            return new_date;
        };

        /**
         * Main countdown function that calculates everything
         */
        function countdown() {
            var target_date = new Date(settings.date), // set target date
                current_date = currentDate(); // get fixed current date

            // difference of dates
            var difference = target_date - current_date;

            // if difference is negative than it's pass the target date
            if (difference < 0) {
                // stop timer
                clearInterval(interval);

                if (callback && typeof callback === 'function') callback();

                return;
            }

            // basic math variables
            var _second = 1000,
                _minute = _second * 60,
                _hour = _minute * 60,
                _day = _hour * 24;

            // calculate dates
            var days = Math.floor(difference / _day),
                hours = Math.floor((difference % _day) / _hour),
                minutes = Math.floor((difference % _hour) / _minute),
                seconds = Math.floor((difference % _minute) / _second);

            // based on the date change the refrence wording
            var text_days = (days === 1) ? settings.day : settings.days,
                text_hours = (hours === 1) ? settings.hour : settings.hours,
                text_minutes = (minutes === 1) ? settings.minute : settings.minutes,
                text_seconds = (seconds === 1) ? settings.second : settings.seconds;

            // fix dates so that it will show two digets
            days = (String(days).length >= 2) ? days : '0' + days;
            hours = (String(hours).length >= 2) ? hours : '0' + hours;
            minutes = (String(minutes).length >= 2) ? minutes : '0' + minutes;
            seconds = (String(seconds).length >= 2) ? seconds : '0' + seconds;

            // set to DOM
            container.find('.days').html(days);
            container.find('.hours').text(hours);
            container.find('.minutes').text(minutes);
            container.find('.seconds').text(seconds);

            container.find('.days_text').text(text_days);
            container.find('.hours_text').text(text_hours);
            container.find('.minutes_text').text(text_minutes);
            container.find('.seconds_text').text(text_seconds);
        }

        // start
        var interval = setInterval(countdown, 1000);
    };
})(jQuery);