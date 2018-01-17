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
    $scope.loading = false;
    $scope.alert = false;
    $scope.mensaje = "";
    $scope.mensajes = ["Algo salió mal, por favor reintente", 
                       'Por favor verifique que los datos que ingresó sean valores numéricos', 
                       'Faltan cifras, por favor verifique'];
    
    $scope.enviar = function(){
    	 var v = $scope.verify($scope.cifras);
    	 if(v){
    	 	var r = cargaFactory.cargaCifras($scope.cifras);
    	 	r.then(function(response){
    	 		//console.log(response)
          $scope.loading = false;
          $scope.notificacion = true;
    	 	}, function(err){
          $scope.mensaje = $scope.mensajes[0];
          $scope.alert = true;
          $scope.loading = false;
    	 		//alert("Algo salió mal, por favor reintente")
    	 	})
    	 }
    }

    $scope.verify = function(obj){
      $scope.loading = true;
    	var errors = 0;
    	var count = 0; //Object.keys(obj).length;
      for(var k in obj) {
        if(obj.hasOwnProperty(k)) {
          //console.log(obj[k].length)  
          if(obj[k].length > 0) {
            count += 1;
          }
        }
      }
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
          $scope.loading = false;
          $scope.mensaje = $scope.mensajes[1];
          $scope.alert = true;
          //alert('Por favor verifique que los datos que ingresó sean valores numéricos');
	    		return false;
	    	} else {
	    		return true;
	    	}
	    } else {
        //console.log("Hellooooo")
        $scope.loading = false;
        $scope.mensaje = $scope.mensajes[2];
        $scope.alert = true;
	    	//alert('Faltan cifras, por favor verifique')
	    	return false
	    }
    }

    $scope.regresar = function() {
      $scope.notificacion = false;
    }

    $scope.changeMessage = function(){
      $scope.alert = false;
      $scope.mesaje ="";
    }
  });
