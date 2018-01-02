'use strict';

describe('Controller: AseguradactrlCtrl', function () {

  // load the controller's module
  beforeEach(module('gmmmApp'));

  var AseguradactrlCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    AseguradactrlCtrl = $controller('AseguradactrlCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(AseguradactrlCtrl.awesomeThings.length).toBe(3);
  });
});
