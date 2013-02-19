var myCenter=new google.maps.LatLng(40,-97);
var mySize=new google.maps.Size(2000,1000);
//markers
var markers = [];

function initialize()
	{
	
	//initial map configurations
	var mapProp = {
			center:myCenter,
			size:mySize,
			minZoom:3,
			maxZoom:13,
			zoom:2,
			mapTypeId:google.maps.MapTypeId.ROADMAP,
			zoomControl:true,
			mapTypeControl:false,
			streetViewControl:false,
			zoomControlOptions: {
				style:google.maps.ZoomControlStyle.SMALL
			}
		};
	//creates new map
	var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
	
	//map colors and styles
	var styles = [
		{
			featureType: "road",
			elementType: "geometry",
			stylers: [
				{ visibility: "simplified" }
			]
		},{
			featureType: "road",
			elementType: "labels",
			stylers: [
        		{ visibility: "off" }
      		]

		},
		{
    		featureType: "administrative",
   			elementType: "all",
    		stylers: [
      			{ saturation: -100 }
    		]
  		},{
    		featureType: "landscape",
		    elementType: "all",
		    stylers: [
		      { saturation: -100 }
		    ]
		},{
		    featureType: "poi",
		    elementType: "all",
		    stylers: [
		      { saturation: -100 }
		    ]
		},{
		    featureType: "road",
		    elementType: "all",
		    stylers: [
		      { saturation: -100 }
		    ]
		},{
		    featureType: "transit",
		    elementType: "all",
		    stylers: [
		      { saturation: -100 }
		    ]
		},{
		    featureType: "water",
		    elementType: "all",
		    stylers: [
		      { visibility: "off" }
		    ]
		}
	];
	//set map styles
	map.setOptions({styles: styles});
	
	
	
	
	
	
	// Add a listener for changes to the map
	google.maps.event.addListener(map, "idle", function() {
		var bounds = map.getBounds();
		var northeast = bounds.getNorthEast();
		var southwest = bounds.getSouthWest();
		loadAjax(map, northeast.lat(),northeast.lng(),southwest.lat(),southwest.lng(), "country");
	});
	
	
};//end of initialize()

//initializing the map
google.maps.event.addDomListener(window, 'load', initialize);
