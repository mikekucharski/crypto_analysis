<?php

if (!isset($_GET['cipher']) || !isset($_GET['m']) 
|| !isset($_GET['k']) || !isset($_GET['encrypt'])) {
	print json_encode(array('success' => false, 'output' => 'Missing paramaters [cipher, k, m, encrypt]'));
	exit();
}

$cipher = $_GET['cipher'];
$m = rawurldecode($_GET['m']);
$k = $_GET['k'];
$encryptFlag = (filter_input(INPUT_GET, "encrypt", FILTER_VALIDATE_BOOLEAN)) ? "encrypt" : "decrypt";

$command = escapeshellcmd("./run.py -c \"{$cipher}\" -m \"{$m}\" -k \"{$k}\" {$encryptFlag}");
exec($command, $output, $return);

if( count($output) > 0 ) {
	$output = str_replace("\\", "", $output[0]);
	$output = rawurlencode($output);
} else {
	$output = "";
}

$res = array(
	'success' => $return==0, 
	'method'  => $cipher, 
	'output'  => $output
);

print json_encode($res);
?>