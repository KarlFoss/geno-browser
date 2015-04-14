(function(){
    'use strict';

    var genoBrowserServices = angular.module('genoBrowserServices', ['ngResource']);

    genoBrowserServices.factory('PlotBounds', function(){
        var bounds = [0,-1];
        return bounds;
    });

    genoBrowserServices.factory('Token', ['$resource',
        function($resource) {
            return function(username, password) {
                return $resource('/api/token/', {}, {
                    get: {
                        headers: {
                            'username': username,
                            'password': password
                        }
                    }
                });
            };
        }]);

    genoBrowserServices.factory('Users', ['$resource',
      function($resource) {
        return $resource('/api/users/:user_id', {}, {});
      }]);

    genoBrowserServices.factory('Tracks', ['$resource',
      function($resource) {
        return $resource('/api/tracks/2', {}, {
            query: { isArray: false }
        });
      }]);

    genoBrowserServices.factory('DataTracks', ['$resource',
      function($resource) {
        return $resource('/api/tracks/data/:track_id', {}, {
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