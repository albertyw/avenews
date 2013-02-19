//markers
var markers = [];

/**
 * Called when map is moved
 * Loads javascript for the map
 **/
function loadAjax(map, lat1,lng1,lat2,lng2, level){
    var query = "/ajax/latlon/"+level+"/" + lat1 + "/" + lng1 + "/" + lat2 + "/" + lng2;
    $.getJSON(query , function(data){
        
        $(data).each(function(i){
            loadMap(map, data[i]);
        });
    });
};

/**
 * checks for loaded markers
 **/
function alreadyLoaded(article_id){
    var loaded = false;
    $(markers).each(function(i){
        if (markers[i] == article_id){
            loaded = true;
        }
    });
    return loaded;
};

/**
 * Called by load_ajax to load new markers onto the map
 **/
function loadMap(map, article_location){
    country_name = article_location[0];
    lat = parseFloat(article_location[1]);
    lon = parseFloat(article_location[2]);
    if (alreadyLoaded(country_name) == false){
        //draw new markers from data
        var newpoint = new google.maps.LatLng(lat, lon);
        var marker = new google.maps.Marker({
            position: newpoint,
            title: country_name,
            map: map,
            clickable: true
        });
        google.maps.event.addListener(marker, 'click', function(event){
            loadArticleList(marker.getTitle());
        });
        markers.push(country_name);
    }
}

/**
 * Called when a marker is clicked on
 * Shows a list of articles at the marker's location
 **/
function loadArticleList(markerTitle){
    var query = "/ajax/articlelist/"+markerTitle;
    $.getJSON(query , function(data){
        var articlelist = '';
        $(data).each(function(i){
            article = data[i];
            console.log(article);
            articlelist += '<a href="javascript:loadArticle(\''+article.url+'\')">';
            articlelist += '<strong>'+article.title+'</strong><br />';
            articlelist += article.publishDate;
            articlelist += '</a><br /><br />';
        });
        if(articlelist==''){
            articlelist = 'Sorry, there is no news from '+markerTitle;
        }else{
            articlelist = 'News From '+markerTitle+'<br /><br />'+articlelist;
        }
        $("#article_list_div").html(articlelist);
    });
}

function loadArticle(url){
    $("#article_iframe").attr('src',url);
}
