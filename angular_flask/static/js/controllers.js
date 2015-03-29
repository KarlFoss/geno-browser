'use strict';

/* Controllers */

var genoBrowserControllers = angular.module('genoBrowserControllers', []);

genoBrowserControllers.controller('navMenuController', ['$scope',
  function ($scope) {
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

      $scope.views = [
        {'name': 'my view'},
        {'name': 'your view'},
        {'name': 'our view'},
        {'name': 'a view?'}
      ];


  }]);
