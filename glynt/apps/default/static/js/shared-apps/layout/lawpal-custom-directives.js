

/* Custom directives for block flexy-layout */
angular.module('lawpal').directive('collapse', function () {
    return {
        require: '^flexyLayout',
        replace: true,
        scope: {},
        template: '<div><span ng-class="{collapse:isCollapsed}" ng-click="toggle()">< ></span></div>',
        restrict: 'E',
        link: function (scope, element, attr, ctrl) {

            var index = parseInt(attr.index,10),
                minWidth = attr.minWidth || 35,
                maxWidth = attr.maxWidth || 350;

            scope.isCollapsed = true;
            scope.toggle = function () {
                ctrl.toggleLockBlock(index, false);
                scope.isCollapsed = scope.isCollapsed !== true;
            };

            scope.$watch('isCollapsed', function (newValue, oldValue) {
                if (newValue !== oldValue) {
                    var newLength = newValue === true ? minWidth - element.parent()[0].offsetWidth : maxWidth - element.parent()[0].offsetWidth;
                    ctrl.moveBlockLength(index, newLength);
                    ctrl.toggleLockBlock(index, true);
                }
            });

            //scope.isCollapsed = attr.collapsed || false;

            scope.$on('toggle-collapse', function( evt, idx ) {
            	if( idx === index ) {
            		scope.toggle();
            	}
            });

            scope.$on('open-sidebar', function( evt, idx ) {
            	if( idx === index ) {
            		ctrl.toggleLockBlock(index, false);
            		scope.isCollapsed = false;
            	}
            });

            scope.$on('close-sidebar', function( evt, idx ) {
            	if( idx === index ) {
            		ctrl.toggleLockBlock(index, false);
            		scope.isCollapsed = true;
            	}
            });

            var scrollerTopMargin = $(".options-container").offset().top;
			$(window).scroll(function(){
			    var c = $(window).scrollTop() - 50;
			    var d = $(".options-container");
			    if (c > scrollerTopMargin) {
			        d.css({ position: "fixed", top: "50px"   });
			    }
			    else if (c <= scrollerTopMargin) 
			    {
			        d.css({ position: "absolute", top: ""   });
			    }
			});
        }
    };
});