'use strict';

describe('Service: cargaFactory', function () {

  // load the service's module
  beforeEach(module('gmmmApp'));

  // instantiate service
  var cargaFactory;
  beforeEach(inject(function (_cargaFactory_) {
    cargaFactory = _cargaFactory_;
  }));

  it('should do something', function () {
    expect(!!cargaFactory).toBe(true);
  });

});
