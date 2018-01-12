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
    $scope.loading = false;
    $scope.alert = false;
    $scope.mensaje = "";
    $scope.mensajes = ["Algo salió mal, por favor reintente", 
                       "Por favor verifique que el archivo sea de extensión .xlsx ó .xls", 
                       "Por favor ingrese un archivo"];

    $scope.send = function() {
      $scope.alert = false;
      $scope.mensaje="";
      console.log($scope.input);
      if($scope.input){
        $scope.loading = true;
        var bool = $scope.verifyExt($scope.input);
        if(bool) {
          var r = cargaFactory.cargaInicial("exampleInputFile");
          r.then(function(response){
            console.log(response);
            $scope.loading = false;
            $scope.notificacion = true;
          }, function(err){
            $scope.alert = true;
            $scope.mensaje = $scope.mensajes[0];
            $scope.loading = false;
            //alert("Algo salió mal, por favor reintente en un momento")
          }); 
        } else {
          $scope.alert = true;
          $scope.mensaje = $scope.mensajes[1];
          $scope.loading = false;
          //alert("Por favor verifique que el archivo sea de extensión .xlsx ó .xls")
        }
      } else {
        $scope.alert = true;
        $scope.mensaje = $scope.mensajes[2];
        $scope.loading = false;
        //alert("Por favor ingrese un archivo")
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

    $scope.$watch('input', function(){
      $scope.alert = false;
      $scope.mensaje = "";
    })
  });
