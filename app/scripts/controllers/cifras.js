'use strict';

/**
 * @ngdoc function
 * @name gmmmApp.controller:CifrasCtrl
 * @description
 * # CifrasCtrl
 * Controller of the gmmmApp
 */
angular.module('gmmApp')
  .controller('CifrasCtrl', function ($scope, cargaFactory) {
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
    $scope.cifras = {};
    $scope.notificacion = false;

    $scope.enviar = function(){
    	 var v = $scope.verify($scope.cifras);
    	 if(v){
    	 	var r = cargaFactory.cargaCifras($scope.cifras);
    	 	r.then(function(response){
    	 		console.log(response)
          $scope.notificacion = true;
    	 	}, function(err){
    	 		alert("Algo salió mal, por favor reintente")
    	 	})
    	 }
    }

    $scope.verify = function(obj){
    	var errors = 0;
    	var count = Object.keys(obj).length;
    	if(count == 22) {
	    	for(var key in obj) {
	    		if(obj.hasOwnProperty(key)){
	    			if(!isNaN(obj[key])){
	    				console.log(obj[key]);
	    			} else {
	    				errors += 1;
	    			}
	    		}
	    	}
	    	if(errors > 0) {
	    		alert('Por favor verifique que los datos que ingresó sean valores numéricos')
	    		return false;
	    	} else {
	    		return true;
	    	}
	    } else {
	    	alert('Faltan cifras, por favor verifique')
	    	return false
	    }
    }

    $scope.regresar = function() {
      $scope.notificacion = false;
    }
  });
