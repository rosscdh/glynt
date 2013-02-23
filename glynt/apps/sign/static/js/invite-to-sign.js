$(document).ready(function(){
  /**
  * Invite To Sign Widget - Allows a list of signatories tobe generated
  * this list is then posted and the backend sends an invite email
  * and unique hash to the invitee list; those invitees are then invited
  * to sign this document
  */
  inviteToSignWidget = function inviteToSignWidget(params) {
    var self = this;
    self.urls = {};
    self.target_element = params['target_element'];
    self.compiledTemplate = Handlebars.compile($('#hb-invite-signatories').html());
    self.compiledDetailTemplate = Handlebars.compile($('#hb-signatory-detail').html());
    self.inviteForm = 'form#send-invite';
    self.context = params;
    self.context['csrf_token'] = $.cookie('csrftoken');;
    self.context['invitees'] = (params['invitees'] != undefined) ? params['invitees']: [];
    self.context['can_add_invite'] = (params['can_add_invite'] === 'true') ? true: false;

    self.findInvitee = function findInvitee(id, find_by_key) {
      invitee = false;
      found_index = false;
      if (find_by_key == undefined) {
        find_by_key = 'id';
      }
      if (id) {
        $.each(self.context['invitees'], function(index, item) {
          if (item[find_by_key] == id) {
            invitee = item;
            found_index = index;
            return true;
          }
        });
      };
      return {'invitee': invitee, 'index': found_index};
    };

    self.add = function add(id, email, name, profile_picture, has_signed) {
      var item = self.findInvitee(id);
      if (item.index === false){
        self.context['invitees'].push({'id': id, 'email': email, 'name': name, 'profile_picture': profile_picture, 'has_signed': has_signed})
        self.render();
      };
    };

    self.update = function update(id, name, email) {
      var item = self.findInvitee(id);
      if (item.index === false) {
        // new invitee
        id = MD5(String(email));
        has_signed = false;
        profile_picture = '';// url to grayman
        self.add(id, email, name, profile_picture, has_signed);
      } else {
        // existing invitee
        // merge hashes
        $.extend(item.invitee, {'email': email, 'name': name});
        self.context['invitees'][item.index] = item.invitee;
      }
      self.render();
    };

    self.showDetailView = function showDetailView(id) {
      var selectedItem = {};

      $.each(self.context['invitees'], function(index, item){
        if (item.id == id) {
          item['index'] = index;
          selectedItem = item;
          return false;
        }
      });

      $( "#signatory-detail" ).html(self.compiledDetailTemplate({'invitee': selectedItem}));
      $('div#modal-signatory-detail').modal('show');
      $('div#modal-signatory-detail').find('#id_detail-name').select();
    };

    self.remove = function remove(id) {
      $.each(self.context['invitees'], function(index, item){
        if (item.id == id) {
          self.context['invitees'].splice(index, 1);
          self.removeInvitation(item.id);
          return false;
        }
      });
      self.render();
    };

    self.render = function render() {
      self.context['csrf_token'] =  $.cookie('csrftoken'); // update the csrf token and make it current
      self.target_element.html(self.compiledTemplate(self.context));
    };

    self.removeInvitation = function removeInvitation(id) {
      self.processRequest(self.urls.remove_invitee.replace('/0/', '/'+ id +'/'), {}, 'DELETE', function(data, textStatus, jqXHR){ return null; }, function(xhrObj){ xhrObj.setRequestHeader("X-CSRFToken", $.cookie('csrftoken')); });
    };

    self.sendInvitation = function sendInvitation() {
      var form = $(self.inviteForm);
      self.processRequest(self.urls.send_invitations, form.serialize(), 'POST', function(data, textStatus, jqXHR){
        // need to update the local invitees with their new pk values
        $.each(data, function(index, item){
          invitee = self.findInvitee(item.email, 'email')
          if (invitee) {
            self.context['invitees'][invitee.index].id = item.pk;
          }
        });
      });
    };

    self.processRequest = function processRequest(url, data, type, successCallback, beforeSendCallback) {
      if (beforeSendCallback == undefined) {
        beforeSendCallback = null;
      }
      var form = $(self.inviteForm);
      $.ajax({
        type: type,
        beforeSend: beforeSendCallback,
        url: url,
        data: data,
      })
      .success(function(data, textStatus, jqXHR) {
          var response_data = $.parseJSON(data);
          self.context['message'] = 'success';
          if (successCallback != undefined) {
            successCallback(response_data, textStatus, jqXHR);
          }
      })
      .error(function(jqXHR, textStatus, errorThrown) { 
        self.context['message'] = 'Error: ' + errorThrown;
      })
      .complete(function(jqXHR, textStatus) {
        self.render();
      });
    };

    self.listen = function listen() {
      $.Queue('invitee.data').subscribe(self.load_contacts);
      $.Queue('invitee.add').subscribe(self.contact_add);

      $(self.target_element).addClass('invitee-vehicle');

      $(document).on('click', '#submit-invitation',  function(event){
          event.preventDefault();
          self.sendInvitation();
      });
      $(document).on('click', '.signatory_add', function(event){
          event.preventDefault();
          self.showDetailView();
      });
      $(document).on('click', '.signatory_detail',  function(event){
          event.preventDefault();
          self.showDetailView($(this).attr('data-index_lookup'));
      });
      $(document).on('click', '.signatory_remove',  function(event){
          event.preventDefault();
          self.remove($(this).attr('data-index_lookup'));
      });
      $('div#modal-signatory-detail"').modal('hide');

      $(document).on('click', 'button#detail-done',  function(event){
          event.preventDefault();

          var control_group = $(this).closest('form');
          // set values
          id = control_group.find('[name=detail-id]').val();
          name = control_group.find('[name=detail-name]').val();
          email = control_group.find('[name=detail-email]').val();

          // validate form
          valid = $('form#add-invite').parsley('validate');

          if (valid === true) {
            self.update(id, name, email);
            $('div#modal-signatory-detail"').modal('hide');
          } else {
            // allow for use cases
            if (name == '' && email == '') {
              $('div#modal-signatory-detail"').modal('hide');
            }
          }

      });

    };

    self.contact_add = function contact_add(contact_ob) {
      self.add(contact_ob.id, contact_ob.email, contact_ob.name, contact_ob.profile_picture, false);
    };

    self.load_contacts = function load_contacts(invitee_list) {
      invitee_list = $.parseJSON(invitee_list);
      if (invitee_list) {
        $.each(invitee_list, function(index, contact_ob) {
          if (contact_ob.pk && contact_ob.to_name) {
            self.add(contact_ob.pk, contact_ob.to_email, contact_ob.to_name, contact_ob.profile_picture, contact_ob.is_signed);
          };
        });
      };
    };

    self.init = function init(params) {
      self.target_element = params.target_element;
      self.urls = params.urls
      self.listen();

      // send the data to the invite widget
      $.Queue('invitee.data').publish($('script#js-invitee-list').html());

      self.render();
    };

    self.init(params);
  };
});