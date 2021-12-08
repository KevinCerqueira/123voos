<?php
include_once('controllers/routes.php');
?>
<div class="row">
	<div class="col-md-1">#</div>
	<div class="col-md-2">Compania</div>
	<div class="col-md-2">Valor</div>
	<div class="col-md-2">Cadeiras dísponíveis</div>
	<div class="col-md-1">Total Cadeiras</div>
	<div class="col-md-1">Tempo (m)</div>
	<div class="col-md-1">Distância (KM)</div>
	<div class="col-md-2">Ação</div>
</div>
<?php
$count = 0;
foreach ($all_routes->companies as $company) {
	foreach ($company->routes as $key => $route) {
		if (($route->start->id == $_GET['start'] and $route->end->id == $_GET['end']) or ($route->start->id == $_GET['end'] and $route->end->id == $_GET['start'])) {
			$count++;
?>
			<div class="row border p-1">
				<div class="col-md-1"><?php echo $count; ?></div>
				<div class="col-md-2"><?php echo $company->company; ?></div>
				<div class="col-md-2"><?php echo $route->value; ?></div>
				<div class="col-md-2"><?php echo $route->total_chairs - $route->filled_chairs; ?></div>
				<div class="col-md-1"><?php echo $route->total_chairs ?></div>
				<div class="col-md-1"><?php echo $route->time; ?></div>
				<div class="col-md-1"><?php echo $route->distance; ?></div>
				<div <?php echo $route->total_chairs - $route->filled_chairs <= 0 ? 'disabled' : '' ?> class="col-md-2"><button class="btn-success">Confirmar</button></div>
			</div>
	<?php }
	}
}
if ($count == 0) {
	?>
	<p class="h4 mb-0 text-center">Não há rotas para esta busca!</p>
<?php
}
?>