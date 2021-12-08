<?php

/**
 * Componente Curricular: MI Concorrência e Conectividade
 * Autor: Kevin Cerqueira Gomes e Esdras Abreu Silva
 *
 * Declaro que este código foi elaborado por mim de forma individual e
 * não contém nenhum trecho de código de outro colega ou de outro autor,
 * tais como provindos de livros e apostilas, e páginas ou documentos
 * eletrônicos da Internet. Qualquer trecho de código de outra autoria que
 * uma citação para o  não a minha está destacado com  autor e a fonte do
 * código, e estou ciente que estes trechos não serão considerados para fins
 * de avaliação. Alguns trechos do código podem coincidir com de outros
 * colegas pois estes foram discutidos em sessões tutorias.
 */
define('MYPATH', '');
include_once('pages/templates/header.php');
include_once('controllers/routes.php');
?>
<style>
	#menu .btn {
		width: 15rem;
		height: 10rem;
	}

	.container {
		position: relative;
		top: 50%;
		transform: translateY(-50%);
	}

	a {
		text-decoration: none;
		color: #FFF !important;
	}

	i {
		font-size: 25px !important;
	}

	.icon-g {
		color: #FFF;
		font-size: 50px !important;
	}
</style>
<title>Dashboard</title>
<div class="p-5 bg-light m-0" style="height: 100vh;">
	<div class="m-0">
		<div class="row bg-white p-3 rounded shadow-sm mb-5">
			<div class="row text-center mb-3">
				<div class="col-md-10 text-center">
					<p class="h2 m-0">
						123voos
					</p>
				</div>
				<div class="col-md-2 row">
					<div class="col-md-10">
						<label class="h5 m-0 mt-3">
						</label>
					</div>
					<div class="col-md-2">
						<label id="logout" class="btn text-dark">
							<i class="fa fa-sign-out text-dark" style="margin-top: 10px;"></i>
						</label>
					</div>
				</div>
				<div hidden id="alert-error" class="alert alert-danger mt-3" role="alert">
					<p id="alert-text-error" class="h5 m-0"></p>
				</div>
			</div>
		</div>
		<div id="menu" class="text-center bg-white p-3 rounded shadow">
			<div class="row mb-3">
				<?php if ($all_routes) { //var_dump($all_routes->companies[0]->routes[0]->start->cep);die(); 
				?>
					<div class="col-md-5">
						<div class="row">
							<div class="col-md-12"><label for="name-patient">Selecione a cidade de partida:</label>
								<select id="start" required name="start">
									<option selected id="default" value=""></option>
									<?php
									foreach ($all_routes->companies as $company) {
										foreach ($company->routes as $key => $route) {
									?>
											<option type="<?php echo 'start'; ?>" cep="<?php echo $route->start->cep; ?>" host="<?php echo $company->host; ?>" port="<?php echo $company->port; ?>" value="<?php echo $route->start->id; ?>">
												<?php echo $route->start->city . ' | ' . $route->start->cep . ' | ' . $route->start->name; ?>
											</option>
											<option type="<?php echo 'end'; ?>" cep="<?php echo $route->end->cep; ?>" host="<?php echo $company->host; ?>" port="<?php echo $company->port; ?>" value="<?php echo $route->end->id; ?>">
												<?php echo $route->end->city . ' | ' . $route->end->cep . ' | ' . $route->end->name; ?>
											</option>
									<?php }
									} ?>
								</select>
							</div>
						</div>
					</div>
					<div class="col-md-5">
						<div class="row">
							<div class="col-md-12"><label for="name-patient">Selecione a cidade de partida:</label>
								<select disabled id="end" required name="end">
									<option selected id="default" value=""></option>
								</select>
							</div>
						</div>
					</div>
					<div class="col-md-2">
						<div class="pt-4 rounded-3">
							<button disabled class="btn-success" id="btn-find">Buscar</button>
						</div>
					</div>
				<?php } else { ?>
					<div hidden id="alert-error" class="alert alert-danger" role="alert">
						<p id="alert-text-error" class="h5 m-0">Não há rotas para serem mostradas.</p>
					</div>
				<?php } ?>
			</div>
			<div>
				<p hidden id="loading" class="text-center-m-0 h2">carregando...</p>
				<div id="list-routes"></div>
			</div>
		</div>
	</div>
</div>
<script>
	$(document).ready(function() {
		$('#start').on('select2:select', (event) => {
			// console.log(($('#start').find(':selected').attr('cep')))
			$.ajax({
				type: "GET",
				url: "end.php?cep=" + $('#start').find(':selected').attr('cep'),
				beforeSend: (data) => {
					$('#btn-find').attr('disabled', 'true');
					$('#end').attr('disabled', 'true');
				},
				success: function(data) {
					$('#end').html(data);
					$('#end').removeAttr('disabled');
					$('#btn-find').removeAttr('disabled');
				},
				error: (data) => {
					alert('Erro na requisição');
					$('#end').attr('disabled', 'true');
					$('#btn-find').attr('disabled', 'true');
				}
			});
		});
		$('#btn-find').click((event) => {
			// console.log(($('#start').find(':selected').attr('cep')))
			$.ajax({
				type: "GET",
				url: "list_routes.php?start=" + $('#start').find(':selected').val() + '&end=' + $('#end').find(':selected').val(),
				beforeSend: (data) => {
					$('#loading').removeAttr('hidden');
				},
				success: function(data) {
					$('#loading').attr('hidden', 'true');
					$('#list-routes').html(data);
				},
				error: (data) => {
					$('#loading').removeAttr('hidden');

				}
			});
		});
	});
	$('#start').select2({
		placeholder: 'Selecione uma rota',
		dropdownAutoWidth: true,
		escapeMarkup: function(text) {
			return text;
		},
		width: "100%",
		language: "pt-BR",
		cache: true
	});

	$('#end').select2({
		placeholder: 'Selecione uma rota de chegada',
		dropdownAutoWidth: true,
		escapeMarkup: function(text) {
			return text;
		},
		width: "100%",
		language: "pt-BR",
		cache: true
	});
	// $('#get-route').submit(function(event) {
	// 		event.preventDefault();
	// 		let type = 'end';
	// 		let route = $('#start-route').find(':selected').val();
	// 		$.ajax({
	// 			type: "POST",
	// 			url: "<?php echo MYPATH; ?>Controllers/delete_patient.php",
	// 			data: {'type': type, 'route': route},
	// 			beforeSend: function() {
	// 				$('#btn-send').attr('hidden', '');
	// 			},
	// 			success: function(data) {
	// 				response = JSON.parse(data);
	// 				if (response.success) {
	// 					Swal.fire(
	// 						'Rota confirmada! ',
	// 						'',
	// 						'success'
	// 					);
	// 				} else {
	// 					Swal.fire(
	// 						'Houve um erro ao deletar o paciente.',
	// 						'Erro: ' + response.error,
	// 						'error'
	// 					);
	// 				}
	// 			},
	// 			error: function(data) {
	// 				Swal.fire(
	// 					'Parece que estamos offline, chame o TI.',
	// 					'',
	// 					'error'
	// 				);
	// 			},
	// 			complete: function() {
	// 				$('#btn-send').removeAttr('disabled');
	// 			}
	// 		});
	// 	});
</script>
<?php include_once('pages/templates/footer.php'); ?>