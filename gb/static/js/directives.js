(function(){
'use strict';

/* Directives */
    var genoBrowserDirectives = angular.module('genoBrowserDirectives', ['genoBrowserControllers','genoBrowserServices', 'ui.bootstrap', 'angularFileUpload']);

    genoBrowserDirectives.directive('gbWigPlot', function(){
        return {
            restrict:'E',
            templateUrl:'partials/wig-plot.html'
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
                        scope.views = Views.query();
                        if(scope.isSelectedView(view)){
                            scope.track_ids = [];
                        }
                    });

                };
                scope.editView = function(view){
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
                scope.removeTrackFromView = function(track){
                    scope.track_ids.splice(scope.track_ids.indexOf(track.track_id),1);
                    scope.selected_view.$update();
                };
                scope.addTrackToView = function(track){
                    scope.track_ids.push(track.track_id);
                    scope.selected_view.$update();
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
                            Views.create({track_ids:[result.initial_track.track_id], view_name:result.view_name}, function(){
                                scope.views = Views.query();
                            });
                        });
                }
            },
            scope:{}
        };
    }]);

    genoBrowserDirectives.directive('trackList', ['Tracks', '$modal', '$upload', function(Tracks, $modal, $upload){
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
                           if(track_id) {
                               Tracks.get({track_id: track_id}, function (data) {
                                   scope.tracks.push(data);
                               }, function (response) {
                                   if (response.status === 404) {

                                   }
                               });
                           }
                       });
                   }
                   else{
                       scope.selected_track = null;
                       scope.tracks = [];
                   }
               }, true);
               scope.selectTrack = function(track){
                   scope.selected_track = track;
               };
               scope.isSelectedTrack = function(track){
                   return track === scope.selected_track;
               };
               scope.addTrack = function(){
                   scope.all_tracks = Tracks.query();
                   $modal.open({
                       templateUrl:'partials/add_track_modal.html',
                       scope:scope
                   }).result.then(function(result){
                           if(result.track) {
                               scope.addTrackToView(result.track);
                           }
                           else{
                               $upload.upload({
                                   file: result.file,
                                   fileFormDataName: 'file',
                                   url: '/api/files',
                                   fields: {
                                       track_name: result.track_name || '',
                                       type: result.track_type
                                   }
                               }).then(function(success){
                                   var new_track_id = success.data.track_ids[0];
                                   if(new_track_id !== undefined) {
                                       scope.addTrackToView({track_id:new_track_id});
                                   }
                               });
                           }


                       });
               };
               scope.editTrack = function(track){
                   scope.selectTrack(track);
                   scope.all_tracks = Tracks.query();
                   $modal.open({
                       templateUrl:'partials/edit_track_modal.html',
                       scope:scope
                   }).result.then(function(result){
                           scope.selected_track.track_name = result.track_name;
                           scope.selected_track.$update();
                       });
               };
               scope.deleteTrack = function(track){
                   track.$delete(function() {
                       scope.tracks.splice(scope.tracks.indexOf(track));
                       if(scope.isSelectedTrack(track)){
                           scope.selected_track = null;
                       }
                       scope.selected_view.get();
                   });
               };
           },
           scope:true
       };
    }]);

})();
