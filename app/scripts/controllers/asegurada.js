'use strict';

/**
 * @ngdoc function
 * @name gmmmApp.controller:AseguradactrlCtrl
 * @description
 * # AseguradactrlCtrl
 * Controller of the gmmmApp
 */
angular.module('gmmApp')
  .controller('AseguradaCtrl', function ($scope) {
  	$scope.cartera= null;
    $scope.carteraList = ['Cartera Anterior','Cartera Posterior'];
    $scope.claveTecnica = [];  
    $scope.clave = {};
    $scope.producto = [];
    $scope.plan =[];
    console.log($scope.carteraList)


    //Cambiamos la clave técnica
    $scope.$watch('cartera', function(newVal, oldVal){
    	console.log(newVal)
    	if(newVal == 'Cartera Anterior'){
    		$scope.claveTecnica = ['G0334GMMIN', 'G0334GMMII'];
    	} else{
    		if(newVal == 'Cartera Posterior'){
    			$scope.claveTecnica = ['G0334GMMIN', 'G0334GMMII', 'G0334GMINT'];
    		}
    	}
    });

    //Cambiamos el producto
    $scope.$watch('clave', function(newVal, oldVal){
    	if(newVal == 'G0334GMMIN' || newVal == 'G0334GMMIN'){

    		
    	}
    });
  });
