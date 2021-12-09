<?php 
include_once($_SERVER['DOCUMENT_ROOT'] . '/123voos/web/controllers/RoutesController.php');

$routes = new RoutesController();
if($_POST['action'] == 'disconfirm'){
	$response = $routes->disconfirmRoute($_POST['id'],  ['host'=>$_POST['host'], 'port' => $_POST['port']]);
}else{
	$response = $routes->confirmRoute($_POST['id'], ['host'=>$_POST['host'], 'port' => $_POST['port']]);
}
echo json_encode($response);
