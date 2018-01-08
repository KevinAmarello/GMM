'use strict';

/**
 * @ngdoc function
 * @name gmmmApp.controller:CambiosctrlCtrl
 * @description
 * # CambiosctrlCtrl
 * Controller of the gmmmApp
 */
angular.module('gmmApp')
  .controller('CambiosCtrl', function ($scope, $state) {
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
    $scope.changeState = function(state){
    	switch(state) {
    		case 1:
    			$state.go('main.sumaAsegurada');
    			break;
    		case 2:
    			$state.go('main.deducible');
          break;
    		case 3:
    			$state.go('main.coaseguros');
    		case 4:
          break; 
    			$state.go('main.derechos')
    	}

    }

  });
