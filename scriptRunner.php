<?php

if (!isset($_GET['cipher']) || !isset($_GET['m']) 
|| !isset($_GET['k']) || !isset($_GET['encrypt'])) {
	print json_encode(array('success' => false, 'output' => 'Missing paramaters.'));
	exit();
}

$cipher = $_GET['cipher'];
$m = $_GET['m'];
$k = $_GET['k'];
$encryptFlag = (filter_input(INPUT_GET, "encrypt", FILTER_VALIDATE_BOOLEAN)) ? "encrypt" : "decrypt";

// $command = escapeshellcmd("./$cipher.py -m \"qp9)0!O8ts{pQ27]+)09O7OZ;ryxIlHmGnFoEpk(\" -k \"22.22.22.23\" decrypt");
$command = escapeshellcmd("./{$cipher}_cipher.py -m \"{$m}\" -k \"{$k}\" {$encryptFlag}");
exec($command, $output, $return);

$res = array(
	'success' => $return==0, 
	'method'  => 'caesar', 
	'output'  => $output
);
print json_encode($res);

?>