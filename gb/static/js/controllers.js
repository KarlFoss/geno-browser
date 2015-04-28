(function(){
    'use strict';

    var genoBrowserControllers = angular.module('genoBrowserControllers', ['genoBrowserServices']);

    genoBrowserControllers.controller('ViewController', ['$scope', '$location', '$routeParams', 'DataViews',
        function($scope, $location, $routeParams, DataViews) {
            var view_id = parseInt($location.path().slice(-1)[0]) || '';
            if(view_id !== ''){
                var data_view = DataViews.get({view_id: view_id}, function(){
                    console.log(data_view);
                    $scope.trackData = [];
                    $scope.boundedData = [];
                    for(var i = 0; i < data_view.view_tracks.length; i++){
                        var view = data_view.view_tracks[i];
                        if(view.data_type === 'wig'){
                            $scope.trackData.push([{key: view.track_name, values:view.data}]);
                        }
                    }
                    $scope.boundedData = $scope.trackData;
                    console.log($scope.boundedData);
                });
            } else {
                $scope.boundedData = null;
            }
        }]);

    genoBrowserControllers.controller('manualBoundsController', ['$scope','PlotBounds', function($scope, PlotBounds){
        $scope.bounds = PlotBounds;
    }]);

    genoBrowserControllers.controller('sliderBoundsController', ['$scope','PlotBounds', function($scope, PlotBounds){
        $scope.bounds = PlotBounds;
    }]);

    genoBrowserControllers.controller('wigController', ['$scope', '$routeParams', 'PlotBounds', function($scope, $routeParams, PlotBounds){

    }]);

    genoBrowserControllers.controller('navBarController', ['$scope', 'userService', 'Users',
        function($scope, userService, Users) {
            $scope.user = userService;

            $scope.login = function() {
                Users.get(function(response) {

                });
            }
        }]);

    genoBrowserControllers.controller('registerModalController', ['$scope', 'userService', 'Users',
        function($scope, userService, Users) {
            $scope.user = userService;

            $scope.register = function() {
                console.log($scope.user);
                Users.save($scope.user);
            }
        }]);
})();
