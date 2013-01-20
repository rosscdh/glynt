$(function () {
/**
* Various Global Javascript Constructs for the Glynt Project
* author: Ross Crawford-d'Heureuse
*/
    GlyntMessage = function (options) {
        this.options = $.extend({}, options);
        this.timer = null;
        this.$container = $('div#messages');
        this.$element = $('div#messages ul');
        this.init();
        this.listen();
    }
    GlyntMessage.prototype = {
        init: function (){
            self = this;
            self.$container.css('position', 'absolute');
        }
        ,listen: function() {
            // closer element
            this.$container.find('div.close').on('click', function(event){
                self.hide();
            });
            this.$container.on('hover', function(event){
                window.clearTimeout(self.timer);
            });
            this.$element.on('hover', function(event){
                window.clearTimeout(self.timer);
            });
        }
        ,place: function(options) {
            //if (!options) {
                options = $('div#document').offset();
                options.top = $(window).scrollTop() + 100;
                options.left = $('div#document').width()/1.2 - self.$container.width()/2;
            //}
            self.$container.width($('div#document').width()/1.2)
            self.$container.offset(options);
            
            return self;
        }
        ,populate_message: function(msg, css_class, textStatus) {
            self.$element.find('li').remove();
            self.$element.append($('<li/>', {class: css_class, html: msg}));
            self.$element.show();
            self.$container.show();
        }
        ,show: function(msg, textStatus) {
            self.populate_message(msg, 'msg', textStatus);
            if (self.timer) {
                window.clearTimeout(self.timer);
            }
            self.timer = window.setTimeout(self.hide, 6000);
        }
        ,show_error: function(msg, textStatus) {
            self.populate_message(msg, 'error', textStatus);
            // no timeout fadeaway for errors; user must click away
        }
        ,hide: function(){
            //self.$container.offset({top: 0, left: 0});
            self.$container.hide();
            self.$element.show();
            self.$referer = null; // always set it to nsull on hide
            return self;
        }
    };

});

$(document).ready(function(){
    $('body').tooltip({
        selector: '[rel=tooltip]',
        placement: 'right',
        animation: true,
        delay: { show: 50, hide: 5 }
    });
    $('body').popover({
        selector: '[rel=popover]',
        trigger: 'hover',
    });
});