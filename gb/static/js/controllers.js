(function(){
    'use strict';

    var genoBrowserControllers = angular.module('genoBrowserControllers', ['genoBrowserServices']);

    genoBrowserControllers.controller('ViewController', ['$scope', '$location', '$routeParams', 'DataViews',
        function($scope, $location, $routeParams, DataViews) {
            var view_id = parseInt($location.path().slice(-1)[0]) || '';
            if(view_id !== ''){
                var data_view = DataViews.get({view_id: view_id}, function(){
                    $scope.trackData = [];
                    $scope.boundedData = [];
/*                    for(var i = 0; i < data_view.view_tracks.length; i++ ){
                        var track_data = data_view.view_tracks[i].data;
                        $scope.trackData.push([]);
                        $scope.trackData[i].push({key: "Wig " + (i+1), values: []});
                        for(var j = 0; j < track_data[0].length; j++){
                            $scope.trackData[i][0].values.push([track_data[0][j], track_data[1][j]]);
                        }
                        $scope.boundedData.push($scope.trackData[i]);
                    }*/
                    console.log(data_view);
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

    genoBrowserControllers.controller('BoundsController', ['$scope','PlotBounds', function($scope, PlotBounds){
        $scope.bounds = PlotBounds;
    }]);

    genoBrowserControllers.controller('wigController', ['$scope', '$routeParams', 'PlotBounds', function($scope, $routeParams, PlotBounds){
        /*PlotBounds[0] = $scope.trackData[0].values[0][0];
        PlotBounds[1] = $scope.trackData[0].values.slice(-1)[0][0];
        // Bind the bounds to the scope
        $scope.bounds = PlotBounds;
        $scope.$watch('bounds', function(newValue){
            // We have to make a copy because the library
            // we are using only tells angular to watch for changes in reference pointer
            var newBoundedData = angular.copy($scope.trackData);
            // Bound the example data and put it in values
            newBoundedData[0]["values"] = $scope.trackData[0].values.filter(function(element){
                return (element[0] >= newValue[0]) && (element[0] <= newValue[1]);
            });
            $scope.boundedData = newBoundedData;
        }, true);
        $scope.hidden = false;
        $scope.sticky = false;*/
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
