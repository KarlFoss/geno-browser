(function(){
'use strict';

/* Directives */
    var genoBrowserDirectives = angular.module('genoBrowserDirectives', ['genoBrowserControllers']);

    genoBrowserDirectives.directive('gbWigPlot', function(){
        return {
            restrict:'E',
            templateUrl:'partials/wig-plot.html',
        };
    });

    genoBrowserDirectives.directive('fileModel', ['$parse', function ($parse) {
        return {
            restrict: 'A',
            link: function(scope, element, attrs) {
                var model = $parse(attrs.fileModel);
                var modelSetter = model.assign;

                element.bind('change', function(){
                    scope.$apply(function(){
                        modelSetter(scope, element[0].files[0]);
                    });
                });
            }
        };
    }]);

})();
