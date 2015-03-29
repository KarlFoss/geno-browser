'use strict';

var genoBrowserServices = angular.module('genoBrowserServices', ['ngResource']);

genoBrowserServices.factory('Users', ['$resource',
  function($resource) {
    return $resource('users/:user_id');
  }]);

genoBrowserServices.factory('Tracks', ['$resource',
  function($resource) {
    return $resource('tracks/:track_id', {}, {
      get: {
        method: 'GET',
        headers: {'X-Userid':'1'}
      },
      query: {
        method: 'GET',
        headers: {'X-Userid':'1'}
      }
    });
  }]);

genoBrowserServices.factory('Files', ['$resource',
  function($resource) {
    return $resource('files/:type/:user_id/:file_id', {}, {});
  }]);

genoBrowserServices.factory('Views', ['$resource',
  function($resource) {
    return $resource('views/:user_id/:view_id', {}, {});
  }]);