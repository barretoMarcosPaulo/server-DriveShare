# Servidor <strong>Multithread</strong> para a plataforma DriveShare
Este repositório consiste na implementação de um servidor para a plataforma DriveShare. A sua função é gerenciar todas as conexões
e salvar todos os dados no banco de dados <strong>MYSQL</strong>

# Caracteristicas
1 - A implementação realizada garante que cada nova requisição seja executada em threads distintas;

2 - Toda a comunicação foi implementada utilizando sockets;

3 - Os registros são salvos por meio do SGBD MYSQL;

4 - O servidor atualiza as informações no client-side.

# Como utilizar

Para a execução do código siga os seguintes passos:

1 - Instale a biblioteca pymysql;

2 - Crie o banco de dados(o arquivo sql esta junto com o projeto);

3 - execute o arquivo <strong>server.py</strong>.
