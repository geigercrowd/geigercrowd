<?php

class Datastore {

	private static $db;

	private __construct() {
		$this->db = new Mongo();
	}

}

?>
