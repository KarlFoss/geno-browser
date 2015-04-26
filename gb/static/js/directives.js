(function(){
'use strict';

/* Directives */
    var genoBrowserDirectives = angular.module('genoBrowserDirectives', ['genoBrowserControllers','genoBrowserServices', 'ui.bootstrap', 'angularFileUpload']);

    genoBrowserDirectives.directive("userToolbar", ['$window', 'API', '$location',
        function ($window, API, $location) {
            return {
                restrict: "E",
                templateUrl: "/partials/user_toolbar.html",
                link: function (scope, element, attrs) {
                    scope.user = {
                        'username':'',
                        'password':''
                    };

                    scope.isAuthenticated = function() {
                        return $window.sessionStorage.token;
                    };

                    scope.login = function() {
                        API.authenticate(scope.user, function(data) {
                            $window.sessionStorage.token = data.token;
                        }, function (response) {
                            delete $window.sessionStorage.token;
                        });
                        $location.path('/');
                        $window.location.reload();
                    };

                    scope.logout = function() {
                        delete $window.sessionStorage.token;
                        $location.path('/');
                        $window.location.reload();
                    };
                }
            };
        }
    ]);

    genoBrowserDirectives.directive('viewList',['$location', 'Views', 'Tracks', '$modal', '$route', function($location, Views, Tracks, $modal, $route){
        return {
            restrict: 'E',
            templateUrl: 'partials/views.html',
            link: function (scope, element, attrs) {
                // First see if the route indicates a loaded view
                var location_view_id = parseInt($location.path().slice(-1)[0]);
                scope.views = Views.query(function(views) {
                    // Find the view with a matching id and set it as loaded
                    var loaded_view = views.filter(function(element){
                        return element.view_id === location_view_id;
                    })[0];
                    // It will be set as undefined if no view is currently loaded
                    scope.loaded_view = loaded_view;
                });

                // Start off with no views selected
                scope.selected_view = null;

                // use this to select a view, called when the user clicks a view
                scope.selectView = function (view) {
                    // Set selected_view pointer to view
                    scope.selected_view = view;
                    // and the track_ids to the view's track_ids
                    scope.track_ids = view.track_ids;
                };

                // This is used by ng-class to check if a view is active
                scope.isSelectedView = function (view) {
                    return scope.selected_view === view;
                };

                // This is used by ng-class to check if a view is loaded
                // it gets a filled star if it is
                scope.isLoaded = function (view) {
                    return view === scope.loaded_view;
                };

                // This is called when a user clicks on a view's trash can
                scope.removeView = function (view) {
                    // Send DELETE request
                    view.$delete(function() {
                        // When we get a positive response
                        // Get a new list of views from the server
                        // The deleted view should be gone
                        scope.views = Views.query();
                        // If the deleted view was selected, clear the tracks pane
                        if(scope.isSelectedView(view)){
                            scope.track_ids = [];
                        }
                    });

                };

                // This is called when a user clicks on a view's edit button
                scope.editView = function(view){
                    // Select the view that will be edited
                    scope.selectView(view);
                    // Use the view_name as a starting point for editing
                    scope.edit_view_name = view.view_name;
                    // Get a list of all tracks for the dropdown
                    scope.all_tracks = Tracks.query();
                    // Open the view edit modal
                    $modal.open({
                        templateUrl:'partials/edit_view_modal.html',
                        scope:scope
                    }).result.then(function(result){
                            // After the modal is submitted
                            // Set the view's attributes to the edited values
                            view.view_name = result.view_name;
                            view.track_ids = [result.initial_track.track_id];
                            // Send PUT request with new values
                            view.$update();
                            $route.reload();
                        })
                };

                // This is called when a user clicks the X on a view
                scope.removeTrackFromView = function(track){
                    // Remove the track from the list of track_ids watched by the trackList directive
                    scope.track_ids.splice(scope.track_ids.indexOf(track.track_id),1);
                    // Send PUT request with track_ids minus the removed one
                    scope.selected_view.track_ids = scope.track_ids;
                    scope.selected_view.$update();
                    $route.reload();
                };

                // This is called when a user submits the add track modal
                scope.addTrackToView = function(track){
                    // Add the id to the list of track_ids watched by the trackList directive
                    scope.track_ids.push(track.track_id);
                    // PUT the new track_ids to the view
                    scope.selected_view.track_ids = scope.track_ids;
                    scope.selected_view.$update();
                    $route.reload();
                };

                // This is called when the user clicks on the star
                scope.load = function (view) {
                    // Set the view_id to be loaded in the URL
                    // This change will be detected by the plotting controllers
                    $location.path('/view/' + view.view_id);
                    $route.reload();
                    // Remember which view was loaded so we can quickly check
                    scope.loaded_view = view;

                };

                // This is called when the user clicks the add view button +
                scope.addView = function(){
                    // Deselect views
                    scope.selected_view = null;
                    // Get a current list of all tracks available as initial track
                    scope.all_tracks = Tracks.query();
                    // Open the add view modal
                    $modal.open({
                        templateUrl:'partials/add_view_modal.html',
                        scope:scope
                    }).result.then(function(result){
                            // When the user submits
                            // Create a new view based on the form data that gets passed back on $close
                            Views.create({track_ids:[result.initial_track.track_id], view_name:result.view_name}, function(){
                                // After confirmation that the view has been created
                                // Refresh the list of views
                                scope.views = Views.query();
                                $route.reload();
                            });
                        });
                };
            },
            // Start an isolated scope
            scope:{}
        };
    }]);

    genoBrowserDirectives.directive('trackList', ['Tracks', '$modal', '$upload', function(Tracks, $modal, $upload){
       return {
           restrict: 'E',
           templateUrl: 'partials/tracks.html',
           link: function(scope,element,attr){
               // Deselect tracks
               scope.selected_track = null;

               // Watch the track_ids attribute, controlled mostly by viewList
               scope.$watch('track_ids',function(newValue){
                   // On change of a view's tracks
                   // If track_ids is valid
                   if(newValue) {
                       // deselect tracks
                       scope.selected_track = null;
                       // Clear tracks from track pane
                       scope.tracks = [];
                       // For every track in track_ids
                       newValue.forEach(function (track_id, index) {
                           // if track_id is valid
                           if(track_id || track_id === 0){
                               // GET the track data for track_id
                               Tracks.get({track_id: track_id}, function (data) {
                                   // Push the result to tracks, which is used by ngRepeat
                                   scope.tracks.push(data);
                               }, function (response) {
                                   // Ignore 404s
                                   if (response.status === 404) {

                                   }
                               });
                           }
                       });
                   }
                   else{
                       // New track_ids array is invalid
                       // Deselect tracks
                       scope.selected_track = null;
                       // Clear tracks pane
                       scope.tracks = [];
                   }
                   //Watch for changes in array equality, not just pointer
               }, true);

               // This is called when the user clicks on a track
               scope.selectTrack = function(track){
                   scope.selected_track = track;
               };

               // This is used by ngClass to see whether to apply the active class and highlight
               scope.isSelectedTrack = function(track){
                   return track === scope.selected_track;
               };

               // This is called when the user clicks on the add track button
               scope.addTrack = function(){
                   // Get a list of all tracks for the add exisiting track dropdown
                   scope.all_tracks = Tracks.query();
                   // Open the add track modal
                   $modal.open({
                       templateUrl:'partials/add_track_modal.html',
                       scope:scope
                   }).result.then(function(result){
                           // After the user submits the form
                           // If the user added an existing track
                           if(result.track) {
                               scope.addTrackToView(result.track);
                           }
                           else{
                               // The user submitted a file
                               // Upload the file
                               $upload.upload({
                                   file: result.file,
                                   fileFormDataName: 'file',
                                   url: '/api/files',
                                   fields: {
                                       track_name: result.track_name || '',
                                       type: result.track_type
                                   }
                               }).then(function(success){
                                   // After the upload is complete
                                   // Get the track_id for the recently uploaded file returned by the API
                                   var new_track_id = success.data.track_ids[0];
                                   if(new_track_id && new_track_id !== 0) {
                                       // Modify the selected view and PUT the changes
                                       scope.addTrackToView({track_id:new_track_id});
                                   }
                               });
                           }


                       });
               };

               // This is called when the user clicks on the edit button
               scope.editTrack = function(track){
                   // Select the track to be edited
                   scope.selectTrack(track);
                   // GET a list of all tracks for the dropdown
                   scope.all_tracks = Tracks.query();
                   // Open the edit track modal
                   $modal.open({
                       templateUrl:'partials/edit_track_modal.html',
                       scope:scope
                   }).result.then(function(result){
                           // After the user submits the form
                           // Make modifications to the selected view
                           scope.selected_track.track_name = result.track_name;
                           // PUT the changes to server
                           scope.selected_track.$update();
                       });
               };

               // This is called when the user clicks the trash can
               scope.deleteTrack = function(track){
                   // DELETE the track
                   track.$delete(function() {
                       // After confirmation of deletion
                       // Remove the track from list of tracks used by ngRepeat
                       scope.tracks.splice(scope.tracks.indexOf(track));
                       // If the track was selected before being deleted
                       if(scope.isSelectedTrack(track)){
                           // Deselect tracks
                           scope.selected_track = null;
                       }
                       // Refresh the selected view, it shouldn't have the deleted track_id now
                       scope.selected_view.get();
                   });
               };
           },
           // Inherit scope from viewList
           scope:true
       };
    }]);

    genoBrowserDirectives.directive('gbTrack', ['Tracks', function(Tracks){
        return {
            restrict:'E',
            templateUrl:'partials/track.html',
            scope:true,
        }
    }]);

    genoBrowserDirectives.directive('gbBedPlot', function(){
        return {
            restrict:'E',
            templateUrl:'partials/bed-plot.html'
        };
    });

    genoBrowserDirectives.directive('gbWigPlot', ['PlotBounds', function(PlotBounds){
        return {
            restrict:'E',
            templateUrl:'partials/wig-plot.html',
            scope:true,
            link: function(scope, element, attrs){
                // Set bounds from first x value and last x value in data.
                PlotBounds[0] = scope.track.data[0][0];
                PlotBounds[1] = scope.track.data.slice(-1)[0][0];
                // Bind the bounds to the scope
                scope.bounds = PlotBounds;
                scope.$watch('bounds', function(){
                    scope.boundedData = [{
                        key:'Wig',
                        values:scope.track.data.filter(function(element){
                            return (element[0] >= scope.bounds[0]) && (element[0] <= scope.bounds[1]);
                        })
                    }];
                }, true);
                scope.hidden = false;
                scope.sticky = false;
            }
        };
    }]);

})();
