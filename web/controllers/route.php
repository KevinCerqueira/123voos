<?php 
include_once($_SERVER['DOCUMENT_ROOT'] . '/123voos/web/controllers/RoutesController.php');

$routes = new RoutesController();
$route = $routes->get($_POST['type'], $_POST['value']);
echo json_encode($response);

?>