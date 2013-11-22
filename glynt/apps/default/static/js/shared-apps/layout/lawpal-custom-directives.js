

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

			scope.open = function() {
				ctrl.toggleLockBlock(index, false);
				scope.isCollapsed = false;
                setTimeout( function(){
                	scope.$apply();
                    adjustScollPos($(".options-container .item-container"));
                },100);
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
				if(scope.isCollapsed === false) {
					if( idx === index ) {
						ctrl.toggleLockBlock(index, false);
						scope.isCollapsed = true;
						setTimeout(
							function() {
								scope.open();
							},
							1000
						);
					}
				} else {
					if( idx === index ) {
						scope.open();
						
					}
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
				var d = element;
				if(scope.isCollapsed===false) {
					var c = $(window).scrollTop() - 20;
                    var w = $(window).height();
                    var dh = $(document).height();
					var wd = d.height() + 20 - w;
                    var eh = d.innerHeight() - 400;
					var top = 20;
                    var scrollerInc = (scrollerTopMargin+20)/dh;

					if( c > scrollerTopMargin && c <= (dh - w - 100)) {
                        var diff = ((eh/dh) * c);
                        d.css({ 'position': "fixed", 'top': -diff + "px"   });
                    } else if( c > (dh - w - 100) && c <= (dh - w - 50) ) {
                    	var diff = ((eh/dh) * c * 1.15);
                    	d.css({ 'position': "fixed", 'top': -diff + "px"   });
                   	} else if( c > (dh - w - 60) ) {
                    	var diff = ((eh/dh) * c * 1.3);
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