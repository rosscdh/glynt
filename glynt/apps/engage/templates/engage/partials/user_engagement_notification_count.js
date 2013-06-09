{% load templatetag_handlebars jsonify %}

{% tplhandlebars "tpl-unread-count" %}
<span class="offset10 unread-messages">{{ unread }}</span>
{% endtplhandlebars %}

<script id="user_engagement_notification_count" type="application/json">
{{ unread|jsonify }}
</script>
<script>
$(document).ready(function(){
    var user_engagement_notification_count = $.parseJSON($('script#user_engagement_notification_count').html());
    var unread_template = Handlebars.compile($('script#tpl-unread-count').html())

    $.each($('ul#engagement-list li'),function(i,item){
        var elem = $(item);
        var pk = elem.attr('data-pk');
        var unread = user_engagement_notification_count[pk];
        if (unread && unread >= 1) {
            html = unread_template({'unread': unread});
            elem.append(html)
        }
    })
});
</script>