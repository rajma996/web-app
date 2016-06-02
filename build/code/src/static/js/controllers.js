
var app = angular.module('directoryApp.controllers',[]);
app.controller("users", function($scope,  $http, $routeParams, $route,$window){
    $scope.role_name = $window.role_name;
    $http.get("http://localhost:5000/users", {headers: {'session': $window.session_email }}).success(function(response){
	$scope.users = response;
    });

});

app.controller("view-user", function($scope,  $http, $routeParams, $route,$window){
    $scope.role_name = $window.role_name;
    $scope.user_id = $window.user_id;
    $http.get("http://localhost:5000/users/" + $routeParams.id, {headers: {'session': $window.session_email }}).success(function(response){
	$scope.users = response;
    });

    $scope.delete_user = function()
    {
      console.log($routeParams.id)
      $http.delete("http://localhost:5000/users/" + $routeParams.id , {headers: {'session': $window.session_email } }  ).success(function(response)
      {
         $scope.users = response;
         console.log(response)
         console.log(response['error']);
         if (typeof response['error'] !== 'undefined')
         {
            $scope.status = response['error']
         }
         else
         {
           history.back()
         }

      });


    };



});

app.controller("add-user", function($scope,  $http, $routeParams, $route,$window){
    $scope.role_name = $window.role_name;

    $scope.add_user = function()
    {

      var send_data =
      {
        name : $scope.name,
        email: $scope.email,
        role: $scope.role,
        session : $window.session_email
      };
      console.log(send_data)
      $http.post("http://localhost:5000/users/" , send_data).success(function(response)
      {
         $scope.users = response;
         console.log(response)
         console.log(response['error']);
         if (typeof response['error'] !== 'undefined')
         {
            $scope.status = response['error']
         }
         else
         {
           history.back()
         }

      });


    };

});

app.controller("edit-user", function($scope,  $http, $routeParams, $route,$window){
    $scope.role_name = $window.role_name;
    console.log($window.role_name)
    $scope.edit_user = function()
    {

      var send_data =
      {
        name : $scope.name,
        email: $scope.email,
        session : $window.session_email
      };
      console.log(send_data)
      $http.put("http://localhost:5000/users/" + $routeParams.id, send_data, {headers: {'session': $window.session_email } }   ).success(function(response)
      {
         $scope.users = response;
         console.log(response)
         history.back()
         history.back()
      });

    };

});
