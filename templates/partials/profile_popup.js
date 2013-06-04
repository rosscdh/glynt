{% load templatetag_handlebars %}
{% tplhandlebars "tpl-lawyer-profile-mini" %}<div class="container">
    <div class="row">
        {{ profile.name }}
        {{ profile.phone }}
        {{ profile.position }}
        {{ profile.profile_photo }}
        {{ profile.years_practiced }}
        {{ profile.practice_locations }}
    </div>
</div>{% endtplhandlebars %}

{% tplhandlebars "tpl-startup-profile-mini" %}<div class="container">
    <div class="row">
        {{ profile }}
    </div>
</div>{% endtplhandlebars %}

<script type="text/javascript">

var GlyntProfilePopup = {
    profile_api_url: '/api/v1/user/profile/?username__in={username_list}'
    ,extra_context: {}
    ,profiles: []
    ,username_list: []
    ,templates: {
        'startup': Handlebars.compile($('script#tpl-startup-profile-mini').html())
        ,'lawyer': Handlebars.compile($('script#tpl-lawyer-profile-mini').html())
    }
    ,add_profile: function add_profile(profile) {
        var self = this;
        var profile_html = null;
        var extra_context = self.extra_context || {}

        context = $.extend({
            'profile': profile
        }, extra_context);


        if (profile.is_lawyer) {
            profile_html = self.templates.lawyer(context)
        }else if (profile.is_startup) {
            profile_html = self.templates.startup(context)
        }
        console.log(profile)
        this.profiles[profile.username] = profile_html

        return this.profiles[profile.username];
    }
    ,render: function render(extra_context) {

    }
    ,show: function show() {
        var self = this;
        output = self.render();
    }
    ,hide: function hide() {
        
    }
    ,find_all: function find_all() {
        var self = this;
        // uniquify
        self.username_list.unique()
        // see if we have them already or not
        $.each(self.username_list, function(i,username){
            if (self.profiles[username] !== undefined) {
                // we already have this profile remove it from query
            }
        });

        // get the list of items
        $.each(self.username_list.inGroupsOf(10), function(i, item_set){
            // perform ajax query
            var url = self.profile_api_url.assign({'username_list': item_set.compact()})
            self.users(url)
        })

    }
    ,users: function users(url) {
        var self = this;

        $.ajax({
            type: 'GET',
            url: url,
        })
        .success(function(data, textStatus, jqXHR) {

            if (data.objects && data.objects.length > 0) {

                $.each(data.objects, function(i,profile){
                    profile = self.add_profile(profile);
                    console.log(profile)
                });
            
            }
        })
        .error(function() { 
            console.log('Error in Javascript event')
        })
        .complete(function() {});
    }
    ,init: function init() {
        var self = this;
        $.each($('.profile-popup'), function(i, item){
            var username = $(item).attr('data-username');
            self.username_list.push(username);
        });
        self.find_all()
    }
}

$(document).ready(function(){
    GlyntProfilePopup.init()
});
</script>