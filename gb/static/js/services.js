(function(){
    'use strict';

    var genoBrowserServices = angular.module('genoBrowserServices', ['ngResource']);

    genoBrowserServices.factory('PlotBounds', function(){
        var bounds = [0,-1];
        return bounds;
    });

    genoBrowserServices.factory('api', function ($http, $cookies) {
        return {
            init: function (jwt) {
                $http.defaults.headers.common['Authorization'] =
                    'Bearer ' + jwt;
            }
        };
    });

    genoBrowserServices.factory('Auth', function(){
        var token;

        return{
            setUser : function(aUser){
                user = aUser;
            },
            isLoggedIn : function(){
                return(user)? user : false;
            }
        }
    })

    genoBrowserServices.factory('Users', ['$resource',
      function($resource) {
        return $resource('/api/users/:user_id', {}, {
            update: { method:'PUT' }
        });
      }]);

    genoBrowserServices.factory('Tracks', ['$resource',
      function($resource) {
        return $resource('/api/tracks/:track_id', {track_id: '@track_id'}, {
            query: { method:'GET',
                isArray: true,
                transformResponse:[angular.fromJson, function(data){return data.tracks;}]
            },
            get: { method:'GET' },
            update: { method:'PUT' },
            save: { method: 'POST'},
            delete: {method: 'DELETE'}
        });
      }]);

    genoBrowserServices.factory('Files', ['$resource',
      function($resource) {
        return $resource('/api/files/:type/:file_id', {}, {
            query: { isArray: false },
            update: { method:'PUT' }
        });
      }]);

    genoBrowserServices.factory('Views', ['$resource',
      function($resource) {
        return $resource('/api/views/:view_id', {view_id: '@view_id'}, {
            query: { method:'GET',
                isArray: true,
                transformResponse:[angular.fromJson, function(data){return data.views;}]
            },
            get:   { method:'GET'},
            create: { method:'POST'},
            update: { method:'PUT' },
            delete: { method: 'DELETE'}
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