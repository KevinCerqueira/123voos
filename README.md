# 123voos - Malha Aérea Compartilhada
O intuito deste problema foi a criação de uma malha de servidores para empresas aéreas as quais se comunicam entre si de forma delimitada e um sistema consome os dados desses servidores.
## Tecnologias utilizadas:
- Python 3.8
- PHP 7.4
- Javascript
- HTML5 & CSS3
### Biblotecas utilizadas
- Python:
    - pymongo (comunicação com banco de dados MongoDB)
    - socket TCP (servidor com socket puro)
    - threading (threads)
    - sys (comandos do sistema)
    - os (pastas e rotas do sistema)
- PHP
    - funções:
        - socket_create (criar cliente com socket puro)
        - socket_connect (conectar com o servidor)
        - socket_write (enviar dados ao servidor)
        - socket_recv (receber dados do servidor)
        - socket_close (fechar conexão com o servidor)
- Javascript
    - JQuery 3.6.0
        - Ajax
    - SweetAlert2
    - Select2
- HTML5 & CSS3
    - Boostrap 5.1
    - FontAwesome
## Como rodar:
1. Antes de tudo é necessário ter instalado o Python (versão 3.8) e o XAMPP (versão 3.3.0) + PHP (v7.4)
    - Python (v3.8.0): https://www.python.org/downloads/
    - XAMPP (v3.3.0) + PHP 7.4: https://www.apachefriends.org/pt_br/download.html
        - **ATENÇÃO**: Baixar o que consta a versão **7.4** do PHP. Não é necessário instalar o php à parte, pois o o mesmo já vem pré configurado no xampp
2. Caso utilize windows, é necessário verificar se o PHP do XAMPP está setado nas variáveis ambiente do seu computador.
    - ![variaveis](https://github.com/kevincerqueira/simcov2/blob/main/telas/variaveis.png?raw=true)
3. Para utilizar o socket do PHP é necessário habilita-lo no php.ini (C:\xampp\php\php.ini):
    - Basta pesquisar dentro do arquivo o nome 'sockets' e apagar o ponto e virgula (;) que fica na frente do mesmo.
        - ![phpini](https://github.com/kevincerqueira/simcov2/blob/main/telas/phpini.png?raw=true)
4. Feito tudo isso, confirme que está tudo funcionando, basta abrir o terminar e digitar 'python --version' para verificar se o Python foi instalado corretamente, e para verificar o PHP basta digitar no mesmo terminal 'php -v'. Feito isso confirme se as versões aparecem devidamente.
5. Após configurado, está na hora de mover o repositório para dentro da pasta C:\xampp\htdocs, como mostrado na imagem:
    - ![htdocs](https://github.com/kevincerqueira/simcov2/blob/main/telas/htdocs.png?raw=true)
6. Agora abra o XAMPP e dê start na opção Apache (o mesmo deve ficar verde):
    - ![xampp](https://github.com/kevincerqueira/simcov2/blob/main/telas/xampp.png?raw=true)
7. Agora instale as importações necessárias para o python:
```sh
pip install pymongo
```

```sh
pip install "pymongo[srv]"
```

8. Após isso, certifique-se que você tem a variável de ambiente CLUSTER no arquivo '123voos/server/src/.env', como no exemplo do .env.example:

   ```
   CLUSTER=mongodb+srv://<username>:<password>@kcluster.meacr.mongodb.net/test
   ```

   - caso não tenha acesso ao banco de dados, será necessário nos solicitar, ou criar um no site do MongoDB.

10. Pronto, agora o front-end da aplicação está rodando, agora é a hora de rodar os servidores. Vá no terminal e execute o arquivo 'main.py' dentro da pasta 'server/src' e quando aparecer uma tela de para imputar o nome da compania, digite 'anil', 'latim' ou 'goal' para iniciar um desses servidores (caso queira iniciar mais de um - até os 3 mesmo - é necessário abrir cada um em um terminal e fazer o mesmo processo, somente mudando o nome da compania) 
```sh
python main.py
```

11. Pronto! agora é só acessar a tela inicial do sistema, basta acessar o link 'http://localhost/123voos/web' em um navegador

## Telas: http://localhost/123voos/web/
- Dashboard: 
    - ![dashboard](https://github.com/kevincerqueira/123voos/blob/main/telas/1_inicial.png?raw=true)
- Selecionando partida:
    - ![partida](https://github.com/kevincerqueira/simcov2/blob/main/telas/2_selecionando_cidade_inicial.png?raw=true)
- Selecionando chegada:
    - ![chegada](https://github.com/kevincerqueira/simcov2/blob/main/telas/3_selecionando_cidade_final.png?raw=true)
- Carregando busca:
    - ![carregando](https://github.com/kevincerqueira/simcov2/blob/main/telas/4_carregando.png?raw=true)
- Resultados da busca:
    - ![busca](https://github.com/kevincerqueira/simcov2/blob/main/telas/5_busca_carregada.png?raw=true)
- Confirmando passagem:
    - ![confirmando](https://github.com/kevincerqueira/simcov2/blob/main/telas/6_confirmando_rota.png?raw=true)
- Desconfirmando passagem:
    - ![desconfirmando](https://github.com/kevincerqueira/simcov2/blob/main/telas/7_desconfirmando_rota.png?raw=true)

