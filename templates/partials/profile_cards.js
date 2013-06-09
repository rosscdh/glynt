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
            <dt>Summary</dt>
            <dd>
                {{ profile.summary }}
            </dd>
            <dt>
                {{#if profile.already_incorporated }}Are already Incorporated{{ else }}Are not yet Incorporated{{/if}}
            </dt>
            
            <dt>
                {{#if profile.already_raised_capital }}Have already raised capital{{ else }}Have not yet raised capital{{/if}}
            </dt>
            <dt>
                {{#if profile.process_raising_capital }}Are in the process of raising capital{{ else }}Are not yet trying to raising capital{{/if}}
            </dt>
            <dt>
                {{#if profile.incubator_or_accelerator_name }}{{ profile.incubator_or_accelerator_name }}{{ else }} Are not part of an incubator or accelerator{{/if}}
            </dt>
            
            {{#each profile.locations }}
                {{this}}
            {{/each}}

            </dd>
        </dl>
{% endtplhandlebars %}

{% tplhandlebars "tpl-lawyer-profile" %}

    <a href="{{ profile.profile_url }}"><img class="avatar" src="{{ profile.profile_photo }}" width="50" height="50" alt="Photo of {{ profile.name }}" title="{{ profile.name }} - Lawyer" /></a>
    <h5>{{ profile.name }}<br/><small>{{ profile.position }} at {{ profile.firm }}</small></h5>
    <dl>
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
        <dt>Startups</dt>
        {{#each profile.startups }}
        <dd>
            {{ name }}
        </dd>
        {{/each}}
    </dl>
{% endtplhandlebars %}

<script type="text/javascript">

var GlyntProfileCards = {
    debug: {% if DEBUG %}true{% else %}false{% endif %}
    ,profile_api_url: '/api/v1/user/profile/?username__in={username_list}'
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
    ,log: function log(msg){
        var self = this;
        if (self.debug === true) {
            console.log(msg);
        }
    }
    ,add_profile: function add_profile(profile) {
        var self = this;
        var profile_html = null;
        var extra_context = self.extra_context || {}

        $.each(self.profile_params[profile.username], function(i,params){
            var template = params.template || 'default';

            // add the profile to the context NB necessary as this is where the display variables are kept
            context = $.extend({
                'profile': profile
            }, extra_context);

            if (template !== 'default') {
                self.log('add_profile.template ' + template + ' for '+ profile.username)
                profile_html = self.templates[template](context);
            } else {
                // if we have no specific template defined
                // then evaluate the user type and set their
                // profile html accordingly
                if (profile.is_lawyer) {
                    self.log(profile.username + 'gets the lawyer template' )
                    profile_html = self.templates.lawyer(context);
                } else if (profile.is_founder) {
                    self.log(profile.username + 'gets the founder template' )
                    profile_html = self.templates.founder(context);
                } else if (profile.is_startup) {
                    self.log(profile.username + 'gets the startup template' )
                    profile_html = self.templates.startup(context);
                } else {
                    self.log(profile.username + 'gets the unknown template' )
                    profile_html = self.templates.unknown(context);
                }
            }
            self.store_profile(profile.username, template, profile_html)
        });
        

        return self.profile_params[profile.username];
    }
    ,store_profile: function store_profile(username, template_type, html) {
        var self = this;
        self.profiles[username] = self.profiles[username] || {}
        // only srote it once
        if (self.profiles[username][template_type] === undefined) {
            self.log('storing template for: ' + username+' of template_type: '+template_type)
            self.profiles[username][template_type] = html;
        }
    }
    ,profile: function profile(username, template_type) {
        var self = this;
        if (self.profiles[username]) {
            return self.profiles[username][template_type];
        } else {
            return null
        }
    }
    /***
    * injects template for user into specific element
    */
    ,inject_into_element: function inject_into_element(target_element, username, params) {
        var self = this;
        target_element = $(target_element)
        var profile_html = self.profile(username, params.template);

        if (params.action == 'popover') {

            target.popover({
                'trigger': 'hover'
                ,'html': profile_html
            });

        } else {
            // inject by default
            target_element.html(profile_html)
        }
    }
    /***
    * injects the item html, into the target element en-masse
    */
    ,inject: function inject() {
        var self = this;
        var profile_set = self.profile_params;

        // loop over each of the users and their defined set of variables
        $.each(profile_set, function(username,target_params){
            // loop over each instance of this users profile tags on the page
            // and populate with appropriate template
            $.each(target_params, function(i,params){
                self.inject_into_element(params.target, username, params)
            })

        });
    }
    /**
    * method exists as a wrapper to allow us to perform lookups in sets of 10 at a time
    */
    ,find_by_batch: function find_by_batch(usernames) {
        var self = this;
        // uniquify
        username_items = usernames || self.usernames

        // get the list of items
        $.each(username_items.unique().inGroupsOf(10), function(i, item_set){
            // perform ajax query
            self.query_api(item_set);
        });
    }
    /**
    * Extract set of usernames from the provided list, that we dont already have
    */
    ,usernames_to_fetch: function usernames_to_fetch(usernames) {
        var self = this;
        present_usernames = Object.keys(self.profiles);
        return usernames.subtract(present_usernames);
    }
    /**
    * Get the json from the api
    */
    ,query_api: function query_api(usernames) {
        var self = this;
        // remove usernames we already have
        usernames = self.usernames_to_fetch(usernames);

        var url = self.profile_api_url.assign({'username_list': usernames})

        if (usernames.length > 0) {
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
            })
            .complete(function(){
                self.inject();
            });
        }
    }
    ,store_profile_params: function store_profile_params(params) {
        var self = this;
        // ensure is a list
        var is_new = false;
        if (self.profile_params[params.username] === undefined) {
            self.profile_params[params.username] =  [];
            is_new = true
        }

        // add dict to list for this username
        self.profile_params[params.username].push(params);
    }
    /**
    * this should not be limited as we store the element that this applies to
    */
    ,store_username_and_profile: function store_username_and_profile(params) {
        var self = this;

        self.usernames.push(params.username);
        self.usernames = self.usernames.compact().unique();

        self.store_profile_params(params);

    }
    ,parse_element: function parse_element(item) {
        var self = this;
        var elem = $(item);

        // add the user details profile
        self.store_username_and_profile({
            'username': elem.attr('data-username')
            ,'action': elem.attr('data-action') || 'inject'
            ,'template': elem.attr('data-template') || 'default'
            ,'target': elem.attr('data-target') || elem // if target specified make jquery object and use other use simply user the current element
        });
    }
    ,listen: function listen() {
        var self = this;

        $(self.selector).live('DOMNodeInserted', function(event){

            var item = event.target;
            var elem = $(item)

            if (elem.is(self.selector)) {
                //self.log(elem)
                self.parse_element(item);
                //self.find_by_batch([elem.attr('data-username')]);
            }
        })
    }
    ,init: function init() {
        var self = this;
        // setup listeners
        self.listen();

        // loop over our selector elements and try to get their info
        console.log(self.selector)
        $.each($(self.selector), function(i, item){
            self.parse_element(item)
        });
        // get the user data from the api
        self.find_by_batch();
    }
}

var GlyntStartupProfileCards = $.extend({}, GlyntProfileCards, {
    profile_api_url: '/api/v1/startup/profile/?slug__in={username_list}'
    ,selector: '.startup-profile-card'
})

$(document).ready(function(){
    var gpc = GlyntProfileCards;
    gpc.init();
    //
    var gspc = GlyntStartupProfileCards;
    gspc.init();
});
</script>