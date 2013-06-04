{% load templatetag_handlebars %}
{% tplhandlebars "tpl-lawyer-profile-mini" %}<div class="container">
    <div class="row">
        {{ profile.name }}
        {{ profile.phone }}
        {{ profile.position }} at {{ profile.firm }}
        {{ profile.profile_photo }}
        {{ profile.years_practiced }}
        {{ profile.practice_locations }}
    </div>
</div>{% endtplhandlebars %}

{% tplhandlebars "tpl-startup-profile-mini" %}<div class="container">
    <div class="row">
        {{ profile.name }}
        {{ profile.phone }}
        {{ profile.summary }}
        {{#each profile.startups }}
            {{ name }}
            {{ summary }}
            {{ twitter }}
            {{ url }}
        {{/each}}

    </div>
</div>{% endtplhandlebars %}

<script type="text/javascript">

var GlyntProfilePopup = {
    profile_api_url: '/api/v1/user/profile/?username__in={username_list}'
    ,selector: '.profile-popup'
    ,extra_context: {}
    ,profiles: []
    ,profile_params:  Object.extended({})
    ,usernames: []
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

        self.set_profile(profile.username, profile_html)

        return this.profile(profile.username);
    }
    ,profile: function profile(username) {
// console.log(this.profiles)
        return this.profiles[username]
    }
    ,set_profile: function set_profile(key, profile_html) {
        this.profiles[key] = profile_html
    }
    ,render: function render(usernames) {
        var self = this;
        var profile_set = self.profile_params.select(usernames) || self.profile_params

        $.each(profile_set, function(username,params){
            var target_profile_html = self.profile(username);
            var target = params.target

            if (params.action == 'popover') {

                target.popover({
                    'trigger': 'hover'
                    ,'html': target_profile_html
                });

            } else {
                // inject by default
                target.html(target_profile_html)
            }
// console.log(target)
        });
    }
    ,find_all: function find_all() {
        var self = this;
        // uniquify
        self.usernames.unique()
        // get the list of items
        $.each(self.usernames.inGroupsOf(10), function(i, item_set){
            // perform ajax query
            self.users(item_set)
        });

    }
    ,users: function users(usernames) {
        var self = this;
        var url = self.profile_api_url.assign({'username_list': usernames.compact()})
        $.ajax({
            type: 'GET',
            url: url,
        })
        .success(function(data, textStatus, jqXHR) {

            if (data.objects && data.objects.length > 0) {
                // loop over elements and create the profiles
                $.each(data.objects, function(i,profile){
                    self.add_profile(profile);
                });
                self.render(usernames);
            }
        })
        .error(function() { 
// console.log('Error in Javascript event')
        })
        .complete(function() {
        });
    }
    ,init: function init() {
        var self = this;
        // loop over our selector elements and try to get their info
        $.each($(self.selector), function(i, item){
            var elem = $(item)
            var username = elem.attr('data-username');
            var action = elem.attr('data-action') || 'inject';
            var target = elem.attr('data-target') || elem; // if target specified make jquery object and use other use simply user the current element

            self.usernames.push(username);
            self.profile_params[username] = {
                'action': action,
                'target': $(target),
            };
        });
        self.find_all()
    }
}

$(document).ready(function(){
    GlyntProfilePopup.init()
});
</script>