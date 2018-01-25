'use strict';

describe('Controller: DescargatablasCtrl', function () {

  // load the controller's module
  beforeEach(module('gmmmApp'));

  var DescargatablasCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    DescargatablasCtrl = $controller('DescargatablasCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(DescargatablasCtrl.awesomeThings.length).toBe(3);
  });
});
