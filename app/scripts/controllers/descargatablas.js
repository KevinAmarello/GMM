'use strict';

/**
 * @ngdoc function
 * @name gmmmApp.controller:DescargatablasCtrl
 * @description
 * # DescargatablasCtrl
 * Controller of the gmmmApp
 */
angular.module('gmmApp')
  .controller('DescargatablasCtrl', function ($scope, cargaFactory) {
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
    $scope.mensaje = false;
    $scope.loading = false;

    $scope.descargaTablas  = function() {
    	$scope.loading = true
    	var r = cargaFactory.descargaTablas();
    	r.then(function(response) {
    		$scope.mensaje = true;
    		$scope.loading = false;
    	})
    }

    $scope.regresar = function() {
    	$scope.mensaje =  false;
    }

  });
