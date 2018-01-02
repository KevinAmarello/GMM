'use strict';

/**
 * @ngdoc directive
 * @name gmmmApp.directive:customOnChange
 * @description
 * # customOnChange
 */
angular.module('gmmApp')
  .directive('customOnChange', function () {
    return {
      	restrict: 'A',
		link: function (scope, element, attrs) {
			var onChangeHandler = scope.$eval(attrs.customOnChange);
			element.on('change', onChangeHandler);
			element.on('$destroy', function() {
				element.off();
			});

	    }
	}
  });
