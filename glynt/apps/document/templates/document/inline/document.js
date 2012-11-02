{% load i18n markup templatetag_handlebars %}
{% load glynt_helpers %}
{% load url from future %}

<script id="inviteeListJSON">{{ invitee_list_json|default:""|safe }}</script>
<script id="document-default_data" type="text/javascript">[{{ default_data|default:''|safe }}]</script>
<script id="js-document" type="text/x-handlebars-template">
{{ userdoc.body|default:object.body|safe }}
</script>
<script src="{{ STATIC_URL }}js/jquery.jeditable.mini.js"></script>
<script id="document-controls" type="text/javascript">
// use strict;
// use warnings;
$(document).ready(function(){
  $('#progress-buttons').hide();

  
  initArgosPanOptia = function initArgosPanOptia(App) {
    App.widgets.observer = new argosPanOptia();
  };

  initConditionalCallback = function initConditionalCallback(App) {
    App.widgets.ccbs = new conditionalCallbackSets(App.documentModel);
    App.widgets.ccbs.parseCallbacks();
  };

  initContactList = function initContactList(App) {
    // ----- FACEBOOK CALLBACK -----
    facebookCallback = function(q,callbackId,callBack) {
      var self = this;
      var results = [];

      processFriends = function(friends) {
        if (friends != undefined) {
            for (var i = 0; i < Math.min(friends.length, 2000); i++) {
                friend = friends[i];
                results.push({
                    'name': friend.name,
                    'picture': 'http://graph.facebook.com/' + friend.id + '/picture',
                    'extra': {'id': friend.id, 'service': 'facebook', 'data_type': 'friends'},
                });
            };
        } else {
            console.log('No Friends were passed in')
        }
      };

      getFBFriends = function(next_url) {
        $.ajax({
          type: 'GET',
          url: next_url,
          dataType: "jsonp"
        })
        .success(function(data, textStatus, jqXHR) {
          var response = data;

          if (response.data != undefined && response.data.length > 0) {
            processFriends(response.data);
            if (response.paging != undefined && response.paging.next != undefined) {
              getFBFriends(response.paging.next);
            }
          } else {
            // console.log('End of friends list');
            sendData();
          }
        })
        .error(function(jqXHR, textStatus, errorThrown) { 
          // console.log(errorThrown);
          sendData();// send what we have
        });
      };

      sendData = function(current_results) {
        callBack(results,callbackId);
      };

      // Only perform IF we have a FB connected account
      if (FB) {
        FB.getLoginStatus(function(response) {
            if (response.status === 'connected') {
              FB.api('/me/friends', function(response) {
                  processFriends(response.data); // process initial set
                  if (response.paging != undefined && response.paging.next != undefined) {
                    // handle pagination of friends
                    getFBFriends(response.paging.next);
                  }
              });
            }
        });
      }
    };

    App.widgets.contactsWidget = new contactsWidget([facebookCallback], {});
  };

  initSelect2 = function initSelect2(App) {
    {% if request.user.is_authenticated %}
    $(".contact-list").select2({
        query: function(query) {
            var data = {results: []};
            var template = Handlebars.compile($('#contact-list-item').html());

            App.widgets.contactsWidget.query(query.term, function(results){
                for (r in results) {
                    item = results[r];
                    data.results.push({'id': item.name , 'text': template(item), 'contact': item});
                }
                // if no results // add search term
                if (data.results.length == 0) {
                    data.results.push({'id': query.term , 'text': query.term, 'contact': {'is_query': true, 'name': query.term, 'picture': false, 'extra': {'id': MD5(String(query.term))}}});
                }
                // send data to expecting callback
                query.callback(data);
            });
        },
        width: 'element',
        minimumInputLength: 2
    });
    // connect with the App.observer
    $(".contact-list").bind("change", function(event) {
      var data = $(this).select2('data');

      var contact = data['contact'];
      if (contact['is_query'] == true) {
      } else {
        var email = (contact['extra']['email'] == undefined)? false : contact['email'];
      }

      App.dispatch('invitee.add', {'id': contact['extra']['id'], 'profile_picture': contact['picture'], 'name': contact['name'], 'email': email});
    });

    $.each($(".contact-list"), function(index, item){
      var var_name = $(this).attr('data-hb-name');
      if (var_name != undefined) {
        var var_value = App.documentModel.context()[var_name];
        if (var_value != undefined) {
          $(this).select2('data', {id:var_value, text: var_value});
        };
      }
    });
    {% endif %}
  };

    function FormControls(App) {
        var self = this;

        self.goto_step_list = Handlebars.compile($('#goto-step-list').html());
        self.actualFormSteps = ({{ form_set|length }}+1);// account for end form
        self.maxFormSteps = ko.observable(({{ form_set|length }}+1));// account for end form
        self.currentFormStep = ko.observable(1);
        self.steps = ko.observableArray([]);
        self.stepIsValid = {};
        self.isComplete = ko.observable(false);
        self.formCompleteOptions = $('div#formCompleteOptions');

        self.init = function init() {

          // happens just 1 time
          // obtain step header info for building accurate list of steps
          $('input[data-step-title]').each(function(index, element) {
                element = $(element);
                var step_title = element.attr('data-step-title');
                var form = element.closest('div.form-group');
                element.hide();
                $(this).text(step_title);
                self.steps.push({title: step_title, form_set: form})
                self.stepIsValid[index+1] = false;
          });

          // $('body').tooltip({
          //   selector: '[rel=pagination-tooltip]',
          //   placement: 'bottom',
          //   animation: false,
          //   delay: { show: 50, hide: 5 }
          // });

          self.stepVisibility(1);
        }

        self.stepList = function stepList() {
          steps = function(text){
            step_list = [];
            i = 1;

            $.each(self.steps(), function(index,element){
              is_current = self.currentFormStep() == i;
              step_text = (text == undefined || text == 'numeric') ? i : text ;
              step_name = element.title;

              step_list.push({index:i-1, text: step_text, step_name: step_name, step: i, is_current: is_current});
              i++;
            });

            return step_list;
          };
          context = {
            'current': self.currentFormStep(),
            'last': self.maxFormSteps(),
            'step_list': steps('&nbsp;')
          }
          // $.each($('ul#step-list li'), function(index,item){
          //   $(item).tooltip('hide');
          // });
          return self.goto_step_list(context);
        }
        self.renderSteps = function renderSteps() {
            App.stepListDisplay(self.stepList());
        }
        self.showNext = function showNext() {
            self.renderSteps();
            return (self.currentFormStep() == self.maxFormSteps())? false : true ;
        }
        self.showPrev = function showPrev() {
            self.renderSteps();
            return (self.currentFormStep() == 1)? false : true ;
        }
        self.isLastStep = function isLastStep() {
            is_last_step = (self.maxFormSteps() == self.currentFormStep()) ? true : false ;
            if (is_last_step == true) {
              $('#last-step').show();
            }else{
              $('#last-step').hide();
            }
            return is_last_step
        }
        self.areAllStepsComplete = function areAllStepsComplete() {
          var complete = true;
          for (var i in self.stepIsValid) {
            value = self.stepIsValid[i];
            if (value == false) {
              return false;
            }
          };
          return complete;
        }

        self.initPrevStep = function initPrevStep(active) {
          default_step = 1;

          for(var step = active; step >= 1; step--) {
              if(self.validateStep(step)) {
                  self.stepVisibility(step);
                  // persist the cookie progress
                  self.persistProgressToCookie(step);
                  return step;
              }
          }
          console.log('error has not caught valid step: '+active)
          self.stepVisibility(default_step);
        };

        self.initNextStep = function initNextStep(active) {
          default_step = parseInt(self.maxFormSteps());

          for(var step = active; step <= default_step ; step++) {
              if(self.validateStep(step)) {
                  self.stepVisibility(step);
                  // persist the cookie progress
                  self.persistProgressToCookie(step);
                  return step;
              }
          }
          console.log('error has not caught valid step: '+active)
          self.stepVisibility(default_step);
        };

        self.validateStep = function validateStep(step) {
            var ruleset = App.documentModel.getRuleByType('show_step_when');
            return true;
        }

        self.persistProgressToCookie = function persistProgressToCookie(step) {
          element = self.steps()[step]
          if (element != undefined) {
            $.each(App.documentModel.context(), function(key, value){
              App.persistKeyValueToCookie(key, value);
            });
            App.persistKeyValueToCookie('stepIsValid', self.stepIsValid);
          }

        }

        self.stepVisibility = function stepVisibility(step) {
          $.each(self.steps(), function(index,item){
              form_group = $(item.form_set);
              if ((index+1) == step) {
                  form_group.css('display', 'block');
                  form_group.removeClass('hidden');
                  window.location.hash = '#step-'+step;
              } else {
                  form_group.css('display', 'none');
                  form_group.addClass('hidden');
              }
          });
          self.currentFormStep(step);
        }

        self.goToStep = function goToStep(step) {
            self.persistProgressToCookie();// catch changes made to current step without pressing next
            App.persistCookieProgress(); // save the cahnged data
            self.initNextStep(step);
            App.message(''); // clear the message
        }

        self.next = function next() {
            var current = parseInt(self.currentFormStep()); //have to parseint as knockout seems to have int problems
            var next = current+1;
            self.persistProgressToCookie();// catch changes made to current step without pressing next

            // synchronous request
            App.validateForm(current, $('form#glynt-doc-' + current), function(textStatus, message) {
              if (textStatus == 'error') {
                self.stepIsValid[current] = false;
                self.currentFormStep(current);
              }else{
                self.stepIsValid[current] = true;
                self.initNextStep(next);
                App.message(''); // clear the message
              }
            });
        }

        self.prev = function prev() {
            var current = parseInt(self.currentFormStep()); //have to parseint as knockout seems to have int problems
            var prev = current-1;
            self.persistProgressToCookie();// catch changes made to current step without pressing next

            // synchronous request
            if (current < self.maxFormSteps()) {
                App.validateForm(current, $('form#glynt-doc-' + current), function(textStatus, message) {
                  if (textStatus == 'error') {
                    self.stepIsValid[current] = false;
                    self.currentFormStep(current);
                  }else{
                    self.stepIsValid[current] = true;
                    App.message(''); // clear the message
                    self.initPrevStep(prev);
                  }
                });
            } else {
              // we are on or less than the last page
              self.initPrevStep(prev);
              App.message(''); // clear the message
            }
        }
        
        self.init();
    }

    function Rule(element,target_element,ruleset){
        var self = this;
        self.element = (element != undefined)?element:null,
        self.target_element = (target_element != undefined)?target_element:null,
        self.ruleset = (ruleset != undefined)?ruleset:[]
    };

    function LoopStep(App, form_fieldset, hide_from_element, iteration_title){
        var self = this;
        self.form_fieldset = (form_fieldset != undefined)?form_fieldset:null;
        self.hide_from_element = (hide_from_element != undefined)?hide_from_element:null;
        self.iteration_title = (iteration_title != undefined)?iteration_title:'Item';
        self.repeatable_fields = [];
        self.repeatable_fieldset = null;
        self.hb_loop_ob_container = ko.observable({});
        self.loopContainerForContext = ko.observableArray([]);

        self.isValidInputType = function isValidInputType(element) {
            var element_type = App.getElementType(element);
            var found = false;
            if ($.inArray(element_type, App.valid_fieldtypes) != -1) {
                return true;
            }
            return false;
        }

        self.showIteration = function showIteration(index) {
            if (self.repeatable_fieldset === null) {
                // not exists create it
                fieldset = $('<fieldset class="loop" style="display:none;"><legend>&nbsp;</legend><ul class="injected"></ul>');
                target_ul = fieldset.find('ul.injected');
                for (f in self.repeatable_fields) {
                    field = $(self.repeatable_fields[f]);
                    field.css('display','');
                    target_ul.append(field);
                }
                self.repeatable_fieldset = fieldset;
            }

            // @TODO remove redundant items from the list, to allow fro increase and decrease of index
            // ruleset if they reduce ie.. 5 to 2 then 3,4,5 are deleted
            // @TODO make methods
            // @CODESMELL
            var fieldsets = self.form_fieldset.find('fieldset.loop');
            var hb_base_ob = {};
            // set array grouping context variable to allow handlebarsjs to loop
            var loop_name = 'loop_' + App.documentModel.slugify(self.iteration_title).toLowerCase();

            for (var c=1; c <= index; c++) {
                var fieldset = false;

                if (self.hb_loop_ob_container()[c] != undefined) {
                    // exists already
                    hb_ob = self.hb_loop_ob_container()[c];
                    fieldset = self.form_fieldset.find('#set-'+c);
                    fieldset.css('display','');

                    fieldset.children().each(function(index,element){
                        element = $(element);

                        if (self.isValidInputType(element) === true) {
                            var key = element.attr('name').replace(/(_(\d+))?/ig, '');
                            hb_ob[key] = element.val();
                        }
                    });
                }else{
                    hb_ob = $.extend({}, hb_base_ob);
                    hb_ob['id'] = self.iteration_title.toLowerCase() +'_'+ c;
                    hb_ob['index'] = c;
                    // new so create it based on default
                    // deep copy the set
                    fieldset = self.repeatable_fieldset.clone();
                    // set element attribs
                    fieldset.attr('id', 'set-'+c)
                    fieldset.css('display','');
                }

                legend = fieldset.find('legend');
                legend.html(self.iteration_title + '&nbsp;' + c); // @TODO need to put real title name here

                // loop over element set of inputs (that are valid)
                if (fieldset !== null) {
                    fieldset.find(App.valid_fieldtypes.join(',')).each(function(index,element){
                        element = $(element);
                        if (self.hb_loop_ob_container()[c] == undefined) {
                            if (self.isValidInputType(element) === true) {
                                // update id to be unique
                                old_id = element.attr('id');
                                new_id = old_id + '_' + c;
                                element.attr('id', new_id);
                                // update name to be unique
                                old_name = element.attr('name');
                                new_name = old_name + '_' + c;
                                element.attr('name', new_name);
                                slug_with_no_id = old_name.replace(/(_(\d+))?/ig, '');

                                // update hb-name so that we get correct context variables
                                element.attr('data-hb-name', old_name);
                                element.attr('data-loop_name', loop_name);

                                // set the context params
                                hb_ob = App.documentModel.ensureElementContextRadioCheckboxOptionsPresent(element,hb_ob);
                                hb_ob[slug_with_no_id] = element.val();

                            }
                        }
                    });
                }
                self.form_fieldset.append(fieldset);
                self.hb_loop_ob_container()[c] = hb_ob;
            }

            // @TODO DELETE HACK
            for (var c=index+1; c <= fieldsets.length; c++) {
                // hide these elements
                $(fieldsets[c]).remove();
                self.form_fieldset.find('#set-'+c).remove();
                delete self.hb_loop_ob_container()[c];
            }
            self.loopContainerForContext([]);//reset
            for (i in self.hb_loop_ob_container()) {
                self.loopContainerForContext().push(self.hb_loop_ob_container()[i]);
            }

            App.documentModel.setContextItemByForce(loop_name, self.loopContainerForContext());
        }

        self.init = function init(){
        // loop over ALL form elements (including labels and other helper items) find the from element and hide all those after
            var found = false;
            self.form_fieldset.find(App.valid_fieldtypes.join(',')).each(function(index,element){
                element = $(element);
                if (element.attr('id') == $(hide_from_element).attr('id')) {
                    found = true;
                } else {
                    if (found == true) {
                        element = element.closest('div.control-group'); //is we are using fo
                        element.hide();
                        self.repeatable_fields.push(element);
                        element.remove();
                    }
                }

            });
        }

        self.init();
    };

  function DocumentModel(App) {
    var self = this;

    self.textElementsList = ['text','textarea','hidden','select'];
    self.FalseValuesList = ['False','false',false,null,void 0,''];
    self.handlebarsElementId = ko.observable('script#js-document');
    self.compiledTemplate = Handlebars.compile($(self.handlebarsElementId()).html()); // must not be ko.observable
    self.renderedHTML = ko.observable('');

    self.visibilityRuleset = ko.observableArray([]);
    self.loopStepList = ko.observable({});

    self.ruleSet = ko.observable({
        'show_step_when': [],
        'show_element_when': []
    });

    self.context = ko.observable({
        'user_company_name': 'RuleNo1',
            'user_company_url': 'http://www.ruleno1.com',
        'document_title': '{{ userdoc.name|default:object.name|escapejs }}'
    });

    self.getRuleByType = function getRuleByType(ruleset_type) {
        if (ruleset_type in self.ruleSet()) {
            return self.ruleSet()[ruleset_type];
        }
        return false;
    }

    self.setRule = function setRule(element,ruleset) {
        var rule = new Rule(element);
        for (r in self.ruleSet()) {
            if (r in ruleset) {
                if (r == 'show_step_when') {
                    rule.target_element = $(element.closest('div.form-group')[0]);
                }
                rule.ruleset.push(ruleset[r]);
                self.ruleSet()[r].push(rule);
            }
        };
    }

    self.showLoopStep = function showLoopStep(element, num) {
        var formset_id = $($(element).closest('div.form-group')[0]).attr('id');
        self.loopStepList()[formset_id].showIteration(num);
    }

    self.getLoopStepByChildElement = function getLoopStepByChildElement(requested_element) {
        var found = false;
        var requested_id = parseInt(requested_element.attr('id').replace(/[^\d]+/ig, ''));
        var formset_id = $($(requested_element).closest('div.form-group')[0]).attr('id');

        $.each(self.loopStepList()[formset_id].hb_loop_ob_container(), function(index,element){
            if (found === false && element['id'] != undefined) {
                var item_id = parseInt(element['id'].replace(/[^\d]+/ig, ''));

                if (item_id === requested_id) {
                    found = {
                        'formset_id': formset_id,
                        'context_index': index,
                        'container_context': element,
                    }
                };
            }
        });

        return found;
    }

    self.setLoopStep = function setLoopStep(form_fieldset, hide_from_element, iteration_title) {
        var formset_id = $($(hide_from_element).closest('div.form-group')[0]).attr('id');
        self.loopStepList()[formset_id] = new LoopStep(App, form_fieldset, hide_from_element, iteration_title);
    }

    self.slugify = function slugify(text) {
        if (typeof text == 'boolean') {
            text = (text === true)?'true':'false';
        } else if (text != undefined && text != null) {
            text = text.replace(/[^_-a-zA-Z0-9,&\s]+/ig, '');
            //text = text.replace(/-/gi, "_");
            text = text.replace(/\s/gi, "-").toLowerCase();
        }
        return text;
    }

    self.assertElementIsVisibleWhen = function assertElementIsVisibleWhen(key, value) {
        if (key in self.context()) {
            var context_value = self.context()[key];
            if (context_value == value) {
                return true;
            } else {
                // hide the relavant object
            }
        }
        return false;
    }

    self.determineValue = function determineValue(input) {
        var value = null;
        var is_placeholder_value = true;
        if (input.val() != undefined && input.val() != '') {
          value = input.val();
          is_placeholder_value = false;
        } else {
          value = input.attr('placeholder');
        }

        if (self.textElementsList.indexOf(input.attr('type')) >= 0 || self.textElementsList.indexOf(input.prop('type')) >= 0) {
                //value = '[' + value.toString() + ']';
                value = value.toString();
        }
        // if the textElementsList has no type of this type.. it could be a checkbox or radio
        if (self.textElementsList.indexOf(input.attr('type')) == -1) {
            
            if (input.attr('type') == 'radio' || input.attr('type') == 'checkbox') {
                value = (input.attr('checked') == 'checked') ? true : false ;
            }
        }

        return {
            'value': value,
            'is_placeholder_value': is_placeholder_value
        };
    };

    self.setTemplateHasHelperValues = function setTemplateHasHelperValues(input, value, is_placeholder_value) {
        var key = 'has_' + input.attr('data-hb-name');
        var has_this_value = (self.FalseValuesList.indexOf(value) >= 0 || is_placeholder_value === true)? false : true ;
        self.setContextItemByForce(key, has_this_value);
    };

    // method to set the _value values of the specified item
    self.getTemplateHelperKey = function getTemplateHelperKey(input) {
        var value = input.val();
        var slug = self.slugify(input.attr('data-hb-name'));
        var value_slug = self.slugify(value);
        var key = '_' + slug + '_' + value_slug;
        var id_free_key = key.replace(/_[\d]+/ig, '');
        return {
            'value': value,
            'slug': slug,
            'value_slug': value_slug,
            'id_free_key': id_free_key,
            'key': key,
        };
    };

    self.ensureElementContextRadioCheckboxOptionsPresent = function ensureElementContextRadioCheckboxOptionsPresent(element,local_context) {
        var required_name = element.attr('name');

        if (element.attr('type') == 'radio' || element.attr('type') == 'checkbox') {
            if (element.attr('name') == required_name) {
                // found the name of the lement so ensure the key exists
                // @TODO these variables need to be commmon make a method
                var slug = self.slugify(element.attr('data-hb-name')).replace(/(_[\d]+)/ig, '');
                var value_slug = self.slugify(element.val());
                var key = '_' + slug + '_' + value_slug;

                if ((key in local_context) == false) {
                    local_context[key] = false;
                }else{
                    for (context_key in local_context) {
                        if (context_key.indexOf(slug) >= 0) {
                            // found it
                            if (element.attr('checked') == 'checked') {
                                // exists 
                                local_context[key] = true;
                            }else{
                                local_context[key] = false;
                            }
                        }
                    }
                }

            }
        };
        return local_context;
    }

    // This is where radio and checkboxes in a loop are handled
    self.setTemplateHelperValues = function setTemplateHelperValues(input, local_context) {
        // set custom
        helper = self.getTemplateHelperKey(input);

        var context = (local_context == undefined) ? self.context() : local_context ;
        var slug = helper['slug'];
        var key = helper['key'];

        if (input.attr('type') == 'radio') {
            helper = self.ensureElementContextRadioCheckboxOptionsPresent(input,helper);
            context = $.merge(context,helper);
        }

        if (local_context == undefined) {
            // set the base key value for this input
            self.setContextItemByForce(key, true);
        }

        return context;
    }

    self.setTemplateHelperValuesForLoopStep = function setTemplateHelperValuesForLoopStep(name, value, loop_index, loop_name) {
      var cookie_key = name + '_' + loop_index;// cookie_name
      App.persistKeyValueToCookie(cookie_key, value);

      var context = self.context();
      loop_index = parseInt(loop_index) - 1;
      context[loop_name][loop_index][name] = value;
      self.context(context);
    }

    self.setContextItem = function setContextItem(input,local_context) {
      // only allow if the data-hb-name is set
      if (typeof input.attr('data-hb-name') == 'string') {
          var context = (local_context == undefined) ? self.context() : local_context ;
          var key = input.attr('data-hb-name');
          var loop_name = input.attr('data-loop_name');

          var value_ob = self.determineValue(input);
          var value = value_ob['value'];
          var is_placeholder_value = value_ob['is_placeholder_value'];

          if (loop_name != undefined) {
            // loopstep input
            loop_index = input.attr('id').replace(/[^\d]+/ig, '');
            self.setTemplateHelperValuesForLoopStep(key, value, loop_index, loop_name);
          } else {
            // normal input
            // set the helper values
            self.setTemplateHelperValues(input);
            context[key] = value;
            App.persistKeyValueToCookie(key, value);
          }

          // set the has_attrib values
          self.setTemplateHasHelperValues(input, value, is_placeholder_value);

          if (local_context == undefined) {
            self.context(context);
          } else {
            return context
          }
      }
      return false;
    }

    self.setContextItemByForce = function setContextItemByForce(key,value) {
        var context = self.context();
        context[key] = value;
        self.context(context);
    }

    self.render = function render() {
        return self.compiledTemplate(self.context());
    }
  }

    /**
    * Primary view acts as a holder for the other views
    */
	$(window).scroll(function(){
	    $(".document-questions").css("top",Math.max(45,130-$(this).scrollTop()));
	});
	$(window).resize(function() {
		$(".document-questions").height($(window).height());
	});
	
    function PageDocumentController() {
        var self = this;
        self.valid_fieldtypes = ['input', 'text','select','textarea','select-one','radio','checkbox']
        self.markdownConverter = new Markdown.Converter();
        self.targetDocumentId = ko.observable('span#document-md');
        self.documentModel = new DocumentModel(self);
        self.formControls = new FormControls(self);
        self.stepListDisplay = ko.observable(self.formControls.stepList());
        self.message = ko.observable(null);
        self.widgets = {};

        self.setGlyntRuleset = function setGlyntRuleset() {
            // loop over lements looking for rulesets
            $('form.bind-document input[data-glynt-rule]').each(function(index,element){
                var rules = eval($(element).attr('data-glynt-rule'));
                rules = rules[0];// javascript json weirdness
                self.documentModel.setRule($(element), rules);
            });
            $('form.bind-document [data-glynt-loop_step]').each(function(index,element){
                var form_fieldset = $(element).closest('div.form-group');
                var data = eval($(element).attr('data-glynt-loop_step'))[0];
                var hide_from_element = $('[name='+ data['hide_from'] +']')[0];
                var iteration_title = data['iteration_title'];
                
                self.documentModel.setLoopStep(form_fieldset, hide_from_element, iteration_title);
            });
        }

        // @TODO apply rulesets
        self.applyGlyntRuleset = function applyGlyntRuleset() {
            var current_context = self.documentModel.context();
            var ruleset = self.documentModel.getRuleByType('show_step_when');

            var target_element = null;
            var target_element_step_id = null;

            var callback = null;
            var required_value = null;
            var current_context_value = null;

            for (var x=0; x < ruleset.length; x++) {

                if (ruleset[x].target_element == 'undefined') {
                    target_element = $(ruleset[x].target_element);
                    target_element_step_id = target_element.attr('id').replace(/[^\d]+/ig, '');
                } else {
                    target_element = null;
                    target_element_step_id = null;
                }

                for (var i=0; i < ruleset[x].ruleset.length; i++) {
                    callback = (ruleset[x].ruleset[i]['callback'] == 'undefined')? null : ruleset[x].ruleset[i]['callback'] ;
                    for (var context_var_name in ruleset[x].ruleset[i]) {

                        required_value = ruleset[x].ruleset[i][context_var_name];    
                        if (context_var_name in current_context) {
                            current_context_value = current_context[context_var_name];
                            if (required_value == current_context_value) {
                                // apply callback
                            }
                        }
                    }
                }
            }
        }

        self.setContext = function setContext() {
            // loop over all valid form elements and set them in the context
            var name = null;
            var value = null;

            $('form.bind-document').find(self.valid_fieldtypes.join(',')).each(function(index,element){
              self.documentModel.setContextItem($(element));
            });
        }

        self.initializeValuesFromDefaultData = function initializeValuesFromDefaultData() {
            var data = $.parseJSON($('script#document-default_data').html());
            if (data) {
                data = data[0];
                if (data) {
                    $('form.bind-document').find(self.valid_fieldtypes.join(',')).each(function(index,element){
                        element = $(element);
                        element_name = element.attr('name');
                        if (element_name != undefined && element_name in data) {
                            element.val(data[element_name]);
                        }
                    });
                }
            }
        }

        /**
        * Method is required to delete other cookie docs and save space in the cookie
        * to prevent the 400 error that occurs when we run out of cookie mem space
        */
        self.deleteOtherDocCookies = function deleteOtherDocCookies() {
            arrCookieDocs = document.cookie.split(';');
            for (var i = 0; i < arrCookieDocs.length; i++) {
                var name_value = arrCookieDocs[i].split("=");
                if (name_value[0].indexOf('glynt-') != -1) {
                    if (name_value[0] != '{{ userdoc.cookie_name }}') {
                        // expire these other cookie docs
                        $.cookie(name_value[0], null);
                    }
                }
            }
        };

        self.initializeValuesFromCookie = function initializeValuesFromCookie() {
            self.deleteOtherDocCookies();
            var cookie_value = $.parseJSON($.cookie('{{ userdoc.cookie_name }}'));
            if (cookie_value) {
                cookie_value = $(cookie_value);
                if (cookie_value.length >= 0) {
                    $('form.bind-document').find(self.valid_fieldtypes.join(',')).each(function(index,element){
                        element = $(element);
                        element_name = element.attr('name');
                        if (element_name != undefined && cookie_value.attr(element_name) != undefined) {
                            element.val(cookie_value.attr(element.attr('name')));
                        }
                    });
                }
            }
        }

        self.render = function render() {
            self.documentModel.renderedHTML(self.renderMarkdown(self.documentModel.render()))
        }
        self.renderMarkdown = function renderMarkdown(md) {
          return self.markdownConverter.makeHtml(md);
        }

        self.changeContext = function changeContext(input) {
            self.documentModel.setContextItem(input);
            self.render();
        }

        {% if userdoc %}
        self.validateForm = function validateForm(step, form, callback) {
            var is_valid = false;
            var form_data_serialized = form.serialize();
            $.ajax({
              type: 'POST',
              url: "{% url 'document:my_view' slug=userdoc.slug %}?step="+step,
              data: form_data_serialized,
              current_progress: $.cookie('{{ userdoc.cookie_name }}')
            })
            .success(function(data, textStatus, jqXHR) {
                var response_data = $.parseJSON(data);
                self.message('');
                is_valid = true;
                self.clearInjectedErrors();
                // Actual data save takes palce here; validateForm is just a validation
                self.persistCookieProgress(); // save the changed data
            })
            .error(function(jqXHR, textStatus, errorThrown) { 
                var data = $.parseJSON(jqXHR.responseText);
                self.clearInjectedErrors();
                self.message(data.message);

                $.each(data.errors, function(key, errors){
                    var intKey = parseInt(key);
                    if (typeof intKey == 'number' && form.find('[name=step_title]').attr('data-glynt-loop_step') != undefined) {
                        // loop-step
                        $.each(errors, function(index, error){
                            field = form.find('#id_'+index+'_'+key);
                            self.injectError(field, error);
                        });
                        
                    } else {
                        // normal step
                        field = $('#id_' + key);
                        self.injectError(field, errors);
                    }
                    
                });
                is_valid = false;
            })
            .complete(function(jqXHR, textStatus) {
              // issue callback
              if (callback != undefined) {
                callback(textStatus, self.message());
              }
            });

            return is_valid;
        };
        // inject an error into a field control-group -> controls
        self.injectError = function injectError(field, errors) {
            var control_element = field.closest('.controls');

            var error_list = $('<ul/>',{ class: 'errorlist'});
            $.each(errors, function(index, error){
                error_list.append($('<li/>',{html: error}))
            });
            
            $(control_element).prepend(error_list);
        };
        self.clearInjectedErrors = function clearInjectedErrors() {
            $.each($('body').find('.errorlist'), function(index, item){
                $(item).remove();
            });
        }
        {% endif %}

        {% if userdoc %}
        // method to persist the cookie data
        self.persistCookieProgress = function persistCookieProgress() {

            var csrf_token = self.getCSRFToken();
            var data = {
                csrfmiddlewaretoken: csrf_token,
                current_progress: $.cookie('{{ userdoc.cookie_name }}'),
            };

            $.ajax({
              type: 'POST',
              url: "{% url 'document:my_persist' pk=userdoc.pk %}",
              data: data,
            })
            .success(function(data, textStatus, jqXHR) {
                var data = data[0];
            })
            .error(function(jqXHR, textStatus, errorThrown) { 
            })
            .complete(function() {
            });
        }
        {% endif %}

        {% if userdoc %}
        self.persistKeyValueToCookie = function persistKeyValueToCookie(key,value) {
            var cookie_value = $.parseJSON($.cookie('{{ userdoc.cookie_name }}'));
            cookie_value = (cookie_value == undefined) ? {} : cookie_value ;
            cookie_value[key] = value;
            $.cookie('{{ userdoc.cookie_name }}', JSON.stringify(cookie_value));
        };
        {% endif %}

        {% if userdoc %}
        self.generatePDF = function generatePDF() {
            var url = "{% url 'export:as_pdf' slug=userdoc.slug %}";
            document.location = url;
        }
        {% endif %}

        self.getCSRFToken = function getCSRFToken() {
          var csrf_token = $.cookie('csrftoken');
          return csrf_token;
        }

        // Method to actual save the document:title
        self.saveDocumentNameChange = function saveDocumentNameChange() {

            var csrf_token = self.getCSRFToken();
            var data = {
                csrfmiddlewaretoken: csrf_token,
                current_progress: $.cookie('{{ userdoc.cookie_name }}'),
                name: $('form#userdoc-name-form input#id_name').val(),
                id: $('form#userdoc-name-form input#id_id').val()
            };

            $.ajax({
              type: 'POST',
              url: "{% url 'document:validate_form' slug=object.slug %}",
              data: data,
            })
            .success(function(data, textStatus, jqXHR) {
                var data = data[0];
                if (data.url != undefined && data.url != document.location) {
                    document.location = data.url;
                } else {
                    console.log('Missing URL to redirect to')
                }
            })
            .error(function(jqXHR, textStatus, errorThrown) { 
                console.log(jqXHR)
            })
            .complete(function() {
            });
        };

        self.getElementType = function getElementType(element) {
            var element_type = element.attr('type');
            if (element_type == undefined) {
                // textarea?
                element_type = element.prop('type');
            }
            return element_type;
        };

        self.initializeLoopSteps = function initializeLoopSteps() {
          $('form.bind-document [data-glynt-loop_length]').each(function(index, element){
            element = $(element);
            var num = parseInt(element.val());
            if (typeof num == 'number'){
                self.documentModel.showLoopStep(element, num);
            }
          });
        }

        // @TODO CODESMELL clean this up
        self.bindLoopStepContextData = function bindLoopStepContextData(fieldset) {
          fieldset = (fieldset == undefined) ? $('form.bind-document fieldset.loop') : fieldset ;

          fieldset.each(function(index,loopstep){
            loopstep = $(loopstep);
            var applicableLoopObject = self.documentModel.getLoopStepByChildElement(loopstep.find('input:first'));

            if (applicableLoopObject) {
                fieldset.find('input,textarea,select').each(function(index, element){
                    element = $(element);
                    var target_id = parseInt(element.attr('id').replace(/[^\d]+/ig, ''));
                    var target_value = element.val();
                    var target_name = $(element).attr('data-hb-name');

                    if (target_name != undefined) {
                      applicableLoopObject['container_context'][target_name] = target_value;
                    }
                });

                var found = false;
                fieldset.find('input[type=radio], input[type=checkbox]').each(function(index,element){
                    element = $(element);
                    var element_type = element.attr('type');
                    var target_id = parseInt(element.attr('id').replace(/[^\d]+/ig, ''));
                    var target_value = element.val();
                    var target_name = $(element).attr('data-hb-name');

                    // because its a iteratable(radio,cehckbox) within a loop object we need to itereate
                    requested_slug = self.documentModel.slugify(element.attr('data-hb-name')).replace(/(_[\d]+)/ig, '');
                    requested_value_slug = self.documentModel.slugify(element.val());
                    requested_target_name = '_' + requested_slug + '_' + requested_value_slug;

                    fieldset.find('input[type='+ element_type +']').each(function(index,element){
                        element = $(element);

                        slug = self.documentModel.slugify(element.attr('data-hb-name')).replace(/(_[\d]+)/ig, '');
                        value_slug = self.documentModel.slugify(element.val());
                        target_name = '_' + slug + '_' + value_slug;

                        if (requested_target_name == target_name && element.attr('checked') == 'checked') {
                            applicableLoopObject['container_context'][target_name] = true;
                            found = true;
                        }else{
                            if (found == false){
                                applicableLoopObject['container_context'][target_name] = false;
                            }
                        }
                    });
                });
            }
          });

        }

        self.registerCallback = function registerCallback(event_name, callback) {
          self.widgets.observer.registerCallback(event_name, callback);
        };
        self.dispatch = function dispatch(event_name, value) {
          self.widgets.observer.dispatch(event_name, value);
        };

        // method to initialize 3rd part widgets that need to load after
        // our js events happen
        self.initializeWidgets = function initializeWidgets() {
          initContactList(self);
          initConditionalCallback(self);
          initSelect2(self);
        };

        self.init = function init() {
          initArgosPanOptia(self);
          self.initializeValuesFromCookie();// cookie basics

          self.setGlyntRuleset();
          self.applyGlyntRuleset();
          self.initializeLoopSteps();
          self.bindLoopStepContextData();

          self.initializeValuesFromDefaultData();// main initializer
          self.setContext();

          self.initializeWidgets();

          self.render();
          // show the buttons which are hidden by default
          $('#progress-buttons').show();
        };

        self.init();
    }

    /**
    * Handler for fields that have show-when and hide when callbacks
    */
    conditionalCallbackSets = function(documentModel) {
      var self = this;
      var showWhen = [];
      var hideWhen = [];

      self.init = function init() {
        // find show-when elements and hide them by default
        self.showWhen = self.showWhenItems();
        // find hiden-when elements and show if their status is correct
        self.hideWhen = self.hideWhenItems();
        self.parseCallbacks();
      };

      self.showWhenItems = function showWhenItems() {
        return $('*[data-show_when]');
      };

      self.evaluateShowWhenItem = function evaluateShowWhenItem(element) {
      };

      self.hideWhenItems = function hideWhenItems() {
        return $('*[data-hide_when]');
      };

      self.evaluateHideWhenItem = function evaluateHideWhenItem(element) {
      };

      self.parseCallbacks = function parseCallbacks() {
        $.each(self.hideWhen, function(i,item) {
          item = $(item);
          if (self.inlineCallBack(item.attr('data-hide_when')) == true) {
            self.recordHiddenField(item, true);
            item.closest('.control-group').hide();
          }else{
            self.recordHiddenField(item, false);
            item.closest('.control-group').fadeIn('slow');
          };
        });
        $.each(self.showWhen, function(i,item) {
          item = $(item);
          if (self.inlineCallBack(item.attr('data-show_when')) == true) {
            self.recordHiddenField(item, false);
            item.closest('.control-group').fadeIn('slow');
          }else{
            self.recordHiddenField(item, true);
            item.closest('.control-group').hide();
          };
        });
      };
      /**
      * populate the step input#hidden_fields field with the names of items affected
      */
      self.recordHiddenField = function recordHiddenField(field, is_hidden) {
        field = $(field);
        target_field = field.closest('form').find('input[name=hidden_fields]:first')[0];
        target_field = $(target_field);

        val = (target_field.val() != '') ? target_field.val() : '[]' ;
        data = $.parseJSON(val);
        // perform union or intersect to add or remove name from list
        data = (is_hidden === true) ? data.union([field.attr('name')]) : data.subtract([field.attr('name')]) ;
        // set the value in the hidden field
        target_field.val(JSON.stringify(data));
        
      };

      self.parseVariable = function parseVariable(variable) {
        if (variable.indexOf('"') != -1 || variable.indexOf("'") != -1) {
          variable = variable.replace(/[\'\"]/gi,'');
          variable = '"' + variable + '"';
        } else {
          variable = variable.replace(/[\'\"]/gi,'"');
          if (isNaN(variable)) {
            variable = documentModel.context()[variable];
            variable = '"' + variable + '"';
          }
        }
        return variable;
      };

      self.inlineCallBack = function inlineCallBack(callback) {
          re = new RegExp("^(.+) ([\={1,2}\!\>\<]+) ([\'\"]?.+?[\'\"]?)$",'ig');
          var match = re.exec(callback)
//          console.log(match)
          var variable = self.parseVariable(match[1]);
          var comparison = match[2];
          var operator = self.parseVariable(match[3]);
          //console.log(operator)

          expression = variable + comparison + operator;
//          console.log('expression is: ' + eval(expression))
          return eval(expression);
      };

      self.init();
    };

    // ----- KO Instance -----
    App = new PageDocumentController();
    // ----- KO Bindings -----
    ko.applyBindings(App);

    $('form.bind-document [data-glynt-loop_length]').live('change', function(event){
        var num = parseInt($(this).val());
        if (typeof num == 'number'){
            App.documentModel.showLoopStep($(this), num);
        }
    });
    $('.fix-errors').live('click', function(event){
        event.preventDefault;
        App.formControls.prev();
    });

    $('.md-updater').live('change', function(event){
        event.preventDefault();
        App.changeContext($(this));
        App.widgets.ccbs.parseCallbacks();
    });

    $('.is_invitee').live('change', function(event){
        var field = $(this);
        var id = slugify(field.val());
        var name = field.val();
        var email = null;
        var picture = null;
        App.dispatch('invitee.add', {'id': id, 'profile_picture': picture, 'name': name, 'email': email});
    });

    $('button#btn-post-pdf').live('click', function(event){
        event.preventDefault();
        App.generatePDF();
    });

    $("input.datepicker").datepicker({dateFormat:"dd MM yy",changeYear:true,changeMonth:true});

    $('ul#step-list li').live('click', function(event){
      event.preventDefault();
      var step = $(this).attr('data-goto_step');
      App.formControls.goToStep(step);
    });

    if ($.cookie('{{ userdoc.cookie_name }}') == null) {
        $.cookie('{{ userdoc.cookie_name }}', JSON.stringify({}));
    }

    {% if userdoc_form %}
    $('#document-title.editable').editable(function(value, settings) { 
        $('form#userdoc-name-form input#id_name').val(value);
        App.saveDocumentNameChange();
        return(value);
    }, { 
        indicator : 'Saving...',
        tooltip   : 'Click to create your new document...',
        placeholder : 'Click to create your new document...',
        type      : 'text',
        submit    : '{% trans "Save" %}',
    });
    {% endif %}


    var hb_popover_template = Handlebars.compile($('#hb-popover').html());
    $('.md-updater').popover({
      trigger: 'hover',
      title: function() {
        return 'Info';//$(this).closest('div.control-group').find('label:first').html();
      },
      content: function() {
          var control_group = $(this).closest('div.control-group');
        item = {
          'field_label': control_group.find('label').html(),
          'explain': control_group.find('span.helptext').html(),
          'example': $(this).attr('placeholder')
        }

        return hb_popover_template(item);
      },
    });
});
</script>

{% tplhandlebars "goto-step-list" %}
<ul id="step-list" class="nav nav-tabs">
  {{#each step_list}}
  <li data-goto_step="{{step}}" rel="pagination-tooltip" title="{{step_name}}" class="{{#if is_current}}active{{/if}}">
  	<a href="#">{{step_name}}	<span class="page_num" style="display:hidden">{{text}}</span></a>
  </li>
  {{/each}}
  <li data-goto_step="{{last}}" class="last_step" title="{{step_name}}"><a href="#">Finalize</a></li>
</ul>
{% endtplhandlebars %}

{% tplhandlebars "contact-list-item" %}
    <img src="{{picture}}" width="45" height="45" />
    {{name}}
{% endtplhandlebars %}

{% tplhandlebars "hb-popover" %}
    <p>
    {{#if explain}}
    {{explain}}<br/>
    {{/if}}
    {{#if example}}
    <i>i.e:</i>&nbsp;{{example}}
    {{/if}}
    </p>
{% endtplhandlebars %}


{% if request.user.is_authenticated %}
	{% include 'socialregistration/facebook_js/facebook_js.html' %}
{% endif %}