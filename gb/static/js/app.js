(function(){
    'use strict';

    var genoBrowser = angular.module('genoBrowser', [
        'ngRoute',
        'ngResource',
        'genoBrowserControllers',
        'genoBrowserServices',
        'nvd3ChartDirectives',
        'genoBrowserDirectives',
        'ui-rangeSlider'
    ]);

    genoBrowser.config(['$routeProvider',
        function($routeProvider) {
            $routeProvider.
                when('/view/:viewId', {
                    templateUrl: 'partials/view-frame.html',
                    resolve:{'$routeParams':'$routeParams','DataViews':'DataViews'},
                    controller: function($routeParams, DataViews){
                        this.view_id = $routeParams.viewId;
                        this.data_view = DataViews.get({view_id:this.view_id});
                    },
                    controllerAs:'view_frame'
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
