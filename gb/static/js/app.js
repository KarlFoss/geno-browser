(function(){
    'use strict';

    var genoBrowser = angular.module('genoBrowser', [
        'ngRoute',
        'ngResource',
        'genoBrowserConstants',
        'genoBrowserControllers',
        'genoBrowserServices'
    ]);

    /*
    genoBrowser.config(['$routeProvider',
      function($routeProvider) {
        $routeProvider.
          when('/', {
            controller: 'navMenuController'
          }).
          otherwise({
            redirectTo: '/'
          });
      }]);
      */
})();
