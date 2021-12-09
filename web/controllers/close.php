<?php 
include_once($_SERVER['DOCUMENT_ROOT'] . '/123voos/web/controllers/RoutesController.php');

$routes = new RoutesController();
$routes->closeAllServers(['host' => 'localhost', 'port' => 8000]);
$routes->closeAllServers(['host' => 'localhost', 'port' => 8100]);
$routes->closeAllServers(['host' => 'localhost', 'port' => 8200]);
?>