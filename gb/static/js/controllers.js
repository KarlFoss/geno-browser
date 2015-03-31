(function(){
    'use strict';

    var genoBrowserControllers = angular.module('genoBrowserControllers', []);

    genoBrowserControllers.controller('navBarController', ['$scope', 'userService',
        function($scope, userService) {
            $scope.user = userService;
        }]);

    genoBrowserControllers.controller('registerModalController', ['$scope', 'userService', 'Users',
        function($scope, userService, Users) {
            $scope.user = userService;

            $scope.register = function() {
                console.log($scope.user);
                Users.save($scope.user);
            }
        }]);

    genoBrowserControllers.controller('navMenuController', ['$scope', 'Tracks',
      function ($scope, Tracks) {

          $scope.files = [
            {'name': 'fasta_file',
             'type': 'fa'},
            {'name': 'wiggity_wack',
             'type': 'wig'},
            {'name': 'beddy_byeeeeee',
             'type': 'bed'},
            {'name': 'fasta_file',
             'type': 'fa'},
            {'name': 'wiggity_wack',
             'type': 'wig'},
            {'name': 'beddy_byeeeeee',
             'type': 'bed'},
            {'name': 'fasta_file',
             'type': 'fa'},
            {'name': 'wiggity_wack',
             'type': 'wig'},
            {'name': 'beddy_byeeeeee',
             'type': 'bed'}
          ];

          $scope.File = {
              add: function() {

              },

              select: function(file) {
                $scope.views = [
                    {'name': 'my view'},
                    {'name': 'your view'},
                    {'name': 'our view'},
                    {'name': 'a view?'}
                ];
              },

              edit: function(file) {

              },

              delete: function(file) {

              }
          };

          $scope.View = {
              add: function() {

              },

              select: function(view) {
                  Tracks.query(function(response) {
                      $scope.tracks = response.tracks;
                  });
              },

              edit: function(view) {

              },

              delete: function(view) {

              }
          };

          $scope.Track = {
              add: function() {

              },

              select: function(track) {

              },

              edit: function(track) {

              },

              delete: function(track) {

              }
          };
      }]);
})();
