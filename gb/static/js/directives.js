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

    genoBrowserDirectives.directive('viewList',['$location', 'Views', function($location, Views){
        return {
            restrict: 'E',
            templateUrl: 'partials/views.html',
            controller: function () {
                this.views = Views.query();
                this.selected_view = null;
                this.loaded_view = parseInt($location.path().slice(-1)[0]);
                this.selectView = function (view) {
                    this.selected_view = view;
                    var tracks = new Array(view.track_ids.length);
                    view.track_ids.forEach(function(element, index){
                        tracks[index] = Tracks.get({track_id:element.track_id});
                    });
                    this.tracks = tracks;
                    console.log(tracks);
                };
                this.isSelected = function (view) {
                    return this.selected_view === view;
                };

                this.isLoaded = function (view) {
                    return view.view_id === this.loaded_view;
                };

                this.remove = function (view) {
                    view.$delete();
                    var scope = this;
                    var views = Views.query({}, function (success) {
                        console.log('success');
                        scope.views = views;
                    }, function(response){
                        if(response.status == 404) {
                            scope.views = [];
                        }
                    });

                };
                this.edit = function(view){

                };
                this.load = function (view) {
                    $location.path('/view/' + view.view_id);
                    this.loaded_view = parseInt(view.view_id);
                };
            },
            scope:{
                onCreate:'&'
            },
            controllerAs:"viewList"
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
           controller: function(){
               this.selected_track = null;
               this.selectTrack = function(track){
                   this.selected_track = track.track_id;
               };
               this.isSelected = function(track){
                   return track === selectedTrack;
               }
               this.edit = function(track){

               }
               this.delete = function(track){
                   track.$delete();
               }
           },
           controllerAs:'trackList'
       }
    }]);

})();
