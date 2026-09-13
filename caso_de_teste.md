# Plano de Testes Funcionais – TeVejo

## Histórico de Alterações

| Data | Versão | Descrição | Autor |
| :---: | :---: | :--- | :--- |
| 13/09/2026 | 1.0 | Elaboração dos casos de teste funcionais com Análise do Valor Limite (AVL) para os CDUs 003 e 011 | João Pedro Dantas Magalhães |

---

## 1. Introdução

Este documento especifica os testes que devem ser realizados para validar os casos de uso **CDU003 – Visualizar Conteúdo Educacional** e **CDU011 – Gerenciar Conteúdo Educacional** da plataforma web **TeVejo**. Ele contém as informações necessárias para a construção dos scripts e execução dos testes, como preparação do ambiente, dados de entrada, resultados esperados e aplicação formal do critério funcional de **Análise do Valor Limite (AVL)**.

### 1.1 Visão Geral do Documento

O documento está estruturado da seguinte forma:
* **Seção 2 – Testes Funcionais do CDU003 (Visualizar Conteúdo Educacional):** Especificação, análise de limites para consultas/listagens e casos de teste do fluxo principal e exceções.
* **Seção 3 – Testes Funcionais do CDU011 (Gerenciar Conteúdo Educacional):** Especificação, análise de limites dos campos cadastrais e casos de teste para criação, edição e exclusão de artigos informativos.
* **Seção 4 – Testes Não Funcionais:** Especificação dos testes de segurança de acesso e desempenho na carga dos conteúdos.
* **Seção 5 – Referências:** Relação das normas acadêmicas e materiais de apoio empregados.

---

## 2. Testes Funcionais – CDU003: Visualizar Conteúdo Educacional

### 2.1 Especificação do CDU
* **Ator Principal:** Convivente
* **Atores Secundários:** Curador
* **Resumo:** Descreve como o convivente acessa e visualiza os conteúdos educacionais curados e verificados disponíveis na plataforma TeVejo.
* **Pré-condição:** O convivente precisa estar logado no sistema e deve haver conteúdo educacional cadastrado.
* **Pós-condição:** O conteúdo educacional completo é exibido na interface para o usuário.

---

### 2.2 Classes de Equivalência

| Variável / Campo | Condições | Classes Válidas | Classes Inválidas | Resultado Esperado |
| :--- | :--- | :--- | :--- | :--- |
| `conteudo_id` | Identificador primário inteiro do artigo ($id \ge 1$) | Inteiro correspondente a um ID existente no banco | ID igual a zero ($0$), ID negativo ($< 0$), tipo não numérico | Válido retorna HTTP 200 com payload completo; Inválido retorna HTTP 400 ou 404 |
| `quantidade_conteudos` | Quantidade de conteúdos publicados na base ($N \ge 0$) | $N \ge 1$ artigos cadastrados | $N = 0$ artigos cadastrados | Válido lista os cards; Inválido exibe mensagem de nenhum conteúdo disponível |
| `autenticacao` | Sessão ativa e perfil do usuário logado | Usuário autenticado com token válido | Usuário sem token (anônimo) ou com token expirado | Válido permite navegação; Inválido retorna HTTP 401/403 e direciona para login |
| `filtro_tag` / `busca` | Tamanho da string de busca ($1 \le len(tag) \le 30$) | String com tamanho entre 1 e 30 caracteres | String vazia ($0$ caracteres), tamanho superior a 30 caracteres | Válido filtra a listagem; Inválido acima do limite retorna HTTP 400 |

---

### 2.3 Análise do Valor Limite (AVL)

#### 1) `quantidade_conteudos` (Fronteira da listagem de conteúdos)
Faixa válida para visualização de lista preenchida: $N \ge 1$ artigos.

| Caso | Entrada / Condição | Resultado Esperado |
| :--- | :--- | :--- |
| Limite inferior inválido | $N = 0$ artigos no banco | HTTP 200; lista vazia `[]`; exibe a mensagem: "Nenhum conteúdo educacional disponível no momento." (Fluxo de Exceção I) |
| Limite inferior válido | $N = 1$ artigo no banco | HTTP 200; lista renderiza exatamente 1 card com título, tipo e autor curador |
| Valor nominal válido | $N = 5$ artigos no banco | HTTP 200; lista renderiza 5 cards estruturados |

#### 2) `conteudo_id` (Identificador numérico do artigo selecionado)
Faixa válida de IDs persistidos: $id \in [1, \infty)$.

| Caso | Entrada / Condição | Resultado Esperado |
| :--- | :--- | :--- |
| Imediatamente abaixo do mínimo | `conteudo_id = 0` | HTTP 400 / 404; identificador inválido |
| Limite inferior válido | `conteudo_id = 1` (artigo existente) | HTTP 200; exibe o artigo completo (título, texto, tags e autor) |
| Valor inexistente (fronteira de busca) | `conteudo_id = 999999` (não cadastrado) | HTTP 404; exibe: "Não foi possível carregar o conteúdo. Tente novamente mais tarde." (Fluxo de Exceção II) |
| Tipo de dado inválido | `conteudo_id = "abc"` | HTTP 400 Bad Request; parâmetro deve ser inteiro |

#### 3) `filtro_tag` / `busca` (Tamanho da string de consulta)
Faixa válida: $1 \le len(termo) \le 30$ caracteres.

| Caso | Entrada / Condição | Resultado Esperado |
| :--- | :--- | :--- |
| Abaixo do limite inferior | $len(termo) = 0$ (`""`) | HTTP 200; termo de busca ignorado, listando todos os artigos |
| Limite inferior válido | $len(termo) = 1$ (`"A"`) | HTTP 200; retorna apenas conteúdos com a ocorrência da letra "A" |
| Limite superior válido | $len(termo) = 30$ (string com 30 caracteres) | HTTP 200; filtra conteúdos aplicando a string limite |
| Imediatamente acima do máximo | $len(termo) = 31$ (string com 31 caracteres) | HTTP 400; mensagem: "Termo de busca excede o limite de 30 caracteres." |

---

### 2.4 Casos de Teste – CDU003

| ID | Cenário / Entrada 1 (`auth`) | Entrada 2 (`conteudo_id`) | Entrada 3 (`quantidade_conteudos`) | Entrada 4 (`filtro_tag`) | Resultado Esperado | Resultado Obtido | Situação |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **CT01** | Convivente logado | N/A (Listagem geral) | $N = 0$ (Vazio) | N/A | HTTP 200, exibe "Nenhum conteúdo educacional disponível no momento." | - | Não executado |
| **CT02** | Convivente logado | N/A (Listagem geral) | $N = 1$ (Limite inferior) | N/A | HTTP 200, exibe listagem com exatamente 1 artigo curado | - | Não executado |
| **CT03** | Convivente logado | $id = 1$ (Existente) | $N \ge 1$ | N/A | HTTP 200, abre tela do artigo com texto completo e dados do curador | - | Não executado |
| **CT04** | Convivente logado | $id = 0$ (Inválido limite) | $N \ge 1$ | N/A | HTTP 400 / 404, exibe "Não foi possível carregar o conteúdo." | - | Não executado |
| **CT05** | Convivente logado | $id = 999999$ (Inexistente) | $N \ge 1$ | N/A | HTTP 404, exibe "Não foi possível carregar o conteúdo. Tente novamente mais tarde." | - | Não executado |
| **CT06** | Convivente logado | N/A | $N \ge 1$ | $len(tag) = 1$ (`"A"`) | HTTP 200, filtra artigos correspondentes à tag | - | Não executado |
| **CT07** | Convivente logado | N/A | $N \ge 1$ | $len(tag) = 31$ (Inválido) | HTTP 400, "Termo de busca excede o limite de 30 caracteres." | - | Não executado |
| **CT08** | Usuário não autenticado (anônimo) | $id = 1$ | $N \ge 1$ | N/A | HTTP 401 Unauthorized / Redirecionamento obrigatório para login | - | Não executado |

---

## 3. Testes Funcionais – CDU011: Gerenciar Conteúdo Educacional

### 3.1 Especificação do CDU
* **Ator Principal:** Curador
* **Atores Secundários:** Não existe
* **Resumo:** Descreve como o curador cadastra, edita e remove conteúdos educacionais da plataforma TeVejo para manter informações confiáveis sobre TEA.
* **Pré-condição:** O usuário deve estar autenticado com perfil de curador ativo.
* **Pós-condição:** O conteúdo é persistido, atualizado ou removido do banco de dados com registro de autoria e data.

---

### 3.2 Classes de Equivalência

| Campo | Regra / Condição | Classes Válidas | Classes Inválidas | Resultado Esperado |
| :--- | :--- | :--- | :--- | :--- |
| `titulo` | Texto obrigatório; $5 \le len(titulo) \le 120$ caracteres | $5 \le len(titulo) \le 120$ caracteres | Vazio, ausente, $len < 5$, $len > 120$ caracteres | Inválido retorna HTTP 400 com erro no campo `titulo` |
| `fonte` | Texto obrigatório; $3 \le len(fonte) \le 100$ caracteres | $3 \le len(fonte) \le 100$ caracteres | Vazio, ausente, $len < 3$, $len > 100$ caracteres | Inválido retorna HTTP 400 com erro no campo `fonte` |
| `corpo` | Texto obrigatório; $20 \le len(corpo) \le 10000$ caracteres | $20 \le len(corpo) \le 10000$ caracteres | Vazio, ausente, $len < 20$, $len > 10000$ caracteres | Inválido retorna HTTP 400 com erro no campo `corpo` |
| `tags` | M2M obrigatório; $1 \le count(tags) \le 5$ tags selecionadas | Lista com 1 a 5 tags válidas | Lista vazia ($0$), lista com mais de 5 tags ($> 5$) | Inválido retorna HTTP 400 com erro de seleção de tags |
| `anexo` | Opcional; formatos permitidos: PDF, JPG, PNG; tamanho $\le 5.0$ MB | Arquivo de $0.1$ MB até $5.0$ MB; sem arquivo (`null`) | Arquivo com tamanho $> 5.0$ MB; formato não suportado | Inválido retorna HTTP 400 com erro de validação de arquivo |
| `perfil` | Permissão de acesso via token | Usuário logado pertencente ao grupo Curador | Usuário com perfil Convivente, usuário anônimo | Sem permissão retorna HTTP 403 Forbidden |

---

### 3.3 Análise do Valor Limite (AVL)

#### 1) `titulo` (Faixa válida: $[5, 120]$ caracteres)
Valores de fronteira testados: $\{4, 5, 120, 121\}$.

| Caso | Entrada | Resultado Esperado |
| :--- | :--- | :--- |
| Um caractere abaixo do mínimo | `len(titulo) = 4` (`"TEA1"`) | HTTP 400 Bad Request; "Título deve conter no mínimo 5 caracteres." |
| Limite inferior válido | `len(titulo) = 5` (`"Rotin"`) | Validação aceita com sucesso |
| Limite superior válido | `len(titulo) = 120` (string de 120 caracteres) | Validação aceita com sucesso |
| Um caractere acima do máximo | `len(titulo) = 121` (string de 121 caracteres) | HTTP 400 Bad Request; "Título não pode exceder 120 caracteres." |

#### 2) `fonte` (Faixa válida: $[3, 100]$ caracteres)
Valores de fronteira testados: $\{2, 3, 100, 101\}$.

| Caso | Entrada | Resultado Esperado |
| :--- | :--- | :--- |
| Um caractere abaixo do mínimo | `len(fonte) = 2` (`"MS"`) | HTTP 400 Bad Request; "Fonte deve conter no mínimo 3 caracteres." |
| Limite inferior válido | `len(fonte) = 3` (`"SBP"`) | Validação aceita com sucesso |
| Limite superior válido | `len(fonte) = 100` (string de 100 caracteres) | Validação aceita com sucesso |
| Um caractere acima do máximo | `len(fonte) = 101` (string de 101 caracteres) | HTTP 400 Bad Request; "Fonte não pode exceder 100 caracteres." |

#### 3) `corpo` (Faixa válida: $[20, 10000]$ caracteres)
Valores de fronteira testados: $\{19, 20, 10000, 10001\}$.

| Caso | Entrada | Resultado Esperado |
| :--- | :--- | :--- |
| Um caractere abaixo do mínimo | `len(corpo) = 19` (19 caracteres) | HTTP 400 Bad Request; "O texto do conteúdo deve conter no mínimo 20 caracteres." |
| Limite inferior válido | `len(corpo) = 20` (20 caracteres) | Validação aceita com sucesso |
| Limite superior válido | `len(corpo) = 10000` (10000 caracteres) | Validação aceita com sucesso |
| Um caractere acima do máximo | `len(corpo) = 10001` (10001 caracteres) | HTTP 400 Bad Request; "O texto do conteúdo não pode ultrapassar 10000 caracteres." |

#### 4) `tags` (Faixa válida de quantidade: $[1, 5]$ tags)
Valores de fronteira testados: $\{0, 1, 5, 6\}$.

| Caso | Entrada | Resultado Esperado |
| :--- | :--- | :--- |
| Abaixo do limite mínimo | `count(tags) = 0` (array vazio `[]`) | HTTP 400 Bad Request; "Selecione pelo menos 1 tag." |
| Limite inferior válido | `count(tags) = 1` (`["TEA"]`) | Validação aceita com sucesso |
| Limite superior válido | `count(tags) = 5` (`["TEA", "Rotina", "Inclusao", "Escola", "Familia"]`) | Validação aceita com sucesso |
| Acima do limite máximo | `count(tags) = 6` (array com 6 tags) | HTTP 400 Bad Request; "Número máximo de 5 tags excedido." |

#### 5) `anexo` (Faixa válida: $\le 5.0$ MB)
Valores de fronteira testados: $\{0.0 \text{ MB}, 5.0 \text{ MB}, 5.1 \text{ MB}\}$.

| Caso | Entrada | Resultado Esperado |
| :--- | :--- | :--- |
| Sem arquivo enviado | Sem anexo (`None`) | Validação aceita; conteúdo salvo sem anexo |
| Limite superior válido | Arquivo PDF de exatamente `5.0 MB` | Validação aceita; arquivo anexado com sucesso |
| Acima do limite superior | Arquivo PDF de `5.1 MB` | HTTP 400 Bad Request; "O tamanho do anexo não pode ser maior que 5 MB." |

---

### 3.4 Casos de Teste – CDU011

#### 3.4.1 Fluxo Principal: Adicionar Conteúdo Educacional

| ID | Perfil Ator | `titulo` | `fonte` | `corpo` | `tags` | `anexo` | Resultado Esperado | Resultado Obtido | Situação |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **CT09** | Curador | `len = 5` | `len = 3` | `len = 20` | 1 tag | Nenhum | HTTP 201 Created; conteúdo salvo com autoria e data | - | Não executado |
| **CT10** | Curador | `len = 120` | `len = 100` | `len = 10000` | 5 tags | PDF 5.0 MB | HTTP 201 Created; conteúdo salvo com metadados e anexo | - | Não executado |
| **CT11** | Curador | `len = 4` | `len = 10` | `len = 50` | 2 tags | Nenhum | HTTP 400; "Título deve conter no mínimo 5 caracteres." | - | Não executado |
| **CT12** | Curador | `len = 121` | `len = 10` | `len = 50` | 2 tags | Nenhum | HTTP 400; "Título não pode exceder 120 caracteres." | - | Não executado |
| **CT13** | Curador | `len = 30` | `len = 2` | `len = 50` | 2 tags | Nenhum | HTTP 400; "Fonte deve conter no mínimo 3 caracteres." | - | Não executado |
| **CT14** | Curador | `len = 30` | `len = 101` | `len = 50` | 2 tags | Nenhum | HTTP 400; "Fonte não pode exceder 100 caracteres." | - | Não executado |
| **CT15** | Curador | `len = 30` | `len = 10` | `len = 19` | 2 tags | Nenhum | HTTP 400; "O texto do conteúdo deve conter no mínimo 20 caracteres." | - | Não executado |
| **CT16** | Curador | `len = 30` | `len = 10` | `len = 10001` | 2 tags | Nenhum | HTTP 400; "O texto do conteúdo não pode ultrapassar 10000 caracteres." | - | Não executado |
| **CT17** | Curador | `len = 30` | `len = 10` | `len = 50` | 0 tags | Nenhum | HTTP 400; "Selecione pelo menos 1 tag." | - | Não executado |
| **CT18** | Curador | `len = 30` | `len = 10` | `len = 50` | 6 tags | Nenhum | HTTP 400; "Número máximo de 5 tags excedido." | - | Não executado |
| **CT19** | Curador | `len = 30` | `len = 10` | `len = 50` | 2 tags | PDF 5.1 MB | HTTP 400; "O tamanho do anexo não pode ser maior que 5 MB." | - | Não executado |
| **CT20** | Convivente | `len = 30` | `len = 10` | `len = 50` | 2 tags | Nenhum | HTTP 403 Forbidden; "Usuário não possui perfil de curador." | - | Não executado |

---

#### 3.4.2 Fluxo Alternativo I: Editar Conteúdo Existente

| ID | Perfil Ator | `conteudo_id` | Campo Alterado | Valor Inserido | Resultado Esperado | Resultado Obtido | Situação |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **CT21** | Curador | Existente ($id = 1$) | `titulo` | String com 5 caracteres (Limite inferior) | HTTP 200; "Conteúdo atualizado com sucesso." | - | Não executado |
| **CT22** | Curador | Existente ($id = 1$) | `titulo` | String com 121 caracteres (Limite acima) | HTTP 400; dados não alterados; erro de validação | - | Não executado |
| **CT23** | Curador | Existente ($id = 1$) | `tags` | Array vazio `[]` (0 tags) | HTTP 400; "Selecione pelo menos 1 tag." | - | Não executado |
| **CT24** | Curador | Inexistente ($id = 9999$) | Qualquer | Qualquer alteração | HTTP 404 Not Found; artigo não localizado | - | Não executado |

---

#### 3.4.3 Fluxo Alternativo II: Remover Conteúdo

| ID | Perfil Ator | `conteudo_id` | Confirmação | Resultado Esperado | Resultado Obtido | Situação |
| :---: | :--- | :--- | :---: | :--- | :---: | :---: |
| **CT25** | Curador | Existente ($id = 1$) | Confirmado (`Sim`) | HTTP 200 / 204 No Content; registro excluído; mensagem de sucesso | - | Não executado |
| **CT26** | Curador | Existente ($id = 1$) | Rejeitado (`Cancelar`) | Exclusão abortada; conteúdo mantido na base | - | Não executado |
| **CT27** | Curador | Inexistente ($id = 9999$) | Confirmado (`Sim`) | HTTP 404 Not Found; registro não encontrado | - | Não executado |
| **CT28** | Convivente | Existente ($id = 1$) | Confirmado (`Sim`) | HTTP 403 Forbidden; apenas curadores podem excluir conteúdos | - | Não executado |

---

## 4. Testes Não Funcionais

### 4.1 RNF01 – Segurança e Controle de Acesso (LGPD e Perfis)
* **Categoria:** Segurança
* **Automatizado:** Sim (via testes de integração Django REST Framework / `APITestCase`)
* **Duração Estimada:** 5 minutos
* **Executado:** Não
* **Responsável:** João Pedro Dantas Magalhães
* **Data:** 13/09/2026
* **Procedimentos:** Enviar requisições `POST`, `PUT` e `DELETE` para o endpoint `/api/conteudos/` utilizando tokens JWT pertencentes a usuários com perfil de convivente padrão e tokens de usuários anônimos.
* **Critérios de Aceitação:** O sistema deve barrar 100% das tentativas de escrita com respostas HTTP 401 Unauthorized ou HTTP 403 Forbidden, garantindo que somente curadores alterem o repositório educacional (RN01).
* **Resultado:** Não executado.

### 4.2 RNF02 – Desempenho na Recuperação de Conteúdo
* **Categoria:** Desempenho
* **Automatizado:** Sim
* **Duração Estimada:** 10 minutos
* **Executado:** Não
* **Responsável:** Ramon Couto Santos
* **Data:** 13/09/2026
* **Procedimentos:** Executar requisições concorrentes de leitura (`GET /api/conteudos/`) simulando 50 acessos simultâneos de conviventes em ambiente Render.
* **Critérios de Aceitação:** O tempo médio de resposta para a carga completa do payload do artigo deve ser inferior a 1,5 segundo em 95% das requisições.
* **Resultado:** Não executado.

---

## 5. Referências

1. FREIRE, Marília A. **Teste de Software: Técnicas e Critérios de Testes – Particionamento em Classes de Equivalência e Análise do Valor Limite**. Natal: IFRN, 2025.
2. TEVEJO. **Documento de Visão e Glossário de Negócio do Projeto TeVejo**. Natal: IFRN, 2026.
3. TEVEJO. **Detalhamentos dos Casos de Uso CDU003 e CDU011**. Natal: IFRN, 2026.
4. IFRN. **Documentos de Casos de Teste dos Projetos Conta Comigo e Bizzu**. Natal: IFRN, 2025/2026.
5. IFRN. **Modelo Padrão de Caso de Teste (caso_de_teste.dot)**. Natal: IFRN.
