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
		if (($route->start->cep == $_GET['cep_start'] and $route->end->cep == $_GET['cep_end']) or ($route->start->cep == $_GET['cep_end'] and $route->end->cep == $_GET['cep_start'])) {
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
				<?php if ($route->total_chairs - $route->filled_chairs <= 0) : ?>
					<div class="col-md-2"><label class="alert alert-danger">LOTADO</label></div>
				<?php else : ?>
					<div class="col-md-2"><button route="<?php echo $route->id; ?>" host="<?php echo $company->host ?>" port="<?php echo $company->port ?>" id="btn_confirm_<?php echo $route->id; ?>" class="btn-success btns btn-confirm">Confirmar</button></div>
				<?php endif; ?>
				<!-- <div class="col-md-2"><button <?php // echo $route->total_chairs - $route->filled_chairs <= 0 ? 'disabled' : '' 
													?> class="btn-success">Confirmar</button></div> -->
			</div>
<?php }
	}
}
?>
<script>
	$('.btns').click((event) => {
		const route = $(event.currentTarget).attr('route');
		const host = $(event.currentTarget).attr('host');
		const port = $(event.currentTarget).attr('port');
		let action = 'confirm';
		if ($('#btn_confirm_' + route).text() == 'Desconfirmar') {
			action = 'disconfirm';
		}
		console.log(action);
		$.ajax({
			type: "POST",
			url: "controllers/update_route.php",
			data: {
				id: route,
				action: action,
				port: port,
				host: host
			},
			beforeSend: (data) => {
				$('.btns').attr('disabled', 'true');
			},
			success: function(data) {
				response = JSON.parse(data)
				if (response.success) {
					if (action == 'disconfirm') {
						$('#btn_confirm_' + route).text('Confirmar');
						$('#btn_confirm_' + route).removeClass('btn-disconfirm');
						$('#btn_confirm_' + route).addClass('btn-confirm');
						$('#btn_confirm_' + route).removeClass('btn-danger');
						$('#btn_confirm_' + route).addClass('btn-success');
					} else {
						$('#btn_confirm_' + route).text('Desconfirmar');
						$('#btn_confirm_' + route).removeClass('btn-confirm');
						$('#btn_confirm_' + route).addClass('btn-disconfirm');
						$('#btn_confirm_' + route).removeClass('btn-success');
						$('#btn_confirm_' + route).addClass('btn-danger');
					}
					$('.btns').removeAttr('disabled');
					Swal.fire(
						response.data,
						'',
						'success'
					);
				} else {
					Swal.fire(
						'Houve um erro ao confirmar a passagem.',
						'Erro: ' + response.error,
						'error'
					);
				}

			},
			error: (data) => {
				$('.btns').attr('disabled', 'true');
				Swal.fire(
					'Parece que estamos offline, chame o TI.',
					'',
					'error'
				);
			}
		});
	});
</script>
<?php
if ($count == 0) {
?>
	<p class="h4 mb-0 text-center">Não há rotas para esta busca!</p>
<?php
}
?>