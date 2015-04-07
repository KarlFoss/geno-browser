(function(){
'use strict';

/* Directives */
    angular.module('genoBrowserDirectives', ['genoBrowserControllers'])
        .directive('gbWigPlot', function(){
            return {
                restrict:'E',
                templateUrl:'partials/wig-plot.html',
            };
        });
})();
