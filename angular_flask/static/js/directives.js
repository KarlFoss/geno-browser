'use strict';

/* Directives */

angular.module('AngularFlask', [])
    .directive('slider', function (DataModel) {
      return {
         restrict: 'A',
         scope: true,
         controller: function ($scope, $element, $attrs) {
            $scope.onSlide = function (e, ui) {
              $scope.model = ui.value;
              // or set it on the model
              // DataModel.model = ui.value;
              // add to angular digest cycle
              $scope.$digest();
            };
         },
         link: function (scope, el, attrs) {

            var options = {
              slide: scope.onSlide  
            };

            // set up slider on load
            angular.element(document).ready(function () {
              scope.$slider = $(el).slider(options);
            });
         }
      }
  });
