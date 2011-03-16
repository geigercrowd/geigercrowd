<?php

// Include the necessary classes.
require_once('classes/datastore.php');
require_once('classes/api.php');
require_once('classes/page.php');

switch ($_SERVER['REQUEST_METHOD']) {

	case 'POST':
		$API 		= new API();
		$mongo 		= new Mongo();
		$db		= $mongo->selectDB('geigercrowd');

		$data = array(
			'timestamp' => (!empty($_POST['timestamp']) 	? (int) $_POST['timestamp'] : time(),
			'latitude'  => (float) $_POST['latitude'],
			'longitude' => (float) $_POST['longitude'],
			'reading'   => (float) $_POST['reading'],
		);

		if ($db->datapoints->insert($data)) {
			$API->output(array(
				'status' => 'success'
			));
		} else {
			$API->output(array(
				'status' => 'failed to insert data.'
			));
		}
	break;

}


$page = new Page();
$page->demo();

?>
