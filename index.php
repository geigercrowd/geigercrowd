<?php

	$data = json_encode($_POST);
	
	$mongo = new Mongo();

	$db = $mongo->selectDB('geigercrowd');

	$db->datapoints->insert( $data );

?>
