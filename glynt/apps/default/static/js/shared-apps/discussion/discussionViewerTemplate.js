/**
 * Discussion list template
 * used in conjuction with 'discussionListDirective.js'
 */
angular.module('lawpal').run(["$templateCache", function($templateCache) {
    'use strict';
    $templateCache.put("template/lawpal/discussion/viewConversation.html",
        '<div class="full-dialog-container">' +
        '<div ng-animate="\'animateToaster\'" ng-repeat="discussion in discussions">\n' +
        '<div class="full-dialog-underlay"></div>' +
        // Start: Dialog
        '<div class="full-dialog">' +
        '<div class="container full-dialog-content">\n' +
        '  <div class="row"><div class="col-lg-10"><button class="close" ng-click="close()">&times</button></div></div>'+
        '  <div class="row" ng-show="discussion.original.title"><div class="col-lg-5 col-offset-2"><h3 ng-bind="discussion.original.title"></h3></div></div>'+
        // Reply
        '  <div class="row clearfix">\n'+
        '    <div class="col-lg-8 col-offset-2">\n' +
        '           <form class="form-discussion" ng-submit="reply(discussion.original)">\n'+
        '               <div class="form-group">\n'+
        '                   <label for="discussionComment" class="sr-only hide">Message</label>\n'+
        '                   <textarea placeholder="Your response" id="discussionComment" name="discussionComment" required="true" ng-model="message.comment" class="form-control" rows="3" style="max-width:100%;"></textarea>\n'+
        '               </div>\n'+
        '               <button class="btn btn-info pull-right" type="submit"><i class="icon icon-reply"></i> Respond</button>\n'+
        '           </form>\n'+
        '    </div>\n'+
        ' </div>\n'+
        // Reply
        '  <div class="row clearfix" ng-repeat="reply in replies | orderBy:\'meta.timestamp\':true">\n'+
        // Start: avatar column
        '    <div class="col-lg-2 col-offset-2">\n' +
        '       <div class="fn fn-lg clearfix" user-mini-widget user="reply.meta.user" data-show-props="photo,name"></div>\n' +
        '       <div class="time text-muted">\n' +
        /*'          <i class="icon icon-time"></i>\n' +*/
        '          <small ng-bind="reply.meta.timestamp | timeAgo"></small>\n' +
        '       </div>\n' +
        '    </div>\n' +
        // End: avatar column
        '    <div class="col-lg-6">\n' +
        '       <div class="comment" ng-bind-html-unsafe="reply.comment | plainTextToParagraphs"></div>\n' +
        '    </div>\n' +
        // End: comment column
        '  </div>\n'+
        '  <div class="row clearfix">\n' +
        // Start: avatar column
        '    <div class="col-lg-2 col-offset-2">\n' +
        '       <div class="fn fn-lg clearfix" user-mini-widget user="discussion.original.meta.user" data-show-props="photo,name"></div>\n' +
        '       <div class="time text-muted">\n' +
        /*'          <i class="icon icon-time"></i>\n' +*/
        '          <small ng-bind="discussion.original.meta.timestamp | timeAgo"></small>\n' +
        '       </div>\n' +
        '    </div>\n' +
        // End: avatar column
        '    <div class="col-lg-6">\n' +
        '       <div class="comment" ng-bind-html-unsafe="discussion.original.comment | plainTextToParagraphs"></div>\n' +
        '    </div>\n' +
        // End: comment column
        '  </div>\n' + // .row
        '</div>\n' + // .full-dialog-container
        '</div>' + // .full-dialog
      // End: Dialog
        '<div class="full-dialog-toolbar">\n' +
        '   <div class="container">\n' +
        '       <div class="col-lg-10">\n' +
        '         <button class="btn btn-primary pull-right" ng-click="close()"><i class="icon icon-remove"></i> Close</button>\n' +
        '       </div>\n' +
        '   </div>\n' +
        '</div>\n' +
        '</div>' +
        '</div>'
    );
}]);