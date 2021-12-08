<?php 
include_once($_SERVER['DOCUMENT_ROOT'] . '/123voos/web/controllers/RoutesController.php');

$routes = new RoutesController();
var_dump($routes->closeAllServers(['host' => 'localhost', 'port' => 8200]))
?>