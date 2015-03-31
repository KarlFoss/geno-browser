(function(){
    'use strict';

    var genoBrowserServices = angular.module('genoBrowserServices', ['ngResource']);

    genoBrowserServices.factory('Users', ['$resource',
      function($resource) {
        return $resource('/api/users/:user_id');
      }]);

    genoBrowserServices.factory('Tracks', ['$resource',
      function($resource) {
        return $resource('/api/tracks/:track_id', {}, {
            query: { isArray: false }
        });
      }]);

    genoBrowserServices.factory('Files', ['$resource',
      function($resource) {
        return $resource('/api/files/:type/:user_id/:file_id', {}, {
            query: { isArray: false }
        });
      }]);

    genoBrowserServices.factory('Views', ['$resource',
      function($resource) {
        return $resource('/api/views/:user_id/:view_id', {}, {
            query: { isArray: false }
        });
      }]);

    genoBrowserServices.factory('userService',
      function() {
        return {
          username:'',
          email:'',
          password:''
        };
      });
})();