'use strict';

describe('Controller: CatalogosCtrl', function () {

  // load the controller's module
  beforeEach(module('gmmmApp'));

  var CatalogosCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    CatalogosCtrl = $controller('CatalogosCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(CatalogosCtrl.awesomeThings.length).toBe(3);
  });
});
