'use strict';

describe('Controller: CambiosctrlCtrl', function () {

  // load the controller's module
  beforeEach(module('gmmmApp'));

  var CambiosctrlCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    CambiosctrlCtrl = $controller('CambiosctrlCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(CambiosctrlCtrl.awesomeThings.length).toBe(3);
  });
});
