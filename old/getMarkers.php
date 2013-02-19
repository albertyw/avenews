<?php
require("functions.php");
connectDatabase();

// Display a marker for all countries
$query = "SELECT name, latitude, longitude FROM countries";
$result = mysql_query($query) or die(mysql_error());
$returnArray = array();
while($row = mysql_fetch_array($result)){
    $name = $row['name'];
    $latitude = $row['latitude'];
    $longitude = $row['longitude'];
    array_push($returnArray,array($name,$latitude,$longitude));
}
$returnString = json_encode($returnArray);
echo $returnString;
