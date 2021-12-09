<?php
include_once('controllers/routes.php');
$cities = array();
foreach ($all_routes->companies as $company) {
	foreach ($company->routes as $key => $route) {
		if ($route->start->cep != $_GET['cep'] and !in_array($route->start->city, $cities)) {
			$cities[] = $route->start->city
?>
			<option type="<?php echo 'start'; ?>" cep="<?php echo $route->start->cep; ?>" host="<?php echo $company->host; ?>" port="<?php echo $company->port; ?>" value="<?php echo $route->start->id; ?>">
				<?php echo $route->start->city; //. ' | ' . $route->start->cep . ' | ' . $route->start->name; ?>
			</option>
		<?php }
		if ($route->end->cep != $_GET['cep'] and !in_array($route->end->city, $cities)) {
			$cities[] = $route->end->city ?>
			<option type="<?php echo 'end'; ?>" cep="<?php echo $route->end->cep; ?>" host="<?php echo $company->host; ?>" port="<?php echo $company->port; ?>" value="<?php echo $route->end->id; ?>">
				<?php echo $route->end->city; //. ' | ' . $route->end->cep . ' | ' . $route->end->name; ?>
			</option>
<?php }
	}
} ?>