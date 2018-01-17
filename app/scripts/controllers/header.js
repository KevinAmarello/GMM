'use strict';

/**
 * @ngdoc function
 * @name gmmmApp.controller:HeaderCtrl
 * @description
 * # HeaderCtrl
 * Controller of the gmmmApp
 */
angular.module('gmmApp')
  .controller('HeaderCtrl', function ($scope, $state) {
    $scope.goTo = function(index){
    	switch(index) {
    		case 1:
    			$state.go('main.archivo');
    			break;
    		case 2:
    			$state.go('main.cifras');
    			break;
    		case 3:
    			$state.go('main.catalogos');
    			break;
    	}
    }
  });
