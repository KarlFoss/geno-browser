'use strict';

var genoBrowserServices = angular.module('genoBrowserServices', ['ngResource']);

genoBrowserServices.factory('Users', ['$resource',
  function($resource){
    return $resource('users/:id');
  }]);

genoBrowserServices.factory('Tracks', ['$resource',
  function($resource){
    return $resource('tracks/:id', {}, {
      get: {
        method:'GET',
        isArray:false,
        headers: {'X-Userid':'1'}
      }
    });
  }]);