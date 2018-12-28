<?php
header("Content-Type:application/json");
require "backend.php";

if(!empty($_POST['type']) && !empty($_POST['id'])) {

    $type = $_POST['type'];
    
	if ($type == 'alert' && !empty($_POST['message'])) {
        $msg = $_POST['message'];
        $id = $_POST['id'];
        response(200, $msg, $id);
    }
}
else {echo 400;}

?>