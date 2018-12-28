<?php

// MySQL Credentals
$dbhost = "localhost:3306";
$dbun = "pi";
$dbpw = "Riyco321";
$dbname = "rath";
$conn = mysqli_connect($dbhost, $dbun, $dbpw, $dbname);

$queue = mysqli_query($conn, "SELECT json FROM api");

function response($status, $msg, $id)
{
	header("HTTP/1.1 ".$status);
	
	$json = $msg;

	queue($json, $id);
	
	echo 200;
}

function queue($json, $id){
	global $conn;

	$json = (string)$json;
	$query = "INSERT INTO api (json, id) VALUES ('$json', '$id')";
	mysqli_query($conn, $query);

	$query = "INSERT INTO history (json) VALUES ('$json')";
	mysqli_query($conn, $query);
}

function dequeue($id){
	global $conn;

	$query = "DELETE FROM api WHERE id='$id'";
	mysqli_query($conn, $query);
	echo '200';
}

?>