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
/** Classe responsável por enviar e receber informações do servidor. */
class RoutesController
{
    public $count_bytes = 8192;
    public $socket;

    /** Construtor */
    public function __construct()
    {
    }

    /** Coneceta no servidor */
    private function connect(Array $addr = null)
    {
		$addr = $addr ?? $this->getLeader();
        $this->socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);

        socket_connect($this->socket, $addr['host'], intval($addr['port']));
    }

    /** Fecha a conexão com o servidor */
    private function close()
    {
        return socket_close($this->socket);
    }

    /** Envia determinada informação e recebe do servidor */
    public function send(string $url, array $data = null)
    {
        $request = $url;

        if (!empty($data))
            $request .= ' ' . strval(json_encode($data));

        // Envia informação para o servidor
        $response = socket_write($this->socket, $request, strlen($request));
        
        socket_recv($this->socket, $response, $this->count_bytes, MSG_WAITALL);
        $this->close();
        return json_decode($response);
    }

    /** Confirma a rota */
    public function confirmRoute(String $route, Array $addr)
    {
        $this->connect($addr);

        $response = $this->send("confirm-route", ['route' => $route]);

        return $response;
    }
    
    /** Desconfirma a rota */
    public function disconfirmRoute(String $route, Array $addr)
    {
        $this->connect($addr);

        $response = $this->send("disconfirm-route", ['route' => $route]);

        return $response;
    }

    /** Retorna quem é o líder do servidor */
    public function getLeader()
    {
        $this->connect(['host' => 'localhost', 'port' => 8000]);
        $response = $this->send('who-leader');
        if($response->success){
            return ['host' => $response->data->host, 'port' => $response->data->port];
        }
		return ['host' => 'localhost', 'port' => 8000];
    }
    
	/** Retorna quem é o lídr do servidor */
    public function closeAllServers(Array $addr)
    {
        $this->connect($addr);
        try{
			$response = $this->send('close');
			return $response;
		}catch(Exception $e){
		}
		return 'Sem resposta';
    }
    
    /** Retorna todas as rotas */
    public function getAll()
    {
        // $this->connect(['host'=> 'localhost', 'port'=> 8100]);
        $this->connect();
        return $this->send("get-all-routes");
    }
    
	/** Retorna uma rota */
    public function get(String $type, String $value)
    {
        $this->connect();
        return $this->send("get-route", ['type' => $type, 'value' => $value]);
    }
}
