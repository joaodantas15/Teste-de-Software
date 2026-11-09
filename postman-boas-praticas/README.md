# 10 Boas Práticas de Teste de API com Postman

Atividade prática da disciplina de **Teste de Software**, aplicando as 10 boas práticas de validação de API REST utilizando o **Postman** e a API **JSONPlaceholder**.

## Estrutura da Collection (`collection_10_boas_praticas.json`)

| Requisição | Método e Endpoint | Práticas Validadas |
| :--- | :--- | :--- |
| **01 - GET Post** | `GET /posts/1` | **1.** Status Code `200`<br>**2.** Campos obrigatórios (`userId`, `id`, `title`, `body`)<br>**3.** Header `Content-Type` (`application/json; charset=utf-8`)<br>**4.** Corpo em formato JSON válido<br>**5.** Regra de negócio (`id === 1`)<br>**6.** Performance (Tempo de resposta `< 2000ms`) |
| **02 - GET Post Inexistente** | `GET /posts/99999` | **7.** Tratamento de erro (`404 Not Found`) |
| **03 - POST Criar Post** | `POST /posts` | **8.** Simulação de Autenticação (`Bearer Token`) e criação (`201 Created`) |
| **04 - GET Lista de Posts** | `GET /posts` | **9.** Paginação e retorno estruturado em lista (`Array`) |
| **10 - GET SQL Injection** | `GET /posts?userId=' OR 1=1 --` | **10.** Verificação de segurança contra SQL Injection (Não retorna erro `500`) |

## Como Importar e Executar no Postman
1. Abra o **Postman** e clique em **Import** no painel esquerdo.
2. Selecione o arquivo `collection_10_boas_praticas.json` contido nesta pasta.
3. Clique nos três pontos (`...`) da Collection **Testes API - JSONPlaceholder** > **Run** para executar todos os 10 testes automatizados de uma só vez.
