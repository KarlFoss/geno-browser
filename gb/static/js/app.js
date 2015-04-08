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
        $httpProvider.interceptors.push(['$q', '$location', 'TokenHandler',
            function($q, $location, TokenHandler) {
                return {
                    'request': function (config) {
                        config.headers = config.headers || {};
                        config.headers['token'] = TokenHandler.get();

                        return config;
                    },
                    'responseError': function(response) {

                    }
                };
        }]);
    });

})();
