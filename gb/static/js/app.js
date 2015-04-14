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
                when('/view', {
                    templateUrl: 'partials/view-frame.html',
                    controller: 'ViewController'
                }).
                when('/view/:viewId', {
                    templateUrl: 'partials/view-frame.html',
                    controller: 'ViewController'
                }).
                otherwise({
                    redirectTo: '/view'
                });
        }]);

})();
