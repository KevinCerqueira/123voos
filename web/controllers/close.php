<?php 
include_once($_SERVER['DOCUMENT_ROOT'] . '/123voos/web/controllers/RoutesController.php');

$routes = new RoutesController();
$routes->closeAllServers(['host' => 'localhost', 'port' => 8000]);
$routes->closeAllServers(['host' => 'localhost', 'port' => 8100]);
$routes->closeAllServers(['host' => 'localhost', 'port' => 8200]);

// $routes->closeAllServers(['host' => 'localhost', 'port' => 8100]);
// foreach ([8000,8100,8200] as $port){
// 	try{
// 		$routes->closeAllServers(['host' => 'localhost', 'port' => $port]);
// 	}catch(Exception $e){
// 		echo $e;
// 	}
// }
?>