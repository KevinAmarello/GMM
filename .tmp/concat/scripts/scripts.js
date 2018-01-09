'use strict';

/**
 * @ngdoc overview
 * @name gmmmApp
 * @description
 * # gmmmApp
 *
 * Main module of the application.
 */
angular
  .module('gmmApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'ui.router',
    'restangular',
    'file-model'
  ])
  .config(["$routeProvider", "$stateProvider", "$urlRouterProvider", "RestangularProvider", function ($routeProvider, $stateProvider, $urlRouterProvider, RestangularProvider) {
    RestangularProvider.setBaseUrl('https://frontend-dot-gnp-auttarifasgmm-qa.appspot.com');
    $urlRouterProvider.otherwise('/archivo');
    $stateProvider
    .state('main', {
      url: '/',
      views: {
        '':{
          templateUrl: 'views/content.html'
        },
        'header@main': {
          templateUrl: 'views/header.html',
          controller: 'HeaderCtrl'
        },
        /*'main@main': {
          templateUrl: 'views/main.html'
        },*/
        'footer@main': {
          templateUrl: 'views/footer.html'
        }
      }

    })
    .state('main.archivo', {
      url:'archivo',
      views: {
        'main@main': {
         templateUrl: 'views/menu_principal.html',
         controller: 'MenuCtrl'
        }
      }
    })
    .state('main.cifras', {
      url:'cifras',
      views: {
        'main@main': {
          templateUrl:'views/ccontrl.html',
          controller: 'CifrasCtrl'
        }
      }
    });
  }]);

'use strict';

/**
 * @ngdoc function
 * @name gmmmApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the gmmmApp
 */
angular.module('gmmApp').controller('MainCtrl', ["$scope", "cargaFactory", function ($scope, cargaFactory) {
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
  }])
   

'use strict';

/**
 * @ngdoc function
 * @name gmmmApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the gmmmApp
 */
angular.module('gmmApp')
  .controller('AboutCtrl', function () {
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });

'use strict';

/**
 * @ngdoc service
 * @name gmmmApp.cargaFactory
 * @description
 * # cargaFactory
 * Factory in the gmmmApp.
 */
angular.module('gmmApp')
  .factory('cargaFactory', ["Restangular", "$http", function (Restangular, $http) {
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
      }

    };
  }]);

'use strict';

/**
 * @ngdoc function
 * @name gmmmApp.controller:CambiosctrlCtrl
 * @description
 * # CambiosctrlCtrl
 * Controller of the gmmmApp
 */
angular.module('gmmApp')
  .controller('CambiosCtrl', ["$scope", "$state", function ($scope, $state) {
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

  }]);

'use strict';

/**
 * @ngdoc function
 * @name gmmmApp.controller:MenuctrlCtrl
 * @description
 * # MenuctrlCtrl
 * Controller of the gmmmApp
 */
angular.module('gmmApp')
  .controller('MenuCtrl', ["$scope", "$state", "cargaFactory", function ($scope, $state, cargaFactory) {
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
  }]);

'use strict';

/**
 * @ngdoc function
 * @name gmmmApp.controller:AseguradactrlCtrl
 * @description
 * # AseguradactrlCtrl
 * Controller of the gmmmApp
 */
angular.module('gmmApp')
  .controller('AseguradaCtrl', ["$scope", function ($scope) {
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
  }]);

'use strict';

/**
 * @ngdoc directive
 * @name gmmmApp.directive:customOnChange
 * @description
 * # customOnChange
 */
angular.module('gmmApp')
  .directive('customOnChange', function () {
    return {
      	restrict: 'A',
		link: function (scope, element, attrs) {
			var onChangeHandler = scope.$eval(attrs.customOnChange);
			element.on('change', onChangeHandler);
			element.on('$destroy', function() {
				element.off();
			});

	    }
	}
  });

'use strict';

/**
 * @ngdoc function
 * @name gmmmApp.controller:CifrasCtrl
 * @description
 * # CifrasCtrl
 * Controller of the gmmmApp
 */
angular.module('gmmApp')
  .controller('CifrasCtrl', ["$scope", "cargaFactory", function ($scope, cargaFactory) {
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
  }]);

'use strict';

/**
 * @ngdoc function
 * @name gmmmApp.controller:CatalogosCtrl
 * @description
 * # CatalogosCtrl
 * Controller of the gmmmApp
 */
angular.module('gmmApp')
  .controller('CatalogosCtrl', function () {
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });

'use strict';

/**
 * @ngdoc function
 * @name gmmmApp.controller:HeaderCtrl
 * @description
 * # HeaderCtrl
 * Controller of the gmmmApp
 */
angular.module('gmmApp')
  .controller('HeaderCtrl', ["$scope", "$state", function ($scope, $state) {
    $scope.goTo = function(index){
    	switch(index) {
    		case 1:
    			$state.go('main.archivo');
    			break;
    		case 2:
    			$state.go('main.cifras');
    	}
    }
  }]);

'use strict';

/**
 * @ngdoc function
 * @name gmmmApp.controller:CatalogoCtrl
 * @description
 * # CatalogoCtrl
 * Controller of the gmmmApp
 */
angular.module('gmmApp')
  .controller('CatalogoCtrl', function () {
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });

angular.module('gmmApp').run(['$templateCache', function($templateCache) {
  'use strict';

  $templateCache.put('views/catalogos.html',
    "<div class=\"container-fluid nopadding\"> <div class=\"row\"> <div class=\"container content\"> <div class=\"col-lg-12 col-md-12 col-sm-12 col-xs-12 header-box\"> <h3>Carga de Catálogos</h3> </div> <div ng-hide=\"notificacion\"> <div class=\"col-lg-6 col-lg-offset-3 col-md-6 col-md-offset-3 col-sm-6 col-sm-offset-3 col-xs-12 col-xs-offset-0 input-file\"> <div class=\"form-group\"> <label for=\"exampleInputFile\">Seleccione el archivo que desea cargar.</label> <input type=\"file\" id=\"exampleInputFile\" file-model=\"input\"> </div> </div> <div class=\"col-lg-12 col-md-12 col-sm-12 col-xs-12\"> <div class=\"col-lg-6 col-lg-offset-3 col-md-6 col-md-offset-3 col-sm-8 col-sm-offset-2 col-xs-12 col-xs-offset-0 send-btn\"> <button type=\"submit\" ng-click=\"send()\"> CARGAR ARCHIVO</button> </div> </div> </div> <div ng-show=\"notificacion\"> <div class=\"col-lg-6 col-lg-offset-3 col-md-6 col-md-offset-3 col-sm-6 col-sm-offset-3 col-xs-12 col-xs-offset-0 input-file\"> <div class=\"form-group\"> <label for=\"exampleInputFile\">El proceso ha iniciado, pronto recibirá una notificación.</label> </div> </div> <div class=\"col-lg-12 col-md-12 col-sm-12 col-xs-12\"> <div class=\"col-lg-6 col-lg-offset-3 col-md-6 col-md-offset-3 col-sm-8 col-sm-offset-2 col-xs-12 col-xs-offset-0 send-btn\"> <button type=\"submit\" ng-click=\"regresar()\"> Regresar</button> </div> </div> </div> </div> </div> </div>"
  );


  $templateCache.put('views/ccontrl.html',
    "<div class=\"container-fluid nopadding\"> <div class=\"row\"> <div class=\"container content\"> <div class=\"col-lg-12 col-md-12 col-sm-12 col-xs-12 header-box\"> <h3>Carga de Cifras de Control</h3> </div> <div class=\"col-lg-6\" ng-hide=\"notificacion\"> <div class=\"container-fluid nopadding\"> <div class=\"row\"> <div class=\"container content\"> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPT8AT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPT8AT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTDGT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTDGT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTDIT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTDIT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTDMT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTDMT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTBCT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTBCT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTCLT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTCLT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTAST </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTAST\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTDLT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTDLT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KAPTPAT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KAPTPAT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPT8LT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPT8LT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTBQT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTBQT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTCKT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTCKT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPT8BT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPT8BT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTDJT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTDJT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTDNT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTDNT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTCNT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTCNT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTCOT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTCOT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTCPT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTCPT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTDFT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTDFT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPT6WT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPT6WT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTDOT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTDOT\"> </div> </div> <div class=\"col-xs-12 row-input\"> <div class=\"col-lg-offset-2 col-lg-1\"> KTPTCQT </div> <div class=\"col-lg-6 input\"> <input type=\"text\" ng-model=\"cifras.KTPTCQT\"> </div> </div> <div class=\"col-xs-12 row-submit nopadding\"> <div class=\"col-lg-offset-3 col-lg-6\"> <button ng-click=\"enviar()\">Guardar</button> </div> </div> </div> </div> </div> </div> <div ng-show=\"notificacion\"> <div class=\"col-lg-6 col-lg-offset-3 col-md-6 col-md-offset-3 col-sm-6 col-sm-offset-3 col-xs-12 col-xs-offset-0 input-file\"> <div class=\"form-group\"> <label for=\"exampleInputFile\">Proceso Finalizado</label> </div> </div> <div class=\"col-lg-12 col-md-12 col-sm-12 col-xs-12\"> <div class=\"col-lg-6 col-lg-offset-3 col-md-6 col-md-offset-3 col-sm-8 col-sm-offset-2 col-xs-12 col-xs-offset-0 send-btn\"> <button type=\"submit\" ng-click=\"regresar()\"> Regresar</button> </div> </div> </div> </div> </div> </div>"
  );


  $templateCache.put('views/content.html',
    "<div class=\"container\"> <div ui-view=\"header\"></div> <div ui-view=\"main\"></div> <div ui-view=\"footer\"></div> </div>"
  );


  $templateCache.put('views/derechos.html',
    "<div class=\"archivo mod\"> <a href=\"archivo.html\"><img class=\"back-arrow\" src=\"img/arrow-back.svg\"></a> <img src=\"img/file.svg\"> <h3><b>Archivo 1</b></h3> <p>Modificacion 4</p> <div class=\"modificaciones\"> <div class=\"ajustes\"> <select> <option>opcion 1</option> </select> <select> <option>opcion 2</option> </select> <select> <option>opcion 3</option> </select> <input type=\"text\" name=\"input\" placeholder=\"Escribe algo\"> </div> <div class=\"btn\"> <button>Guardar</button> </div> </div> </div>"
  );


  $templateCache.put('views/footer.html',
    "<!-- \n" +
    " <div class=\"footer\">\n" +
    "      <div class=\"container\">\n" +
    "        <p><span class=\"glyphicon glyphicon-heart\"></span> from the Yeoman team</p>\n" +
    "      </div>\n" +
    "    </div>\n" +
    "-->"
  );


  $templateCache.put('views/header.html',
    "<div class=\"container-fluid nopadding\"> <div class=\"row\"> <div class=\"container\"> <div class=\"col-lg-9 col-md-9 col-sm-9 col-xs-9 nav-bar\"> <ul> <li><a ng-click=\"\">Descarga de Archivo</a></li> <li><a ng-click=\"\">Carga de Cat&aacute;logos</a></li> <li><a ng-click=\"goTo(2)\">Carga de Cifras de Control</a></li> <li><a ng-click=\"goTo(1)\">Carga de Tablas</a></li> </ul> </div> </div> </div> </div>"
  );


  $templateCache.put('views/menu_principal.html',
    "<div class=\"container-fluid nopadding\"> <div class=\"row\"> <div class=\"container content\"> <div class=\"col-lg-12 col-md-12 col-sm-12 col-xs-12 header-box\"> <h3>Carga de Archivo de Tablas</h3> </div> <div ng-hide=\"notificacion\"> <div class=\"col-lg-6 col-lg-offset-3 col-md-6 col-md-offset-3 col-sm-6 col-sm-offset-3 col-xs-12 col-xs-offset-0 input-file\"> <div class=\"form-group\"> <label for=\"exampleInputFile\">Seleccione el archivo que desea cargar.</label> <input type=\"file\" id=\"exampleInputFile\" file-model=\"input\"> </div> </div> <div class=\"col-lg-12 col-md-12 col-sm-12 col-xs-12\"> <div class=\"col-lg-6 col-lg-offset-3 col-md-6 col-md-offset-3 col-sm-8 col-sm-offset-2 col-xs-12 col-xs-offset-0 send-btn\"> <button type=\"submit\" ng-click=\"send()\"> CARGAR ARCHIVO</button> </div> </div> </div> <div ng-show=\"notificacion\"> <div class=\"col-lg-6 col-lg-offset-3 col-md-6 col-md-offset-3 col-sm-6 col-sm-offset-3 col-xs-12 col-xs-offset-0 input-file\"> <div class=\"form-group\"> <label for=\"exampleInputFile\">El proceso ha iniciado, pronto recibirá una notificación.</label> </div> </div> <div class=\"col-lg-12 col-md-12 col-sm-12 col-xs-12\"> <div class=\"col-lg-6 col-lg-offset-3 col-md-6 col-md-offset-3 col-sm-8 col-sm-offset-2 col-xs-12 col-xs-offset-0 send-btn\"> <button type=\"submit\" ng-click=\"regresar()\"> Regresar</button> </div> </div> </div> </div> </div> </div>"
  );

}]);
