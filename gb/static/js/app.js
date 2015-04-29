(function(){
    'use strict';

    var genoBrowser = angular.module('genoBrowser', [
        'ngRoute',
        'ngResource',
        'genoBrowserControllers',
        'genoBrowserServices',
        'nvd3ChartDirectives',
        'genoBrowserDirectives',
        'ui-rangeSlider',
        'ui.bootstrap.showErrors'
    ]);

    genoBrowser.config(['$routeProvider',
        function($routeProvider) {
            $routeProvider.
                when('/view/:viewId', {
                    templateUrl: 'partials/view-frame.html',
                    resolve:{'$routeParams':'$routeParams','DataViews':'DataViews'},
                    controller: function($routeParams, DataViews){
                        var _this = this;
                        _this.view_id = $routeParams.viewId;
                        _this.fasta_track = {data_type: "fasta", data:[">EBV1", 'ACTGACTG']};
                        _this.data_view = DataViews.get({view_id:_this.view_id}, function(){
                            for(var i = 0; i < _this.data_view.view_tracks.length; i++){
                                if(_this.data_view.view_tracks[i].data_type === 'fasta'){
                                    _this.data_view.view_tracks.push(_this.data_view.view_tracks.splice(i, 1)[0]);
                                }
                            }
                            console.log(_this.data_view.view_tracks);
                        });
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
