'use strict';

var genoBrowser = angular.module('genoBrowser', [
    'ngRoute',
    'ngResource',
    'genoBrowserControllers'
]);

genoBrowser.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        //templateUrl: 'partials/phone-list.html',
        controller: 'navMenuController'
      }).
      otherwise({
        redirectTo: '/'
      });
  }]);
