<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<style type="text/css">
  html { height: 100% }
  body { height: 100%; margin: 0px; padding: 0px }
  #map_canvas { height: 100% }
</style>
<script type="text/javascript" src="jquery-1.4.3.min.js"></script>
<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=true"></script>
<script type="text/javascript">
function initialize_map() {
    /*
    Create the basic map and return it
    */
    var latlng = new google.maps.LatLng(0, 0);
    var myOptions = {
        zoom: 3,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
    return map;
}
function getMarkers(map) {
    /*
    Get markers and display them
    */
    $.post(
        'getMarkers.php',
        {
            // extra variables
        },
        function(data) {
            for(var i=0; i < data.length; i++){
                var name = data[i][0];
                var latitude = data[i][1];
                var longitude = data[i][2];
                var LatLong = new google.maps.LatLng(latitude, longitude);
                var marker = new google.maps.Marker({
                    position: LatLong,
                    map: map,
                    title:name
                });
            }
        },
        "json"
    );
    var latlng = new google.maps.LatLng(0, 0);
    var marker = new google.maps.Marker({
        position: latlng, 
        map: map, 
        title:"Hello World!"
    });   
}
$(document).ready(function() {
    var map = initialize_map();
    getMarkers(map);
});
</script>
</head>
<body>
  <div id="header" style="width:100%; height:10%;font-size:20px;text-align:center;">
  News Map Header
  </div>
  <div id="map_canvas" style="width:80%; height:90%;float:left"></div>
  <div id="news" style="width:20%;height:90%;float:right">asdf</div>
</body>
</html>
