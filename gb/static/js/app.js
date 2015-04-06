(function(){
    'use strict';

    var genoBrowser = angular.module('genoBrowser', [
        'ngRoute',
        'ngResource',
        'genoBrowserControllers',
        'genoBrowserServices',
        'nvd3ChartDirectives'
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
