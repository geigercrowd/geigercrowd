<?php

class API {
	public output($data) {
		header('Content-Type: application/json');
		echo json_encode($data);
		exit();
	}
}

?>
