(function(){
    'use strict';

    var genoBrowserServices = angular.module('genoBrowserServices', ['ngResource']);

    genoBrowserServices.factory('PlotBounds', function(){
        var bounds = [0,-1];
        return bounds;
    });

    genoBrowserServices.factory('AppAlert', ['$rootScope',
        function($rootScope) {
            var alertService;
            $rootScope.alerts = [];
            return alertService = {
                add: function(type, msg) {
                    return $rootScope.alerts.push({
                        type: type,
                        msg: msg,
                        close: function() {
                            return alertService.closeAlert(this);
                        }
                    });
                },
                closeAlert: function(alert) {
                    return this.closeAlertIdx($rootScope.alerts.indexOf(alert));
                },
                closeAlertIdx: function(index) {
                    return $rootScope.alerts.splice(index, 1);
                }
            };
        }]);

    genoBrowserServices.factory('API', ['$resource',
        function($resource) {
            return $resource('/api/auth', {}, {
                authenticate: { method:'POST' }
            });
        }]);

    genoBrowserServices.factory('Users', ['$resource',
      function($resource) {
        return $resource('/api/users/:user_id', {}, {
            get: { method:'GET' },
            update: { method:'PUT' },
            save: { method: 'POST' },
            delete: { method: 'DELETE' }
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

/*    genoBrowserServices.factory('DataTracks', ['$resource',
      function($resource) {
        return $resource('/api/tracks/data/:track_id', {}, {
          query: { isArray: false }
        });
      }]);*/

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

      genoBrowserServices.factory('DataViews', ['$resource',
      function($resource) {
        return $resource('/api/views/data/:view_id', {view_id: '@view_id'}, {
            query: { method:'GET',
                isArray: true,
                transformResponse:[angular.fromJson, function(data){return data.view_tracks;}]
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