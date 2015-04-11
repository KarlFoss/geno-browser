(function(){
'use strict';

/* Directives */
    var genoBrowserDirectives = angular.module('genoBrowserDirectives', ['genoBrowserControllers','genoBrowserServices']);

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

    genoBrowserDirectives.directive('viewList',['$location', 'Views', 'Tracks', function($location, Views, Tracks){
        return {
            restrict: 'E',
            templateUrl: 'partials/views.html',
            link: function (scope, element, attrs) {
                var location_view_id = parseInt($location.path().slice(-1)[0]);
                scope.views = Views.query(function(views){
                    console.log(views);
                    var loaded_view = views.filter(function(element){
                        return element.view_id === location_view_id;
                    })[0];
                    console.log(loaded_view);
                    scope.loaded_view = loaded_view;
                });
                scope.selected_view = null;

                scope.selectView = function (view) {
                    scope.selected_view = view;
                    scope.track_ids = view.track_ids;
                };

                scope.isSelectedView = function (view) {
                    return scope.selected_view === view;
                };

                scope.isLoaded = function (view) {
                    return view === scope.loaded_view;
                };

                scope.remove = function (view) {
                    view.$delete(function() {
                        console.log('Running delete');
                        scope.views = Views.query();
                        if(scope.isSelectedView(view)){
                            scope.track_ids = [];
                        }
                    });

                };
                scope.edit = function(view){

                };
                scope.load = function (view) {
                    $location.path('/view/' + view.view_id);
                    scope.loaded_view = view;
                };
            },
            scope:{}
        };
    }]);

    genoBrowserDirectives.directive('viewModal', function(){
       return {
           restrict: 'E',
           templateUrl: 'partials/view-modal.html'
       };
    });

    genoBrowserDirectives.directive('trackList', ['Tracks', function(Tracks){
       return {
           restrict: 'E',
           templateUrl: 'partials/tracks.html',
           link: function(scope,element,attr){
               scope.selected_track = null;
               scope.$watch('track_ids',function(newValue){
                   if(newValue) {
                       scope.selected_track = null;
                       scope.tracks = [];
                       newValue.forEach(function (track_id, index) {
                           Tracks.get({track_id: track_id},function(data){
                               scope.tracks.push(data);
                           }, function(response){
                               if(response.status === 404){

                               }
                           });
                       });
                   }
               }, true);
               scope.selectTrack = function(track){
                   scope.selected_track = track;
               };
               scope.isSelectedTrack = function(track){
                   return track === scope.selected_track;
               };
               scope.edit = function(track){

               };
               scope.delete = function(track){
                   track.$delete(function() {
                       scope.tracks.splice(scope.tracks.indexOf(track));
                       if(scope.isSelectedTrack(track)){
                           scope.selected_track = null;
                       }
                   });
               };
           },
           scope:true
       };
    }]);

})();
