(function(){
    'use strict';

    var genoBrowserControllers = angular.module('genoBrowserControllers', ['genoBrowserServices']);

    genoBrowserControllers.controller('ViewController', ['$scope', '$routeParams',
        function($scope, $routeParams) {

        }]);

    genoBrowserControllers.controller('BoundsController', ['$scope','PlotBounds', function($scope, PlotBounds){
        $scope.bounds = PlotBounds;
    }]);

    genoBrowserControllers.controller('ExampleWigController', ['$scope', 'PlotBounds', function($scope, PlotBounds){
        // Default data to get passed to plot, none
        $scope.boundedData = [
            {
                "key":"Wig",
                "values": []
            }
        ];
        // TODO Here we hold onto some example data, should be loaded by a service in the future
        $scope.exampleData = [
            [0, 0], [1000, 1], [2000, 1], [3000, 0], [4000, 2], [5000, 1], [6000, 0], [7000, 0], [8000, 0], [9000, 0], [10000, 0], [11000, 0], [12000, 0], [13000, 0], [14000, 0], [15000, 0], [16000, 0], [17000, 0], [18000, 0], [19000, 1], [20000, 0], [21000, 0], [22000, 0], [23000, 0], [24000, 0], [25000, 0], [26000, 0], [27000, 0], [28000, 0], [29000, 0], [30000, 0], [31000, 0], [32000, 0], [33000, 0], [34000, 0], [35000, 0], [36000, 0], [37000, 0], [38000, 167], [39000, 841], [40000, 33], [41000, 1], [42000, 2], [43000, 17], [44000, 0], [45000, 0], [46000, 0], [47000, 2], [48000, 2], [49000, 1], [50000, 1], [51000, 0], [52000, 2], [53000, 1], [54000, 3], [55000, 5], [56000, 7], [57000, 12], [58000, 3], [59000, 5], [60000, 1], [61000, 3], [62000, 0], [63000, 6], [64000, 9], [65000, 15], [66000, 20], [67000, 6], [68000, 34], [69000, 13], [70000, 0], [71000, 21], [72000, 0], [73000, 1], [74000, 1], [75000, 4], [76000, 0], [77000, 0], [78000, 1], [79000, 1], [80000, 0], [81000, 0], [82000, 0], [83000, 0], [84000, 0], [85000, 1], [86000, 1], [87000, 2], [88000, 0], [89000, 0], [90000, 3], [91000, 1], [92000, 0], [93000, 6], [94000, 0], [95000, 1], [96000, 0], [97000, 1], [98000, 2], [99000, 6], [100000, 4], [101000, 3], [102000, 1], [103000, 1], [104000, 4], [105000, 3], [106000, 3], [107000, 1], [108000, 0], [109000, 7], [110000, 2], [111000, 2], [112000, 0], [113000, 3], [114000, 1], [115000, 0], [116000, 0], [117000, 1], [118000, 0], [119000, 0], [120000, 0], [121000, 1], [122000, 0], [123000, 0], [124000, 1], [125000, 0], [126000, 0], [127000, 1], [128000, 0], [129000, 5], [130000, 2], [131000, 2], [132000, 1], [133000, 0], [134000, 0], [135000, 0], [136000, 0], [137000, 1], [138000, 7], [139000, 3], [140000, 2], [141000, 272], [142000, 211], [143000, 3], [144000, 3], [145000, 3], [146000, 77], [147000, 77], [148000, 78], [149000, 80], [150000, 27], [151000, 29], [152000, 32], [153000, 41], [154000, 38], [155000, 40], [156000, 81], [157000, 60], [158000, 58], [159000, 26], [160000, 48], [161000, 1], [162000, 7], [163000, 2], [164000, 2], [165000, 6], [166000, 1], [167000, 0], [168000, 2], [169000, 0], [170000, 0], [171000, 0]
        ];

        // Initialize the view's plot bounds to the data bounds
        PlotBounds[0] = $scope.exampleData[0][0];
        PlotBounds[1] = $scope.exampleData.slice(-1)[0][0];

        // Bind the bounds to the scope
        $scope.bounds = PlotBounds;
        // Watch for changes in the view's bounds (from input at the page footer)
        $scope.$watch('bounds', function(newValue){
            // We have to make a copy because the library
            // we are using only tells angular to watch for changes in reference pointer
            var newBoundedData = angular.copy($scope.boundedData);
            // Bound the example data and put it in values
            newBoundedData[0]["values"] = $scope.exampleData.filter(function(element){
                return (element[0] >= newValue[0]) && (element[0] <= newValue[1]);
            });
            $scope.boundedData = newBoundedData;
        }, true);

        $scope.hidden = false;

        $scope.sticky = false;

    }]);

    genoBrowserControllers.controller('wigController', ['$scope', 'PlotBounds', 'Tracks', function($scope, PlotBounds, Tracks){
        $scope.boundedData = [
            {
                key: "Wig",
                values: []
            }
        ]
        Tracks.get(function(response){
            console.log(response);
            $scope.boundedData.values = response.values;
        });

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
