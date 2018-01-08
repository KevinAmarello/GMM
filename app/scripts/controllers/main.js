'use strict';

/**
 * @ngdoc function
 * @name gmmmApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the gmmmApp
 */
angular.module('gmmApp').controller('MainCtrl', function ($scope, cargaFactory) {
    $scope.loading = false;
    $scope.makingRequest = false;

    //subida inicial del archivo
    $scope.uploadFile = function(file){
      //Cambiamos banderas para saber si hay algun archivo en proceso
      // & el logo de espera.
      $scope.makingRequest = true;
      $scope.loading = true;
      var request = cargaFactory.cargaInicial("xlf");
      request.then(function(response){
        console.log(response);
        $scope.$apply(function(){
            //Apagamos banderas
            $scope.loading = false;
            $scope.makingRequest = false
        });
      })
    }
  })
   
