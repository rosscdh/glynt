'use strict';
/*
Based on django-ajaxcomments, BSD licensed.
Copyright (c) 2009 Brandon Konkle and individual contributors.

Updated to be more generic, more fancy, and usable with different templates.

2013. Updated by Ross Crawford-d'Heureuse to be a jquery.plugin
*/
$(function() {
    // the widget definition, where "custom" is the namespace,
    // "colorize" the widget name
    $.widget( "django.fluent_comments", {
        // default options
        comments_container: undefined,
        submit_element: undefined,
        comment_element: undefined,
        preview_area: undefined,
        comment_waiting: undefined,

        comment_moderated_message: undefined,
        comment_added_message: undefined,

        scrollElement: $('html, body'),
        active_input: null,
        previewAutoAdded: null,
        commentBusy: false,
        options: {
            'submit_element': undefined,
            'comment_element': undefined,
            'comments_container': undefined,
            'preview_area': undefined,
            'comment_moderated_message': undefined,
            'comment_added_message': undefined,
            'comment_waiting': undefined,
            'show_preview': false,
            'is_reversed': false,
            'scroll_to_comment': true,
            'debug': true,
            'COMMENT_SCROLL_TOP_OFFSET': 100,
            'PREVIEW_SCROLL_TOP_OFFSET': 200,
        },
        _log: function (msg) {
            var self = this;
            if (self.options.debug === true) {
                console.log(msg)
            }
        },
        // the constructor
        _create: function() {
            var self = this;

            this._listen();
        },
        _listen: function () {
            var self = this;
            self.comments_container = $(self.options.comments_container || "#comments") || $("body");
            self.preview_area = $(self.options.preview_area || '#comment-preview-area') || $("body");

            self.submit_element = $(self.options.submit_element || self.element.find('input[type="submit"]:last')) || $(self.element.find('button[type="submit"]:last'));
            self.comment_element = $(self.options.comment_element || self.element.find('input#id_comment')) || $(self.element.find('textarea:last'));
            self.comment_waiting = $(self.options.comment_element || '#comment-waiting');

            self.comment_moderated_message = $(self.options.comment_moderated_message || "#comment-moderated-message");
            self.comment_added_message = $(self.options.comment_added_message || "#comment-added-message");

            self.comment_element.on( 'click focus mousedown', {'fluent_comments': self}, self.setActiveInput);
            self.submit_element.on( 'click', {'fluent_comments': self}, self.onSubmitCommentForm); // main submit event

        },
        setActiveInput: function (event) {
            this.active_input = $(event.target);
        },
        getCommentsDiv: function () {
            var self = this;
            var $comments = self.comments_container;

            if( $comments.length == 0 ) {
                self._log("Internal error - unable to display comment.\n\nreason: container is missing in the page.");
            }
            return $comments;
        },
        onSubmitCommentForm: function (event) {
            event.preventDefault();  // only after ajax call worked.
            var self = event.data.fluent_comments;
            var form = self.element;

            self.submitAjaxComment(form, {
                'fluent_comments': self,
                'onsuccess': (self.options.show_preview === true) ? null : self.onCommentPosted,
                'preview': (self.options.show_preview === true) ? 'preview' : false
            });
            return false;
        },
        submitAjaxComment: function (form, args) {
            var self = this;
            var onsuccess = args.onsuccess;
            var preview = !!args.preview;

            $('div.comment-error').remove();
            if (self.commentBusy) {
                return false;
            }

            self.commentBusy = true;

            var $form = this.element;
            var comment = $form.serialize() + (preview ? '&preview=1' : '');
            var url = $form.attr('action') || './';
            var ajaxurl = $form.attr('data-ajax-action');

            // Add a wait animation
            if( ! preview )
                self.comment_waiting.fadeIn(1000);

            // Use AJAX to post the comment.
            $.ajax({
                type: 'POST',
                url: ajaxurl || url,
                data: comment,
                dataType: 'json',
                success: function ( data ) {
                    self.commentBusy = false;

                    self.removeWaitAnimation();
                    self.removeErrors();

                    if ( data.success ) {
                        var $added;
                        if( preview )
                            $added = self.commentPreview(data);
                        else
                            $added = self.commentSuccess(data);

                        if( onsuccess )
                            args.onsuccess(data.comment_id, data.is_moderated, $added);
                    }
                    else {
                        self.commentFailure(data);
                    }
                },
                error: function ( data ) {
                    self.commentBusy = false;
                    self.removeWaitAnimation();

                    // Submit as non-ajax instead
                    //$form.unbind('submit').submit();
                },
                complete: function () {
                }
            });

            return false;
        },
        commentPreview: function (data) {
            var self = this;
            var $previewarea = this.options.preview_area || false;
            if( $previewarea === false || $previewarea.length == 0 )
            {
                // If not explicitly added to the HTML, include a previewarea in the comments.
                // This should at least give the same markup.
                getCommentsDiv().append('<div id="comment-preview-area"></div>').addClass('has-preview');
                $previewarea = $("#comment-preview-area");
                self.previewAutoAdded = true;
            }

            var had_preview = $previewarea.hasClass('has-preview-loaded');
            $previewarea.html(data.html).addClass('has-preview-loaded');

            if( ! had_preview )
                $previewarea.hide().show(600);

            // Scroll to preview, but allow time to render it.
            setTimeout(function(){ scrollToElement( $previewarea, 500, this.options.PREVIEW_SCROLL_TOP_OFFSET ); }, 500);
        },
        onCommentPosted: function ( comment_id, is_moderated, $comment ) {
            var self = this.fluent_comments;
            var $message_span;

            if( is_moderated ) {
                $message_span = self.comment_moderated_message.fadeIn(200);
            } else {
                $message_span = self.comment_added_message.fadeIn(200);
            }

            setTimeout(function(){ self.scrollToComment(comment_id, 1000); }, 1000);
            setTimeout(function(){ $message_span.fadeOut(500) }, 4000);
        },
        commentSuccess: function (data) {
            var self = this;
            // Clean form
            console.log('fds')
            self.comment_element.val('');
            // @TODO: cancelThreadedReplyForm
            //self.cancelThreadedReplyForm();  // in case threaded comments are used.

            // Show comment
            var had_preview = self.removePreview();
            var $new_comment = self.addComment(data);

            if( had_preview )
                // Avoid double jump when preview was removed. Instead refade to final comment.
                $new_comment.hide().fadeIn(600);
            else
                // Smooth introduction to the new comment.
                $new_comment.hide().show(600);

            return $new_comment;
        },
        commentFailure: function (data) {
            var self = this;
            // Show mew errors
            for (var field_name in data.errors) {
                if(field_name) {
                    var $field = $('#id_' + field_name);

                    // Twitter bootstrap style
                    $field.after('<span class="js-errors">' + data.errors[field_name] + '</span>');
                    $field.closest('.control-group').addClass('error');
                }
            }
        },
        addComment: function (data) {
            var self = this;
            // data contains the server-side response.
            var html = $(data.html) // create the domElement and thus fire appropriate events
            var parent_id = data.parent_id;

            //var $new_comment;

            // define the action by which the comment is inserted at the top of the list or the bottom
            var insert_action = (self.options.is_reversed === true) ? 'append' : 'prepend' ;

            if(parent_id)
            {
                var $parentLi = $("#c" + parseInt(parent_id)).parent('li.comment-wrapper');
                var $commentUl = $parentLi.children('ul');
                if( $commentUl.length == 0 )
                    $commentUl = $parentLi.append('<ul class="comment-list-wrapper"></ul>').children('ul.comment-list-wrapper');
                $commentUl[insert_action]('<li class="comment-wrapper">' + html.prop('outerHTML') + '</li>');
            }
            else
            {
                var $comments = self.getCommentsDiv();
                $comments[insert_action]( html.prop('outerHTML') ).removeClass( 'empty' );
            }

            return $("#c" + parseInt(data.comment_id));
        },
        scrollToComment: function (id, speed) {
            // Allow initialisation before scrolling.
            var self = this;
            var $comment = $("#c" + id);
            if( $comment.length == 0 ) {
                self._log("scrollToComment() - #c" + id + " not found.");
                return;
            }

            // Scroll to the comment.
            self.scrollToElement( $comment, speed, self.options.COMMENT_SCROLL_TOP_OFFSET );
        },
        scrollToElement: function( $element, speed, offset ) {
            var self = this;

            if( $element.length && self.options.scroll_to_comment === true )
                self.scrollElement.animate( {'scrollTop': $element.offset().top - (offset || 0) }, speed || 1000 );
        },
        removeWaitAnimation: function () {
            // Remove the wait animation and message
            this.comment_waiting.hide().stop();
        },
        removeErrors: function () {
            var self = this;
            self.element.find('.js-errors').remove();
            self.element.find('.control-group.error').removeClass('error');
        },
        removePreview: function () {
            var self = this;
            var $previewarea = self.preview_area;
            var had_preview = $previewarea.hasClass('has-preview-loaded');

            if ( self.previewAutoAdded === true ) {
                $previewarea.remove();  // make sure it's added at the end again later.
            } else {
                $previewarea.html('');
            }

            // Update classes. allowing CSS to add/remove margins for example.
            $previewarea.removeClass('has-preview-loaded')
            self.comments_container.removeClass('has-preview');

            return had_preview;
        }
    });
});
