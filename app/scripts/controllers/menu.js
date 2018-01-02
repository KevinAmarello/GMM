'use strict';

/**
 * @ngdoc function
 * @name gmmmApp.controller:MenuctrlCtrl
 * @description
 * # MenuctrlCtrl
 * Controller of the gmmmApp
 */
angular.module('gmmApp')
  .controller('MenuCtrl', function ($scope, $state, cargaFactory) {
    $scope.notificacion = false;

    $scope.send = function() {
      console.log($scope.input);
      if($scope.input){
        var bool = $scope.verifyExt($scope.input);
        if(bool) {
          var r = cargaFactory.cargaInicial("exampleInputFile");
          r.then(function(response){
            console.log(response);
            $scope.notificacion = true;
          }, function(err){
            alert("Algo salió mal, por favor reintente en un momento")
          }); 
        } else {
          alert("Por favor verifique que el archivo sea de extensión .xlsx ó .xls")
        }
      } else {
        alert("Por favor ingrese un archivo")
      }
    }

    $scope.verifyExt = function(sender) {
      var validExts = new Array(".xlsx", ".xls");
      var fileExt = sender.name;
      console.log(fileExt)
      fileExt = fileExt.substring(fileExt.lastIndexOf('.'));
      if (validExts.indexOf(fileExt) < 0) {
        return false;
      }
      else return true;
    }

    $scope.regresar = function() {
      $scope.notificacion = false;
    }
  });
