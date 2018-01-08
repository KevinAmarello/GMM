'use strict';

describe('Controller: CifrasCtrl', function () {

  // load the controller's module
  beforeEach(module('gmmmApp'));

  var CifrasCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    CifrasCtrl = $controller('CifrasCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(CifrasCtrl.awesomeThings.length).toBe(3);
  });
});
