

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
					adjustScollPos($(".options-container .item-container"));
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
                    setTimeout( function(){
                        adjustScollPos($(".options-container .item-container"));
                    },100);
					
				}
			});

			scope.$on('close-sidebar', function( evt, idx ) {
				if( idx === index ) {
					ctrl.toggleLockBlock(index, false);
					scope.isCollapsed = true;
				}
			});

			scope.$on('adjust-sidebar', function( evt, idx ) {
				adjustScollPos($(".options-container .item-container"));
			});

			function adjustScollPos( element ) {
                console.log('adjusting');
				var d = element;
				if(scope.isCollapsed===false) {
					var c = $(window).scrollTop() - 50;
                    var w = $(window).height();
                    var dh = $(document).height();
					var wd = d.height() + 50 - w;
                    var eh = d.innerHeight() - 400;
					var top = 50;
                    var scrollerInc = (scrollerTopMargin+50)/dh;

					if( c > scrollerTopMargin) {
                        var diff = ((eh/dh) * c);
                        console.log("wd",w,eh, eh/dh, (c-scrollerTopMargin), diff);
                        d.css({ 'position': "fixed", 'top': -diff + "px"   });
                    } else {
                        d.css({ 'position': "relative", 'top': ""   });
                    }
				} else {
					d.css({ 'position': "relative", 'top': ""   });
				}
			}
			

			var scrollerTopMargin = $(".options-container").offset().top;

			$(window).scroll(function(){
				adjustScollPos($(".options-container .item-container"));
			});			
		}
	};
});