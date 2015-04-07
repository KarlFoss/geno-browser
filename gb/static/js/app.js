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

    genoBrowser.config(function($httpProvider) {
        $httpProvider.interceptors.push(['$q', '$location', function($q, $location) {
            return {
                'request': function (config) {
                    config.headers = config.headers || {};
                    config.headers['X-Userid']   = '1';
                    config.headers['auth-token'] = '';

                    return config;
                },
                'responseError': function(response) {

                }
            };
        }]);
    });

})();
