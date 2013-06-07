{% load templatetag_handlebars %}

{% tplhandlebars "tpl-profile-mini" %}
<img class="avatar" src="{{ profile.profile_photo }}" width="50" height="50" alt="Photo of {{ profile.name }}" title="{{ profile.name }} - {{#if profile.is_lawyer }}Lawyer{{/if}}{{#if profile.is_founder }}Founder{{/if}}" />
{% endtplhandlebars %}

{% tplhandlebars "tpl-unknown-profile" %}
        <img class="avatar" src="{{ profile.profile_photo }}" width="50" height="50" alt="Photo of {{ profile.name }}" title="{{ profile.name }}" />
        <h3>{{ profile.name }}</h3>
{% endtplhandlebars %}

{% tplhandlebars "tpl-startup-profile" %}
        <img class="avatar" src="{{ profile.profile_photo }}" width="50" height="50" alt="Photo of {{ profile.name }}" title="{{ profile.name }} - Startup" />
        <h5>{{ profile.name }}<br/><small>Startup</small></h5>
        <dl>
            <dt>Website</dt>
            <dd><a href="{{ profile.website }}" target="_blank">{{ profile.website }} <i class="icon-share"></i></a></dd>
            <!-- <dt>Founders</dt>
            // <dd>...</dd> -->
            <dt>Summary</dt>
            <dd>
                {{ profile.summary }}
            </dd>
            {{#if profile.locations }}
            <dt>Locations</dt>
            <dd>
            {{/if}}
            {{#each profile.locations }}
                {{this}}
            {{/each}}
            </dd>
            {{#if profile.twitter }}
            <dt>Twitter</dt>
            <dd><a href="http://twitter.com/{{ profile.twitter }}"><i class="icon-twitter"></i>{{ profile.twitter }}</a></dd>
            {{/if}}
        </dl>
        <!-- // <p class="text-center"><a href="{{ profile.profile_url }}" class="btn btn-primary">View full profile</a></p>-->
{% endtplhandlebars %}

{% tplhandlebars "tpl-lawyer-profile" %}

    <a href="{{ profile.profile_url }}"><img class="avatar" src="{{ profile.profile_photo }}" width="50" height="50" alt="Photo of {{ profile.name }}" title="{{ profile.name }} - Lawyer" /></a>
    <h5>{{ profile.name }}<br/><small>{{ profile.position }} at {{ profile.firm }}</small></h5>
    <dl>
        <!--
        // {{#if profile.website }}
        // <dt>Website</dt>
        // <dd><a href="{{ profile.website }}" target="_blank">{{ profile.website }} <i class="icon-share"></i></a></dd>
        // {{/if}} -->
        <dt>Summary</dt>
        <dd>
            {{ profile.summary }}
        </dd>
        {{#if profile.locations }}
        <dt>Locations</dt>
        <dd>
        {{/if}}
        {{#each profile.locations }}
            {{this}}
        {{/each}}
        </dd>
        {{#if profile.twitter }}
        <dt>Twitter</dt>
        <dd><a href="http://twitter.com/{{ profile.twitter }}"><i class="icon-twitter"></i>{{ profile.twitter }}</a></dd>
        {{/if}}
    </dl>
    <p class="text-center"><a href="{{ profile.profile_url }}" class="btn btn-primary">View full profile</a></p>
{% endtplhandlebars %}

{% tplhandlebars "tpl-founder-profile" %}
    <img class="avatar" src="{{ profile.profile_photo }}" width="50" height="50" alt="Photo of {{ profile.name }}" title="{{ profile.name }} - Founder" />
    <h5>{{ profile.name }}<br/><small>founder</small></h5>
    <dl>
        {{#if profile.phone }}
        <dt>Phone</dt>
        <dd>{{profile.phone}}</dd>
        {{/if}}
        <dt>Summary</dt>
        <dd>
            {{ profile.summary }}
        </dd>
        <dt>Startups</dt>
        {{#each profile.startups }}
        <dd>
            {{ name }}
        </dd>
        {{/each}}
    </dl>
    <p class="text-center"><a href="{{ profile.profile_url }}" class="btn btn-primary">View full profile</a></p>
{% endtplhandlebars %}

<script type="text/javascript">

var GlyntProfileCards = {
    profile_api_url: '/api/v1/user/profile/?username__in={username_list}'
    ,selector: '.profile-card'
    ,extra_context: {}
    ,profiles: {}
    ,profile_params:  Object.extended({})
    ,usernames: []
    ,templates: {
        'mini': Handlebars.compile($('script#tpl-profile-mini').html())
        ,'startup': Handlebars.compile($('script#tpl-startup-profile').html())
        ,'founder': Handlebars.compile($('script#tpl-founder-profile').html())
        ,'lawyer': Handlebars.compile($('script#tpl-lawyer-profile').html())
        ,'unknown': Handlebars.compile($('script#tpl-unknown-profile').html())
    }
    ,add_profile: function add_profile(profile) {
        var self = this;
        var profile_html = null;
        var extra_context = self.extra_context || {}
console.log(profile)
        $.each(self.profile_params[profile.username], function(i,params){
            var template = params.template || 'default'

            // add the profile to the context NB necessary as this is where the display variables are kept
            context = $.extend({
                'profile': profile
            }, extra_context);

            if (template !== 'default') {
                profile_html = self.templates[template](context);
            } else {
                // if we have no specific template defined
                // then evaluate the user type and set their
                // profile html accordingly
                if (profile.is_lawyer) {
                    profile_html = self.templates.lawyer(context);
                } else if (profile.is_founder) {
                    profile_html = self.templates.founder(context);
                } else if (profile.is_startup) {
                    profile_html = self.templates.startup(context);
                } else {
                    profile_html = self.templates.unknown(context);
                }
            }

            self.store_profile(profile.username, template, profile_html)
        });


        return self.profile_params[profile.username];
    }
    ,store_profile: function store_profile(username, profile_type, html) {
        var self = this;
        self.profiles[username] = self.profiles[username] || {}
        self.profiles[username][profile_type] = html;
    }
    ,profile: function profile(username, profile_type) {
        var self = this;
        return self.profiles[username][profile_type];
    }
    ,render: function render(usernames) {
        var self = this;
        var profile_set = self.profile_params.select(usernames) || self.profile_params
console.log('rdenr')
console.log(profile_set)
        // loop over each of the users and their defined set of variables
        $.each(profile_set, function(username,target_params){
            // loop over each instance of this users profile tags on the page
            // and populate with appropriate template
console.log(username +' has: '+target_params)
            $.each(target_params, function(i,params){
                var target = params.target;
                var target_profile_html = self.profile(username, params.template);

                if (params.action == 'popover') {

                    target.popover({
                        'trigger': 'hover'
                        ,'html': target_profile_html
                    });

                } else {
                    // inject by default
                    target.html(target_profile_html);
                }
            })

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
        // remove usernames that are already present
        var usernames = self.usernames.find(function(u){
            return (self.profiles[u] === undefined)
        })
        // only get the usernames we DONT have from the api
        if (usernames && usernames.length > 0) {
            var url = self.profile_api_url.assign({'username_list': usernames})
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
                }
            });
        }
        self.render();
    }
    ,listen: function listen() {
        var self = this;

        $(self.selector).live('DOMNodeInserted', function(event){
            console.log('live.load')
            var elem = $(event.target);
            self.parse_element(elem);
            self.users([elem.attr('data-username')])
        })
    }
    ,add_username: function add_username(username) {
        var self = this;
        if (self.usernames.find(username) == undefined) {
            self.usernames.push(username);
            self.usernames = self.usernames.compact();
            self.usernames = self.usernames.unique();
        }
    }
    ,parse_element: function parse_element(item) {
        var self = this;
        var elem = $(item)
        var username = elem.attr('data-username');
        var action = elem.attr('data-action') || 'inject';
        var template = elem.attr('data-template') || 'default';
        var target = elem.attr('data-target') || elem; // if target specified make jquery object and use other use simply user the current element

        self.add_username(username);

        // ensure is a list
        self.profile_params[username] = (self.profile_params[username] === undefined) ? [] : self.profile_params[username] ;

        // test if the template object is already present
        var is_already_present = self.profile_params[username].find(function(p){
            return (p.action == action && p.template == template)
        })

        // only add this item if we dont already have it
        if (is_already_present === undefined) {
            // add dict to list for this username
            self.profile_params[username].push({
                'action': action
                ,'template': template
                ,'target': target
            });
        }
    }
    ,init: function init() {
        var self = this;
        // loop over our selector elements and try to get their info
        $.each($(self.selector), function(i, item){
            self.parse_element(item)
        });
        self.listen();
        self.find_all();
    }
}

var GlyntStartupProfileCards = $.extend({}, GlyntProfileCards, {
    profile_api_url: '/api/v1/startup/profile/?slug__in={username_list}'
    ,selector: '.startup-profile-card'
})

$(document).ready(function(){
    GlyntProfileCards.init()
    GlyntStartupProfileCards.init()
});
</script>