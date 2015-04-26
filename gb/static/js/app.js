(function(){
    'use strict';

    var genoBrowser = angular.module('genoBrowser', [
        'ngRoute',
        'ngResource',
        'genoBrowserControllers',
        'genoBrowserServices',
        'nvd3ChartDirectives',
        'genoBrowserDirectives'
    ]);

    genoBrowser.config(['$routeProvider',
        function($routeProvider) {
            $routeProvider.
                when('/view/:viewId', {
                    templateUrl: 'partials/view-frame.html',
                    resolve:{'$routeParams':'$routeParams','Views':'Views'},
                    controller: /*function($routeParams, Views){
                        this.view_id = $routeParams.viewId;
                        this.view = Views.get({view_id:this.view_id});
                    },*/ 'ViewController',
                    controllerAs:'view'
                }).
                otherwise({
                    redirectTo: '/'
                });
        }]);

    genoBrowser.factory('authInterceptor', function ($rootScope, $q, $window) {
        return {
            request: function (config) {
                config.headers = config.headers || {};
                if ($window.sessionStorage.token) {
                    config.headers.Authorization = 'Bearer ' + $window.sessionStorage.token;
                }

                return config;
            },
            responseError: function (response) {
                if (response.status === 401 || response.status === 403) {
                    delete $window.sessionStorage.token;
                }

                return response || $q.when(response);
            }
        };
    });

    genoBrowser.config(function ($httpProvider) {
        $httpProvider.interceptors.push('authInterceptor');
    });

})();
