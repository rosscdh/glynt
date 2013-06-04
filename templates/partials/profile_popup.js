{% load templatetag_handlebars %}
{% tplhandlebars "tpl-profile-mini" %}<div class="container">
    <div class="row">
        <div class="alert {{alert_type}}">
            <button type="button" class="close" data-dismiss="alert">&times;</button>
            {{# unless messages }}<div class="close span1 pull-right">X</div>{{/unless}}
            {{#each messages}}
                <span class="{{ tags }}">{{ message }}</span><br />
            {{/each}}
        </div>
    </div>
</div>{% endtplhandlebars %}

<script type="text/javascript">

var GlyntProfilePopup = {
    extra_context: {}
    ,profiles: []
    ,template: Handlebars.compile($('script#tpl-profile-mini').html())
    ,add_message: function add_profile(profile) {
        var self = this;
        extra_context = self.extra_context || {}
        context = $.extend({
            'profile': profile
        }, extra_context);

        return this.profiles[profile.id] = this.template(context);
    }
    ,render: function render(extra_context) {

    }
    ,show: function show(){
        var self = this;
        output = self.render();
    }
    ,hide: function hide(){
        
    }
}
</script>