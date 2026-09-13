# Plano de Testes Funcionais – TeVejo

## Histórico de Alterações

| Data | Versão | Descrição | Autor |
| :---: | :---: | :--- | :--- |
| 13/09/2026 | 1.0 | Elaboração dos casos de teste funcionais com Análise do Valor Limite (AVL) para os CDUs 003 e 011[cite: 5, 6, 11, 12, 14] | João Pedro Dantas Magalhães[cite: 1] |

---

## 1. Introdução

Este documento especifica os testes que devem ser realizados para validar os casos de uso **CDU003 – Visualizar Conteúdo Educacional** e **CDU011 – Gerenciar Conteúdo Educacional** da plataforma web **TeVejo**[cite: 11, 12, 13]. Ele contém as informações necessárias para a construção dos scripts e execução dos testes, como preparação do ambiente, dados de entrada, resultados esperados e aplicação formal do critério funcional de **Análise do Valor Limite (AVL)**[cite: 5, 6, 13, 14].

### 1.1 Visão Geral do Documento

O documento está estruturado da seguinte forma[cite: 13, 14]:
* **Seção 2 – Testes Funcionais do CDU003 (Visualizar Conteúdo Educacional):** Especificação, análise de limites para consultas/listagens e casos de teste do fluxo principal e exceções[cite: 6, 11, 13].
* **Seção 3 – Testes Funcionais do CDU011 (Gerenciar Conteúdo Educacional):** Especificação, análise de limites dos campos cadastrais e casos de teste para criação, edição e exclusão de artigos informativos[cite: 6, 12, 13].
* **Seção 4 – Testes Não Funcionais:** Especificação dos testes de segurança de acesso e desempenho na carga dos conteúdos[cite: 4, 13].
* **Seção 5 – Referências:** Relação das normas acadêmicas e materiais de apoio empregados[cite: 13].

---

## 2. Testes Funcionais – CDU003: Visualizar Conteúdo Educacional

### 2.1 Especificação do CDU
* **Ator Principal:** Convivente[cite: 11]
* **Atores Secundários:** Curador[cite: 11]
* **Resumo:** Descreve como o convivente acessa e visualiza os conteúdos educacionais curados e verificados disponíveis na plataforma TeVejo[cite: 2, 11].
* **Pré-condição:** O convivente precisa estar logado no sistema e deve haver conteúdo educacional cadastrado[cite: 11].
* **Pós-condição:** O conteúdo educacional completo é exibido na interface para o usuário[cite: 11].

---

### 2.2 Classes de Equivalência

| Variável / Campo | Condições | Classes Válidas | Classes Inválidas | Resultado Esperado |
| :--- | :--- | :--- | :--- | :--- |
| `conteudo_id` | Identificador primário inteiro do artigo ($id \ge 1$)[cite: 5, 6] | Inteiro correspondente a um ID existente no banco[cite: 5, 6] | ID igual a zero ($0$), ID negativo ($< 0$), tipo não numérico[cite: 5, 6] | Válido retorna HTTP 200 com payload completo; Inválido retorna HTTP 400 ou 404[cite: 11, 14] |
| `quantidade_conteudos` | Quantidade de conteúdos publicados na base ($N \ge 0$)[cite: 6] | $N \ge 1$ artigos cadastrados[cite: 6] | $N = 0$ artigos cadastrados[cite: 6, 11] | Válido lista os cards; Inválido exibe mensagem de nenhum conteúdo disponível[cite: 11] |
| `autenticacao` | Sessão ativa e perfil do usuário logado[cite: 11] | Usuário autenticado com token válido[cite: 11] | Usuário sem token (anônimo) ou com token expirado[cite: 4, 11] | Válido permite navegação; Inválido retorna HTTP 401/403 e direciona para login[cite: 4, 11, 14] |
| `filtro_tag` / `busca` | Tamanho da string de busca ($1 \le len(tag) \le 30$)[cite: 5, 6] | String com tamanho entre 1 e 30 caracteres[cite: 5, 6] | String vazia ($0$ caracteres), tamanho superior a 30 caracteres[cite: 5, 6] | Válido filtra a listagem; Inválido acima do limite retorna HTTP 400[cite: 6, 14] |

---

### 2.3 Análise do Valor Limite (AVL)

#### 1) `quantidade_conteudos` (Fronteira da listagem de conteúdos)
Faixa válida para visualização de lista preenchida: $N \ge 1$ artigos[cite: 6].

| Caso | Entrada / Condição | Resultado Esperado |
| :--- | :--- | :--- |
| Limite inferior inválido | $N = 0$ artigos no banco[cite: 6] | HTTP 200; lista vazia `[]`; exibe a mensagem: "Nenhum conteúdo educacional disponível no momento." (Fluxo de Exceção I)[cite: 11] |
| Limite inferior válido | $N = 1$ artigo no banco[cite: 6] | HTTP 200; lista renderiza exatamente 1 card com título, tipo e autor curador[cite: 11] |
| Valor nominal válido | $N = 5$ artigos no banco[cite: 6] | HTTP 200; lista renderiza 5 cards estruturados[cite: 11] |

#### 2) `conteudo_id` (Identificador numérico do artigo selecionado)
Faixa válida de IDs persistidos: $id \in [1, \infty)$[cite: 6].

| Caso | Entrada / Condição | Resultado Esperado |
| :--- | :--- | :--- |
| Imediatamente abaixo do mínimo | `conteudo_id = 0`[cite: 6] | HTTP 400 / 404; identificador inválido[cite: 6, 14] |
| Limite inferior válido | `conteudo_id = 1` (artigo existente)[cite: 6] | HTTP 200; exibe o artigo completo (título, texto, tags e autor)[cite: 11] |
| Valor inexistente (fronteira de busca) | `conteudo_id = 999999` (não cadastrado)[cite: 6, 14] | HTTP 404; exibe: "Não foi possível carregar o conteúdo. Tente novamente mais tarde." (Fluxo de Exceção II)[cite: 11, 14] |
| Tipo de dado inválido | `conteudo_id = "abc"`[cite: 5, 14] | HTTP 400 Bad Request; parâmetro deve ser inteiro[cite: 14] |

#### 3) `filtro_tag` / `busca` (Tamanho da string de consulta)
Faixa válida: $1 \le len(termo) \le 30$ caracteres[cite: 6].

| Caso | Entrada / Condição | Resultado Esperado |
| :--- | :--- | :--- |
| Abaixo do limite inferior | $len(termo) = 0$ (`""`)[cite: 6] | HTTP 200; termo de busca ignorado, listando todos os artigos[cite: 14] |
| Limite inferior válido | $len(termo) = 1$ (`"A"`)[cite: 6] | HTTP 200; retorna apenas conteúdos com a ocorrência da letra "A"[cite: 6, 14] |
| Limite superior válido | $len(termo) = 30$ (string com 30 caracteres)[cite: 6] | HTTP 200; filtra conteúdos aplicando a string limite[cite: 6] |
| Imediatamente acima do máximo | $len(termo) = 31$ (string com 31 caracteres)[cite: 6] | HTTP 400; mensagem: "Termo de busca excede o limite de 30 caracteres."[cite: 6, 14] |

---

### 2.4 Casos de Teste – CDU003

| ID | Cenário / Entrada 1 (`auth`) | Entrada 2 (`conteudo_id`) | Entrada 3 (`quantidade_conteudos`) | Entrada 4 (`filtro_tag`) | Resultado Esperado | Resultado Obtido | Situação |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **CT01** | Convivente logado[cite: 11] | N/A (Listagem geral) | $N = 0$ (Vazio)[cite: 6] | N/A | HTTP 200, exibe "Nenhum conteúdo educacional disponível no momento."[cite: 11] | - | Não executado[cite: 14] |
| **CT02** | Convivente logado[cite: 11] | N/A (Listagem geral) | $N = 1$ (Limite inferior)[cite: 6] | N/A | HTTP 200, exibe listagem com exatamente 1 artigo curado[cite: 6, 11] | - | Não executado[cite: 14] |
| **CT03** | Convivente logado[cite: 11] | $id = 1$ (Existente)[cite: 6] | $N \ge 1$ | N/A | HTTP 200, abre tela do artigo com texto completo e dados do curador[cite: 11] | - | Não executado[cite: 14] |
| **CT04** | Convivente logado[cite: 11] | $id = 0$ (Inválido limite)[cite: 6] | $N \ge 1$ | N/A | HTTP 400 / 404, exibe "Não foi possível carregar o conteúdo."[cite: 11] | - | Não executado[cite: 14] |
| **CT05** | Convivente logado[cite: 11] | $id = 999999$ (Inexistente)[cite: 6, 14] | $N \ge 1$ | N/A | HTTP 404, exibe "Não foi possível carregar o conteúdo. Tente novamente mais tarde."[cite: 11] | - | Não executado[cite: 14] |
| **CT06** | Convivente logado[cite: 11] | N/A | $N \ge 1$ | $len(tag) = 1$ (`"A"`)[cite: 6] | HTTP 200, filtra artigos correspondentes à tag[cite: 6, 14] | - | Não executado[cite: 14] |
| **CT07** | Convivente logado[cite: 11] | N/A | $N \ge 1$ | $len(tag) = 31$ (Inválido)[cite: 6] | HTTP 400, "Termo de busca excede o limite de 30 caracteres."[cite: 6, 14] | - | Não executado[cite: 14] |
| **CT08** | Usuário não autenticado (anônimo)[cite: 4, 11] | $id = 1$ | $N \ge 1$ | N/A | HTTP 401 Unauthorized / Redirecionamento obrigatório para login[cite: 4, 11, 14] | - | Não executado[cite: 14] |

---

## 3. Testes Funcionais – CDU011: Gerenciar Conteúdo Educacional

### 3.1 Especificação do CDU
* **Ator Principal:** Curador[cite: 12]
* **Atores Secundários:** Não existe[cite: 12]
* **Resumo:** Descreve como o curador cadastra, edita e remove conteúdos educacionais da plataforma TeVejo para manter informações confiáveis sobre TEA[cite: 2, 4, 12].
* **Pré-condição:** O usuário deve estar autenticado com perfil de curador ativo[cite: 12].
* **Pós-condição:** O conteúdo é persistido, atualizado ou removido do banco de dados com registro de autoria e data[cite: 12].

---

### 3.2 Classes de Equivalência

| Campo | Regra / Condição | Classes Válidas | Classes Inválidas | Resultado Esperado |
| :--- | :--- | :--- | :--- | :--- |
| `titulo` | Texto obrigatório; $5 \le len(titulo) \le 120$ caracteres[cite: 5, 6, 12] | $5 \le len(titulo) \le 120$ caracteres[cite: 5, 6] | Vazio, ausente, $len < 5$, $len > 120$ caracteres[cite: 5, 6] | Inválido retorna HTTP 400 com erro no campo `titulo`[cite: 14] |
| `fonte` | Texto obrigatório; $3 \le len(fonte) \le 100$ caracteres[cite: 5, 6, 12] | $3 \le len(fonte) \le 100$ caracteres[cite: 5, 6] | Vazio, ausente, $len < 3$, $len > 100$ caracteres[cite: 5, 6] | Inválido retorna HTTP 400 com erro no campo `fonte`[cite: 14] |
| `corpo` | Texto obrigatório; $20 \le len(corpo) \le 10000$ caracteres[cite: 5, 6, 12] | $20 \le len(corpo) \le 10000$ caracteres[cite: 5, 6] | Vazio, ausente, $len < 20$, $len > 10000$ caracteres[cite: 5, 6] | Inválido retorna HTTP 400 com erro no campo `corpo`[cite: 14] |
| `tags` | M2M obrigatório; $1 \le count(tags) \le 5$ tags selecionadas[cite: 5, 6, 12] | Lista com 1 a 5 tags válidas[cite: 5, 6] | Lista vazia ($0$), lista com mais de 5 tags ($> 5$)[cite: 5, 6] | Inválido retorna HTTP 400 com erro de seleção de tags[cite: 14] |
| `anexo` | Opcional; formatos permitidos: PDF, JPG, PNG; tamanho $\le 5.0$ MB[cite: 6, 12, 15] | Arquivo de $0.1$ MB até $5.0$ MB; sem arquivo (`null`)[cite: 6, 14, 15] | Arquivo com tamanho $> 5.0$ MB; formato não suportado[cite: 6, 15] | Inválido retorna HTTP 400 com erro de validação de arquivo[cite: 14, 15] |
| `perfil` | Permissão de acesso via token[cite: 12] | Usuário logado pertencente ao grupo Curador[cite: 12] | Usuário com perfil Convivente, usuário anônimo[cite: 4, 12, 14] | Sem permissão retorna HTTP 403 Forbidden[cite: 14] |

---

### 3.3 Análise do Valor Limite (AVL)

#### 1) `titulo` (Faixa válida: $[5, 120]$ caracteres)[cite: 6]
Valores de fronteira testados: $\{4, 5, 120, 121\}$[cite: 6].

| Caso | Entrada | Resultado Esperado |
| :--- | :--- | :--- |
| Um caractere abaixo do mínimo | `len(titulo) = 4` (`"TEA1"`)[cite: 6] | HTTP 400 Bad Request; "Título deve conter no mínimo 5 caracteres."[cite: 6, 14] |
| Limite inferior válido | `len(titulo) = 5` (`"Rotin"`)[cite: 6] | Validação aceita com sucesso[cite: 6, 14] |
| Limite superior válido | `len(titulo) = 120` (string de 120 caracteres)[cite: 6] | Validação aceita com sucesso[cite: 6, 14] |
| Um caractere acima do máximo | `len(titulo) = 121` (string de 121 caracteres)[cite: 6] | HTTP 400 Bad Request; "Título não pode exceder 120 caracteres."[cite: 6, 14] |

#### 2) `fonte` (Faixa válida: $[3, 100]$ caracteres)[cite: 6]
Valores de fronteira testados: $\{2, 3, 100, 101\}$[cite: 6].

| Caso | Entrada | Resultado Esperado |
| :--- | :--- | :--- |
| Um caractere abaixo do mínimo | `len(fonte) = 2` (`"MS"`)[cite: 6] | HTTP 400 Bad Request; "Fonte deve conter no mínimo 3 caracteres."[cite: 6, 14] |
| Limite inferior válido | `len(fonte) = 3` (`"SBP"`)[cite: 6] | Validação aceita com sucesso[cite: 6, 14] |
| Limite superior válido | `len(fonte) = 100` (string de 100 caracteres)[cite: 6] | Validação aceita com sucesso[cite: 6, 14] |
| Um caractere acima do máximo | `len(fonte) = 101` (string de 101 caracteres)[cite: 6] | HTTP 400 Bad Request; "Fonte não pode exceder 100 caracteres."[cite: 6, 14] |

#### 3) `corpo` (Faixa válida: $[20, 10000]$ caracteres)[cite: 6]
Valores de fronteira testados: $\{19, 20, 10000, 10001\}$[cite: 6].

| Caso | Entrada | Resultado Esperado |
| :--- | :--- | :--- |
| Um caractere abaixo do mínimo | `len(corpo) = 19` (19 caracteres)[cite: 6] | HTTP 400 Bad Request; "O texto do conteúdo deve conter no mínimo 20 caracteres."[cite: 6, 14] |
| Limite inferior válido | `len(corpo) = 20` (20 caracteres)[cite: 6] | Validação aceita com sucesso[cite: 6, 14] |
| Limite superior válido | `len(corpo) = 10000` (10000 caracteres)[cite: 6] | Validação aceita com sucesso[cite: 6, 14] |
| Um caractere acima do máximo | `len(corpo) = 10001` (10001 caracteres)[cite: 6] | HTTP 400 Bad Request; "O texto do conteúdo não pode ultrapassar 10000 caracteres."[cite: 6, 14] |

#### 4) `tags` (Faixa válida de quantidade: $[1, 5]$ tags)[cite: 6]
Valores de fronteira testados: $\{0, 1, 5, 6\}$[cite: 6].

| Caso | Entrada | Resultado Esperado |
| :--- | :--- | :--- |
| Abaixo do limite mínimo | `count(tags) = 0` (array vazio `[]`)[cite: 6] | HTTP 400 Bad Request; "Selecione pelo menos 1 tag."[cite: 6, 12, 14] |
| Limite inferior válido | `count(tags) = 1` (`["TEA"]`)[cite: 6] | Validação aceita com sucesso[cite: 6, 14] |
| Limite superior válido | `count(tags) = 5` (`["TEA", "Rotina", "Inclusao", "Escola", "Familia"]`)[cite: 6] | Validação aceita com sucesso[cite: 6, 14] |
| Acima do limite máximo | `count(tags) = 6` (array com 6 tags)[cite: 6] | HTTP 400 Bad Request; "Número máximo de 5 tags excedido."[cite: 6, 14] |

#### 5) `anexo` (Faixa válida: $\le 5.0$ MB)[cite: 6, 15]
Valores de fronteira testados: $\{0.0 \text{ MB}, 5.0 \text{ MB}, 5.1 \text{ MB}\}$[cite: 6, 15].

| Caso | Entrada | Resultado Esperado |
| :--- | :--- | :--- |
| Sem arquivo enviado | Sem anexo (`None`)[cite: 12, 14] | Validação aceita; conteúdo salvo sem anexo[cite: 12, 14] |
| Limite superior válido | Arquivo PDF de exatamente `5.0 MB`[cite: 6, 15] | Validação aceita; arquivo anexado com sucesso[cite: 6, 12, 15] |
| Acima do limite superior | Arquivo PDF de `5.1 MB`[cite: 6, 15] | HTTP 400 Bad Request; "O tamanho do anexo não pode ser maior que 5 MB."[cite: 6, 14, 15] |

---

### 3.4 Casos de Teste – CDU011

#### 3.4.1 Fluxo Principal: Adicionar Conteúdo Educacional

| ID | Perfil Ator | `titulo` | `fonte` | `corpo` | `tags` | `anexo` | Resultado Esperado | Resultado Obtido | Situação |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **CT09** | Curador[cite: 12] | `len = 5`[cite: 6] | `len = 3`[cite: 6] | `len = 20`[cite: 6] | 1 tag[cite: 6] | Nenhum[cite: 12] | HTTP 201 Created; conteúdo salvo com autoria e data[cite: 12, 14] | - | Não executado[cite: 14] |
| **CT10** | Curador[cite: 12] | `len = 120`[cite: 6] | `len = 100`[cite: 6] | `len = 10000`[cite: 6] | 5 tags[cite: 6] | PDF 5.0 MB[cite: 6, 15] | HTTP 201 Created; conteúdo salvo com metadados e anexo[cite: 12, 14] | - | Não executado[cite: 14] |
| **CT11** | Curador[cite: 12] | `len = 4`[cite: 6] | `len = 10` | `len = 50` | 2 tags | Nenhum | HTTP 400; "Título deve conter no mínimo 5 caracteres."[cite: 6, 14] | - | Não executado[cite: 14] |
| **CT12** | Curador[cite: 12] | `len = 121`[cite: 6] | `len = 10` | `len = 50` | 2 tags | Nenhum | HTTP 400; "Título não pode exceder 120 caracteres."[cite: 6, 14] | - | Não executado[cite: 14] |
| **CT13** | Curador[cite: 12] | `len = 30` | `len = 2`[cite: 6] | `len = 50` | 2 tags | Nenhum | HTTP 400; "Fonte deve conter no mínimo 3 caracteres."[cite: 6, 14] | - | Não executado[cite: 14] |
| **CT14** | Curador[cite: 12] | `len = 30` | `len = 101`[cite: 6] | `len = 50` | 2 tags | Nenhum | HTTP 400; "Fonte não pode exceder 100 caracteres."[cite: 6, 14] | - | Não executado[cite: 14] |
| **CT15** | Curador[cite: 12] | `len = 30` | `len = 10` | `len = 19`[cite: 6] | 2 tags | Nenhum | HTTP 400; "O texto do conteúdo deve conter no mínimo 20 caracteres."[cite: 6, 14] | - | Não executado[cite: 14] |
| **CT16** | Curador[cite: 12] | `len = 30` | `len = 10` | `len = 10001`[cite: 6] | 2 tags | Nenhum | HTTP 400; "O texto do conteúdo não pode ultrapassar 10000 caracteres."[cite: 6, 14] | - | Não executado[cite: 14] |
| **CT17** | Curador[cite: 12] | `len = 30` | `len = 10` | `len = 50` | 0 tags[cite: 6] | Nenhum | HTTP 400; "Selecione pelo menos 1 tag."[cite: 6, 12, 14] | - | Não executado[cite: 14] |
| **CT18** | Curador[cite: 12] | `len = 30` | `len = 10` | `len = 50` | 6 tags[cite: 6] | Nenhum | HTTP 400; "Número máximo de 5 tags excedido."[cite: 6, 14] | - | Não executado[cite: 14] |
| **CT19** | Curador[cite: 12] | `len = 30` | `len = 10` | `len = 50` | 2 tags | PDF 5.1 MB[cite: 6, 15] | HTTP 400; "O tamanho do anexo não pode ser maior que 5 MB."[cite: 6, 14, 15] | - | Não executado[cite: 14] |
| **CT20** | Convivente[cite: 4] | `len = 30` | `len = 10` | `len = 50` | 2 tags | Nenhum | HTTP 403 Forbidden; "Usuário não possui perfil de curador."[cite: 4, 12, 14] | - | Não executado[cite: 14] |

---

#### 3.4.2 Fluxo Alternativo I: Editar Conteúdo Existente

| ID | Perfil Ator | `conteudo_id` | Campo Alterado | Valor Inserido | Resultado Esperado | Resultado Obtido | Situação |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **CT21** | Curador[cite: 12] | Existente ($id = 1$)[cite: 6] | `titulo` | String com 5 caracteres (Limite inferior)[cite: 6] | HTTP 200; "Conteúdo atualizado com sucesso."[cite: 12] | - | Não executado[cite: 14] |
| **CT22** | Curador[cite: 12] | Existente ($id = 1$)[cite: 6] | `titulo` | String com 121 caracteres (Limite acima)[cite: 6] | HTTP 400; dados não alterados; erro de validação[cite: 6, 12, 14] | - | Não executado[cite: 14] |
| **CT23** | Curador[cite: 12] | Existente ($id = 1$)[cite: 6] | `tags` | Array vazio `[]` (0 tags)[cite: 6] | HTTP 400; "Selecione pelo menos 1 tag."[cite: 6, 12, 14] | - | Não executado[cite: 14] |
| **CT24** | Curador[cite: 12] | Inexistente ($id = 9999$)[cite: 6, 14] | Qualquer | Qualquer alteração | HTTP 404 Not Found; artigo não localizado[cite: 12, 14] | - | Não executado[cite: 14] |

---

#### 3.4.3 Fluxo Alternativo II: Remover Conteúdo

| ID | Perfil Ator | `conteudo_id` | Confirmação | Resultado Esperado | Resultado Obtido | Situação |
| :---: | :--- | :--- | :---: | :--- | :---: | :---: |
| **CT25** | Curador[cite: 12] | Existente ($id = 1$)[cite: 6] | Confirmado (`Sim`)[cite: 12] | HTTP 200 / 204 No Content; registro excluído; mensagem de sucesso[cite: 12] | - | Não executado[cite: 14] |
| **CT26** | Curador[cite: 12] | Existente ($id = 1$)[cite: 6] | Rejeitado (`Cancelar`)[cite: 12] | Exclusão abortada; conteúdo mantido na base[cite: 12] | - | Não executado[cite: 14] |
| **CT27** | Curador[cite: 12] | Inexistente ($id = 9999$)[cite: 6, 14] | Confirmado (`Sim`)[cite: 12] | HTTP 404 Not Found; registro não encontrado[cite: 12, 14, 15] | - | Não executado[cite: 14] |
| **CT28** | Convivente[cite: 4] | Existente ($id = 1$)[cite: 6] | Confirmado (`Sim`)[cite: 12] | HTTP 403 Forbidden; apenas curadores podem excluir conteúdos[cite: 4, 12, 14] | - | Não executado[cite: 14] |

---

## 4. Testes Não Funcionais

### 4.1 RNF01 – Segurança e Controle de Acesso (LGPD e Perfis)
* **Categoria:** Segurança[cite: 4, 13]
* **Automatizado:** Sim (via testes de integração Django REST Framework / `APITestCase`)[cite: 3, 13]
* **Duração Estimada:** 5 minutos[cite: 13]
* **Executado:** Não[cite: 13]
* **Responsável:** João Pedro Dantas Magalhães[cite: 1, 13]
* **Data:** 13/09/2026[cite: 13]
* **Procedimentos:** Enviar requisições `POST`, `PUT` e `DELETE` para o endpoint `/api/conteudos/` utilizando tokens JWT pertencentes a usuários com perfil de convivente padrão e tokens de usuários anônimos[cite: 3, 4, 12, 13].
* **Critérios de Aceitação:** O sistema deve barrar 100% das tentativas de escrita com respostas HTTP 401 Unauthorized ou HTTP 403 Forbidden, garantindo que somente curadores alterem o repositório educacional (RN01)[cite: 4, 12, 13].
* **Resultado:** Não executado[cite: 13, 14].

### 4.2 RNF02 – Desempenho na Recuperação de Conteúdo
* **Categoria:** Desempenho[cite: 4, 13]
* **Automatizado:** Sim[cite: 13]
* **Duração Estimada:** 10 minutos[cite: 13]
* **Executado:** Não[cite: 13]
* **Responsável:** Ramon Couto Santos[cite: 1, 13]
* **Data:** 13/09/2026[cite: 13]
* **Procedimentos:** Executar requisições concorrentes de leitura (`GET /api/conteudos/`) simulando 50 acessos simultâneos de conviventes em ambiente Render[cite: 1, 11, 13].
* **Critérios de Aceitação:** O tempo médio de resposta para a carga completa do payload do artigo deve ser inferior a 1,5 segundo em 95% das requisições[cite: 4, 13].
* **Resultado:** Não executado[cite: 13, 14].

---

## 5. Referências

1. FREIRE, Marília A. **Teste de Software: Técnicas e Critérios de Testes – Particionamento em Classes de Equivalência e Análise do Valor Limite**. Natal: IFRN, 2025[cite: 5, 6].
2. TEVEJO. **Documento de Visão e Glossário de Negócio do Projeto TeVejo**. Natal: IFRN, 2026[cite: 2, 4].
3. TEVEJO. **Detalhamentos dos Casos de Uso CDU003 e CDU011**. Natal: IFRN, 2026[cite: 11, 12].
4. IFRN. **Documentos de Casos de Teste dos Projetos Conta Comigo e Bizzu**. Natal: IFRN, 2025/2026[cite: 14, 15].
5. IFRN. **Modelo Padrão de Caso de Teste (caso_de_teste.dot)**. Natal: IFRN[cite: 13].
