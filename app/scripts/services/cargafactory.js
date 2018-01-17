'use strict';

/**
 * @ngdoc service
 * @name gmmmApp.cargaFactory
 * @description
 * # cargaFactory
 * Factory in the gmmmApp.
 */
angular.module('gmmApp')
  .factory('cargaFactory', function (Restangular, $http) {
    // Service logic
    // ...

    var meaningOfLife = 42;

    // Public API here
    return {
      cargaInicial: function (id) {
        var fd = new FormData();
        console.log(document.getElementById(id).files[0])
        fd.append('file', document.getElementById(id).files[0]);
        //for (var key of fd.entries()) {
        //console.log(key[0] + ', ' + key[1]);
    //}
        //console.log(fd.file)
        return Restangular.one('uploadPBA').withHttpConfig({transformRequest: angular.identity})
        .customPOST(fd, '', undefined, {'Content-Type': undefined})
      },
      cargaCifras: function(cifras) {
        return Restangular.all('uploadCC').withHttpConfig({timeout: 60000}).post(cifras);
      },
      cargaCatalogo: function (id) {
        var fd = new FormData();
        console.log(document.getElementById(id).files[0])
        fd.append('file', document.getElementById(id).files[0]);
        //for (var key of fd.entries()) {
        //console.log(key[0] + ', ' + key[1]);
    //}
        //console.log(fd.file)
        return Restangular.one('uploadCatalog').withHttpConfig({transformRequest: angular.identity})
        .customPOST(fd, '', undefined, {'Content-Type': undefined})
      }

    };
  });
