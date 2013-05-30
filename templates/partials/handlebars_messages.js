{% load templatetag_handlebars %}
{% tplhandlebars "tpl-messages" %}<div class="container">
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


var GlyntJsMessages = {
    title: null
    ,messages: []
    ,output_target: $('{{output_target}}')
    ,template: Handlebars.compile($('script#tpl-messages').html())
    ,add_message: function add_message(msg, tags) {
        tags = tags || null
        this.messages.push({'message': msg, 'tags': tags});
    }
    ,render: function render(extra_context) {
        var self = this;
        extra_context = extra_context || {}
        context = $.extend({
            'messages': self.messages
        }, extra_context);
        console.log(context)
        return this.template(context)
    }
    ,show: function show(){
        var self = this;
        output = self.render();
        {% if target_in_before_after == 'in' %}
        self.output_target.html(output);
        {% endif %}
        {% if target_in_before_after == 'before' %}
        self.output_target.before(output);
        {% endif %}
        {% if target_in_before_after == 'after' %}
        self.output_target.after(output);
        {% endif %}
    }
    ,hide: function hide(){
        
    }
}
</script>