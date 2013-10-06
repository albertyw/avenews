<?php

function connectDatabase(){
    mysql_connect("localhost", 'newsmap','') or die(mysql_error());
    mysql_select_db('newsmap') or die(mysql_error());
}
