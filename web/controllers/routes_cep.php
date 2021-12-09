<?php 
include_once($_SERVER['DOCUMENT_ROOT'] . '/123voos/web/controllers/RoutesController.php');

$routes = new RoutesController();
$all_routes = $routes->getAll();
// echo json_encode($all_routes);die();
if($all_routes->success){
	$all_routes = $all_routes->data;
}else{
	$all_routes = null;
}
?>