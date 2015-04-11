(function(){
'use strict';

/* Directives */
    var genoBrowserDirectives = angular.module('genoBrowserDirectives', ['genoBrowserControllers','genoBrowserServices', 'ui.bootstrap']);

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

    genoBrowserDirectives.directive('viewList',['$location', 'Views', 'Tracks', '$modal', function($location, Views, Tracks, $modal){
        return {
            restrict: 'E',
            templateUrl: 'partials/views.html',
            link: function (scope, element, attrs) {
                var location_view_id = parseInt($location.path().slice(-1)[0]);
                scope.views = Views.query(function(views){
                    var loaded_view = views.filter(function(element){
                        return element.view_id === location_view_id;
                    })[0];
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

                scope.removeView = function (view) {
                    view.$delete(function() {
                        console.log('Running delete');
                        scope.views = Views.query();
                        if(scope.isSelectedView(view)){
                            scope.track_ids = [];
                        }
                    });

                };
                scope.editView = function(view){
                    //scope.views.push();
                    scope.selectView(view);
                    scope.edit_view_name = view.view_name;
                    scope.all_tracks = Tracks.query();
                    $modal.open({
                        templateUrl:'partials/edit_view_modal.html',
                        scope:scope
                    }).result.then(function(result){
                            view.view_name = result.view_name;
                            view.track_ids = [result.initial_track.track_id];
                            view.$update();
                        })
                };
                scope.load = function (view) {
                    $location.path('/view/' + view.view_id);
                    scope.loaded_view = view;
                };

                scope.addView = function(){
                    scope.selected_view = null;
                    scope.all_tracks = Tracks.query();
                    $modal.open({
                        templateUrl:'partials/add_view_modal.html',
                        scope:scope
                    }).result.then(function(result){
                            console.log(result);
                        });
                }
            },
            scope:{}
        };
    }]);

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
