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
				<div class="col-md-4">
					<button class="btn btn-primary btn-block" data-bs-toggle="modal" data-bs-target="#register-patient">
						<p class="h2">Rotas</p>
					</button>
				</div>
			</div>
		</div>
	</div>
</div>
<?php include_once('pages/templates/footer.php'); ?>