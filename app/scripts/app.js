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
  .config(function ($routeProvider, $stateProvider, $urlRouterProvider, RestangularProvider) {
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
          templateUrl: 'views/header.html'
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
  });
