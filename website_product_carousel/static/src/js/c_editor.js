odoo.define('website_product_carousel.carousel_editor', function (require) {
    "use strict";

    var rpc = require('web.rpc');
    var options = require('web_editor.snippets.options');
    var core = require('web.core');
    var _t = core._t;
    options.registry.js_get_objects_in_slide = options.Class.extend({
        _setActive: function () {
            this._super.apply(this, arguments);
            var t = this.$target.data("objects_in_slide") || 3;
            this.$el.find("[data-objects_in_slide]").removeClass("active"), this.$el.find("[data-objects_in_slide=" + t + "]").addClass("active")
        }, start: function () {
            var t = this;
            setTimeout(function () {
                var e = $(t.el);
                if (t.$target.attr("data-objects_in_slide")) {
                    var i = t.$target.attr("data-objects_in_slide");
                    $(t.$el).find('we-toggler').text(i)
                    e.find('we-button[data-objects_in_slide="' + i + '"]').addClass("active")
                } else e.find('we-button[data-objects_in_slide="3"]').addClass("active")
            }, 100)
        }, objects_in_slide: function (t, e, i) {
            var self = this;
            0 == t && (e = parseInt(e), this.$target.attr("data-objects_in_slide", e).data("objects_in_slide", e), setTimeout(function () {
                $(self.$el).find('we-toggler').text(e)
                $(self.el).find('.active').removeClass("active"), $(self.el).find('we-button[data-objects_in_slide="' + e + '"]').addClass("active")
            }, 100)), this.trigger_up("animation_start_demand", {editableMode: !0, $target: this.$target})
        }
    }), options.registry.js_get_objects_in_slide_tablet = options.Class.extend({
        _setActive: function () {
            this._super.apply(this, arguments);
            var t = this.$target.data("objects_in_slide_tablet") || 3;
            this.$el.find("[data-objects_in_slide_tablet]").removeClass("active"), this.$el.find("[data-objects_in_slide_tablet=" + t + "]").addClass("active")
        }, start: function () {
            var t = this;
            setTimeout(function () {
                var e = $(t.$el);
                if (t.$target.attr("data-objects_in_slide_tablet")) {
                    var i = t.$target.attr("data-objects_in_slide_tablet");
                    $(t.$el).find('we-toggler').text(i)
                    e.find('we-button[data-objects_in_slide_tablet="' + i + '"]').addClass("active")
                } else e.find('we-button[data-objects_in_slide_tablet="3"]').addClass("active")
            }, 100)
        }, objects_in_slide_tablet: function (t, e, i) {
            var self = this;
            0 == t && (e = parseInt(e), this.$target.attr("data-objects_in_slide_tablet", e).data("objects_in_slide_tablet", e), setTimeout(function () {
                $(self.$el).find('we-toggler').text(e)
                $(self.el).find('.active').removeClass("active"), $(self.el).find('we-button[data-objects_in_slide_tablet="' + e + '"]').addClass("active")
            }, 100)), this.trigger_up("animation_start_demand", {editableMode: !0, $target: this.$target})
        }
    }), options.registry.js_get_objects_in_slide_mobile = options.Class.extend({
        _setActive: function () {
            this._super.apply(this, arguments);
            var t = this.$target.data("objects_in_slide_mobile") || 3;
            this.$el.find("[data-objects_in_slide_mobile]").removeClass("active"), this.$el.find("[data-objects_in_slide_mobile=" + t + "]").addClass("active")
        }, start: function () {
            var t = this;
            setTimeout(function () {
                var e = $(t.$el);
                if (t.$target.attr("data-objects_in_slide_mobile")) {
                    var i = t.$target.attr("data-objects_in_slide_mobile");
                    $(t.$el).find('we-toggler').text(i)
                    e.find('we-button[data-objects_in_slide_mobile="' + i + '"]').addClass("active")
                } else e.find('we-button[data-objects_in_slide_mobile="3"]').addClass("active")
            }, 100)
        }, objects_in_slide_mobile: function (t, e, i) {
            var self = this;
            0 == t && (e = parseInt(e), this.$target.attr("data-objects_in_slide_mobile", e).data("objects_in_slide_mobile", e), setTimeout(function () {
                $(self.$el).find('we-toggler').text(e)
                $(self.el).find('.active').removeClass("active"), $(self.el).find('we-button[data-objects_in_slide_mobile="' + e + '"]').addClass("active")
            }, 100)), this.trigger_up("animation_start_demand", {editableMode: !0, $target: this.$target})
        }
    }), options.registry.js_get_objects_limit = options.Class.extend({
        _setActive: function () {
            this._super.apply(this, arguments);
            var t = this.$target.data("objects_limit") || 3;
            this.$el.find("[data-objects_limit]").removeClass("active"), this.$el.find("[data-objects_limit=" + t + "]").addClass("active")
        }, start: function () {
            var t = this;
            setTimeout(function () {
                var e = $(t.$el);
                if (t.$target.attr("data-objects_limit")) {
                    var i = t.$target.attr("data-objects_limit");
                    $(t.$el).find('we-toggler').text(i)
                    e.find('we-button[data-objects_limit="' + i + '"]').addClass("active")
                } else e.find('we-button[data-objects_limit="15"]').addClass("active")
            }, 100)
        }, objects_limit: function (t, e, i) {
            var self = this;
            0 == t && (e = parseInt(e), this.$target.attr("data-objects_limit", e).data("objects_limit", e), setTimeout(function () {
                $(self.$el).find('we-toggler').text(e)
                $(self.el).find('.active').removeClass("active"), $(self.el).find('we-button[data-objects_limit="' + e + '"]').addClass("active")
            }, 100)), this.trigger_up("animation_start_demand", {editableMode: !0, $target: this.$target})
        }
    }), options.registry.js_get_objects_selectFilter = options.Class.extend({
        start: function () {
            var t = this;
            setTimeout(function () {
                var e = $(t.el);
                if (t.$target.attr("data-filter_by_filter_id")) {
                    var i = t.$target.attr("data-filter_by_filter_id");
                    $(t.$el).find('we-toggler').text(t.$el.find('we-button[data-filter_by_filter_id="' + i + '"]').text())
                    e.find('we-button[data-filter_by_filter_id="' + i + '"]').addClass("active")
                } else e.find('we-button[data-filter_by_filter_id=""]').addClass("active")
            }, 100)
        }, filter_by_filter_id: function (t, e, i) {
            var self = this;
            $(self.$el).find('we-toggler').text(self.$el.find('we-button[data-filter_by_filter_id="' + e + '"]').text())
            0 == t && ($(self.el).find('.active').removeClass("active"), $(self.el).find('we-button[data-filter_by_filter_id="' + e + '"]').addClass("active"), e = parseInt(e), this.$target.attr("data-filter_by_filter_id", e).data("filter_by_filter_id", e)), this.trigger_up("animation_start_demand", {
                editableMode: !0,
                $target: this.$target
            })
        }, _setActive: function () {
            this.$el.find("we-button[data-filter_by_filter_id]").removeClass("active").filter("we-button[data-filter_by_filter_id=" + this.$target.attr("data-filter_by_filter_id") + "]").addClass("active")
        }
    }), options.registry.js_get_objects = options.Class.extend({
        onBuilt: function () {
            this._super.apply(this, arguments)
        }, cleanForSave: function () {
            this._super.apply(this, arguments), this.$target.empty()
        }
    }), options.registry.carousel_objects_in_row = options.Class.extend({
        _setActive: function () {
            this._super.apply(this, arguments);
            var t = this.$target.data("split_product_object") || 3;
            this.$el.find("[data-split_product_object]").removeClass("active"), this.$el.find("[data-split_product_object=" + t + "]").addClass("active")
        }, start: function () {
            var t = this;
            setTimeout(function () {
                var i = $(t.$el);
                if (t.$target.attr("data-split_product_object")) {
                    var e = t.$target.attr("data-split_product_object");
                    $(t.$el).find('we-toggler').text(e)
                    i.find('we-button[data-split_product_object="' + e + '"]').addClass("active")
                } else i.find('we-button[data-split_product_object="1"]').addClass("active")
            }, 100)
        }, split_product_object: function (t, e, i) {
            var self = this;
            0 == t && (e = parseInt(e), this.$target.attr("data-split_product_object", e).data("split_product_object", e), setTimeout(function () {
                $(self.$el).find('we-toggler').text(e)
                $(self.el).find('.active').removeClass("active"), $(self.el).find('we-button[data-split_product_object="' + e + '"]').addClass("active")
            }, 100)), this.trigger_up("animation_start_demand", {editableMode: !0, $target: this.$target})
        }
    });
});