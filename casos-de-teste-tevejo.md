# Plano Unificado de Testes Funcionais – TeVejo

## Histórico de Alterações

| Data | Versão | Descrição | Autores |
| :---: | :---: | :--- | :--- |
| 13/09/2026 | 1.0 | Elaboração dos testes com AVL para CDU003 e CDU011 | João Pedro Dantas Magalhães |
| 15/09/2026 | 1.1 | Inclusão dos testes funcionais dos CDU001 e CDU002 | Ramon Couto Santos |
| 15/09/2026 | 1.2 | Inclusão dos testes funcionais dos CDU006 e CDU007 | Fernando Yuri Vital De Aquino |
| 15/09/2026 | 1.3 | Inclusão dos testes funcionais dos CDU024 e CDU025 | Aaron Guerra Goldberg |
| 15/09/2026 | 1.4 | Inclusão dos testes com limites dos CDU008 e CDU023 | Lorrany Fagundes Campos da Silva |
| 15/09/2026 | 2.0 | Consolidação e padronização final do documento de testes do projeto | Equipe TeVejo |

---

## 1. Introdução

Este documento reúne a especificação unificada dos casos de teste funcionais da plataforma web **TeVejo**, desenvolvida na disciplina de Prática de Desenvolvimento de Software (PDS) do IFRN. Ele contém o planejamento de testes de caixa-preta estruturado a partir das técnicas de **Particionamento em Classes de Equivalência (PCE)** e **Análise do Valor Limite (AVL)**, servindo como referência para validação das regras de negócio, integridade de dados e conformidade das rotas web e da API REST.

### 1.1 Visão Geral do Documento

O documento está organizado nos seguintes tópicos:
* **Seção 2 – Dados e Preparação do Ambiente de Teste:** Pré-condições globais, dados de carga inicial e padronização dos estados de execução.
* **Seção 3 – Testes Funcionais por Caso de Uso:**
  * 3.1 CDU001 – Fazer Login (Ramon Couto)
  * 3.2 CDU002 – Autocadastro (Ramon Couto)
  * 3.3 CDU003 – Visualizar Conteúdo Educacional (João Pedro Dantas)
  * 3.4 CDU006 – Participar de Comunidade (Fernando Yuri)
  * 3.5 CDU007 – Postar nas Comunidades (Fernando Yuri)
  * 3.6 CDU008 – Criar Comunidade (Lorrany Fagundes)
  * 3.7 CDU011 – Gerenciar Conteúdo Educacional (João Pedro Dantas)
  * 3.8 CDU023 – Interação em Postagens (Lorrany Fagundes)
  * 3.9 CDU024 – Moderar Conviventes (Aaron Goldberg)
  * 3.10 CDU025 – Analisar Denúncias (Aaron Goldberg)
* **Seção 4 – Testes Não Funcionais:** Segurança de permissões (LGPD/perfis) e requisitos de desempenho.
* **Seção 5 – Referências:** Materiais e referências bibliográficas do projeto.

---

## 2. Dados e Preparação do Ambiente de Teste

Para a execução dos casos de teste, o ambiente deve atender às seguintes condições iniciais:
* O banco de dados PostgreSQL deve estar ativo, migrado e com as cargas de teste necessárias.
* Os testes web devem ser executados nas páginas mapeadas da aplicação (`/usuarios/login/`, `/usuarios/cadastro/`, etc.) e as validações de API devem usar os endpoints sob `/api/` com headers adequados.
* Contas de teste preparadas:
  * Um usuário ativo com perfil `Convivente` padrão.
  * Um usuário ativo com perfil `Curador` habilitado.
  * Um usuário ativo com perfil `Moderador` associado a pelo menos uma comunidade.
  * Uma conta de usuário marcada com `is_active=False` para validação de bloqueio.
* Base de dados populada com:
  * Comunidades de teste: ID 1 (`Autismo Adulto`), ID 2 (`Pais e Mães Atípicos`) e ID 3 (`Rotina e Terapias`).
  * Convivente de teste associado como membro nas comunidades 1 e 3, moderador na comunidade 2 e com registro prévio de banimento na comunidade 2 em cenário específico.
* As situações dos testes são padronizadas em: `Passou`, `Não passou` ou `Não executado`.

---

## 3. Testes Funcionais por Caso de Uso

### 3.1 CDU001 – Fazer Login

* **Responsável:** Ramon Couto Santos
* **Ator Principal:** Convivente, Curador, Moderador ou Administrador
* **Pré-condição:** Usuário cadastrado; para sucesso, conta ativa.
* **Pós-condição:** Usuário autenticado, sessão iniciada/tokens gerados e redirecionamento para o dashboard inicial ou destino solicitado.

#### 3.1.1 Classes de Equivalência

| Campo ou Condição | Classes Válidas | Classes Inválidas | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| Identificador | Username existente ou e-mail existente (case-insensitive) | Username/e-mail inexistente ou identificador vazio | Credenciais válidas autenticam; demais casos retornam erro genérico |
| Senha | Senha correta cadastrada da conta | Senha incorreta, vazia ou ausente | Apenas senha coincidente permite autenticação |
| Status da Conta | `is_active=True` | `is_active=False` | Conta inativa tem login recusado |
| Username | String textual sem espaços | String textual com um ou mais espaços | Rejeição pelo formulário |
| Parâmetro `next` | URL interna de destino válida | Ausente ou vazia | Ausente direciona para início; preenchida redireciona à rota |
| CSRF | Token CSRF válido na sessão/header | Token ausente, adulterado ou expirado | Rejeição da requisição com erro de sessão |

#### 3.1.2 Análise do Valor Limite (AVL)

| ID | Campo | Entrada | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| LOGIN-LIM-01 | Username | 1 caractere válido | Validação de tamanho aceita; autenticação prossegue |
| LOGIN-LIM-02 | Username | 150 caracteres válidos | Validação de tamanho aceita; autenticação prossegue |
| LOGIN-LIM-03 | Username | 151 caracteres | HTTP 200/400 com erro de tamanho máximo; autenticação bloqueada |
| LOGIN-LIM-04 | Username | Um caractere de espaço entre duas palavras | Erro: "O nome de usuário não pode conter espaços." |
| LOGIN-LIM-05 | Username | Espaços em branco no início e no fim | Espaços removidos (strip); login realizado se dados forem corretos |
| LOGIN-LIM-06 | Senha | Senha contendo espaços no início ou no fim | Valor mantido sem strip; autentica apenas se coincidir com o hash |

#### 3.1.3 Tabela de Casos de Teste – CDU001

| ID | Cenário | Dados de Entrada | Resultado Esperado | Resultado Obtido | Situação |
| :--- | :--- | :--- | :--- | :---: | :---: |
| LOGIN-01 | Credenciais válidas por username | Username e senha cadastrados corretos | HTTP 302 para início; usuário logado | - | Não executado |
| LOGIN-02 | Credenciais válidas por e-mail | E-mail e senha cadastrados corretos | HTTP 302 para início; usuário logado | - | Não executado |
| LOGIN-03 | Redirecionamento com `next` | Credenciais corretas e `next=/conteudos/` | HTTP 302 para o destino `/conteudos/` | - | Não executado |
| LOGIN-04 | Username não cadastrado | Username inexistente e qualquer senha | Formulário reapresentado: "Usuário ou senha inválidos." | - | Não executado |
| LOGIN-05 | E-mail não cadastrado | E-mail inexistente e qualquer senha | Formulário reapresentado: "Usuário ou senha inválidos." | - | Não executado |
| LOGIN-06 | Senha incorreta | Usuário válido e senha incorreta | Formulário reapresentado: "Usuário ou senha inválidos." | - | Não executado |
| LOGIN-07 | Conta desativada | Usuário inativo com senha correta | Login recusado: "Usuário ou senha inválidos." | - | Não executado |
| LOGIN-08 | Username com espaço interno | `"usuario teste"` com senha válida | Erro: "O nome de usuário não pode conter espaços." | - | Não executado |
| LOGIN-09 | Campos obrigatórios vazios | Username vazio e/ou senha vazia | Erro indicando campo obrigatório | - | Não executado |
| LOGIN-10 | Acesso de usuário já logado | Sessão autenticada ativa | Redirecionamento automático para home | - | Não executado |
| LOGIN-11 | POST sem token CSRF | Requisição sem CSRF | Erro 403 Forbidden / Sessão expirada | - | Não executado |
| API-LOGIN-01 | Login REST válido | JSON com identificador e senha válidos | HTTP 200 com tokens JWT (access/refresh) | - | Não executado |
| API-LOGIN-02 | Login REST sem identificador | JSON com username/e-mail ausente | HTTP 400: "Informe e-mail ou username." | - | Não executado |
| API-LOGIN-03 | Login REST com dados inválidos | Identificador inexistente ou senha errada | HTTP 400: "Usuário ou senha inválidos." | - | Não executado |

---

### 3.2 CDU002 – Autocadastro

* **Responsável:** Ramon Couto Santos
* **Ator Principal:** Convivente
* **Pré-condição:** Visitante não autenticado na plataforma.
* **Pós-condição:** Registro persistido, vinculado ao grupo `Convivente` e redirecionado para a tela de login.

#### 3.2.1 Classes de Equivalência

| Campo ou Condição | Classes Válidas | Classes Inválidas | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| Username | Texto único, sem espaços, $1 \le len \le 150$ | Vazio, duplicado, com espaços ou $len > 150$ | Válido prossegue; inválido exibe erro de validação |
| Nome | Texto com $3 \le len \le 100$ | Vazio, ausente, $len < 3$ ou $len > 100$ | Válido aceito; inválido bloqueia submissão |
| E-mail | Formato de e-mail válido e inédito na base | Vazio, formato inválido ou e-mail já existente | Válido aceito; inválido exibe erro |
| Senha | Mínimo de 6 caracteres aprovado pelos validadores | $len < 6$, senha fraca ou não informada | Rejeição da criação da conta |
| Confirmação | Valor idêntico ao campo de senha | Divergente da senha informada | Erro: "As senhas não coincidem." |
| Foto | Arquivo opcional em formato de imagem válido | Arquivo executável ou não imagem | Validação do arquivo rejeita submissão |

#### 3.2.2 Análise do Valor Limite (AVL)

| ID | Campo | Entrada | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| CAD-LIM-01 | Nome | 2 caracteres | Erro: "O nome deve ter pelo menos 3 caracteres." |
| CAD-LIM-02 | Nome | 3 caracteres | Limite inferior aceito com sucesso |
| CAD-LIM-03 | Nome | 100 caracteres | Limite superior aceito com sucesso |
| CAD-LIM-04 | Nome | 101 caracteres | Erro de tamanho máximo violado |
| CAD-LIM-05 | Username | 150 caracteres | Limite superior aceito com sucesso |
| CAD-LIM-06 | Username | 151 caracteres | Erro de tamanho máximo violado |
| CAD-LIM-07 | Senha | 5 caracteres | Erro de tamanho mínimo da senha |
| CAD-LIM-08 | Senha | 6 caracteres válidos | Limite inferior de senha aceito |
| CAD-LIM-09 | Confirmação | Idêntica à senha | Sucesso na criação |
| CAD-LIM-10 | Confirmação | 1 caractere divergente da senha | Erro: "As senhas não coincidem." |

#### 3.2.3 Tabela de Casos de Teste – CDU002

| ID | Cenário | Dados de Entrada | Resultado Esperado | Resultado Obtido | Situação |
| :--- | :--- | :--- | :--- | :---: | :---: |
| CAD-01 | Cadastro com campos obrigatórios | Username, nome, e-mail e senha válidos | HTTP 302 para login; usuário salvo como Convivente | - | Não executado |
| CAD-02 | Cadastro completo com foto | Campos obrigatórios + imagem PNG válida | Conta criada com avatar e redirecionamento | - | Não executado |
| CAD-03 | Username duplicado | Username já existente na base | Erro: "Nome de usuário já cadastrado." | - | Não executado |
| CAD-04 | E-mail duplicado | E-mail já utilizado por outro usuário | Erro: "E-mail já cadastrado." | - | Não executado |
| CAD-05 | Username com espaço | `"novo usuario"` e dados válidos | Erro: "O nome de usuário não pode conter espaços." | - | Não executado |
| CAD-06 | Nome com 2 caracteres | `nome = "Ab"` | Erro: "O nome deve ter pelo menos 3 caracteres." | - | Não executado |
| CAD-07 | Confirmação divergente | Senha e confirmação diferentes | Erro: "As senhas não coincidem." | - | Não executado |
| CAD-08 | Senha com 5 caracteres | `password = "12345"` | Erro de senha menor que o limite mínimo | - | Não executado |
| CAD-09 | Campo obrigatório ausente | Payload sem o campo `email` | Erro indicando campo obrigatório ausente | - | Não executado |
| CAD-10 | Formato de e-mail inválido | `email = "emailsemarroba"` | Erro de formato de e-mail | - | Não executado |
| CAD-11 | Usuário autenticado acessa cadastro | Sessão ativa existente | Redirecionamento automático para a área logada | - | Não executado |
| CAD-12 | Cadastro sem CSRF | POST web sem token | HTTP 403 Forbidden | - | Não executado |
| API-CAD-01 | Cadastro REST com sucesso | JSON com dados válidos | HTTP 201 com tokens JWT e sem expor a senha | - | Não executado |
| API-CAD-02 | Cadastro REST duplicado | JSON com e-mail já existente | HTTP 400 com mensagem de duplicidade | - | Não executado |

---

### 3.3 CDU003 – Visualizar Conteúdo Educacional

* **Responsável:** João Pedro Dantas Magalhães
* **Ator Principal:** Convivente
* **Atores Secundários:** Curador
* **Pré-condição:** Usuário autenticado com sessão ativa no sistema.
* **Pós-condição:** Conteúdo educacional renderizado de forma íntegra.

#### 3.3.1 Classes de Equivalência

| Variável / Campo | Condições | Classes Válidas | Classes Inválidas | Resultado Esperado |
| :--- | :--- | :--- | :--- | :--- |
| `conteudo_id` | Identificador primário inteiro ($id \ge 1$) | ID existente no banco de dados | ID igual a zero ($0$), negativo ($< 0$), não numérico | Válido retorna HTTP 200; inválido retorna HTTP 400/404 |
| `quantidade_conteudos` | Quantidade de registros cadastrados ($N \ge 0$) | $N \ge 1$ artigos cadastrados | $N = 0$ artigos cadastrados | Válido lista os itens; inválido exibe mensagem de lista vazia |
| `autenticacao` | Sessão ativa na plataforma | Usuário com sessão/token válido | Usuário não logado (anônimo) ou token vencido | Válido exibe tela; inválido retorna 401 e força login |
| `filtro_tag` / `busca` | Tamanho da string ($1 \le len \le 30$) | String entre 1 e 30 caracteres | String vazia ($0$) ou acima de 30 caracteres | Válido filtra a listagem; acima de 30 retorna HTTP 400 |

#### 3.3.2 Análise do Valor Limite (AVL)

| Campo | Limite / Fronteira | Entrada | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| `quantidade_conteudos` | Limite inferior inválido | $N = 0$ | HTTP 200; lista vazia; exibe: "Nenhum conteúdo educacional disponível no momento." |
| `quantidade_conteudos` | Limite inferior válido | $N = 1$ | HTTP 200; exibe exatamente 1 card com dados do artigo e curador |
| `quantidade_conteudos` | Valor nominal | $N = 5$ | HTTP 200; listagem renderiza os 5 cards com scroll/paginação |
| `conteudo_id` | Abaixo do limite mínimo | `conteudo_id = 0` | HTTP 400 / 404; identificador de recurso inválido |
| `conteudo_id` | Limite inferior válido | `conteudo_id = 1` | HTTP 200; abre tela de leitura com texto e fonte |
| `conteudo_id` | Acima da base (inexistente) | `conteudo_id = 999999` | HTTP 404: "Não foi possível carregar o conteúdo. Tente novamente mais tarde." |
| `filtro_tag` | Limite inferior (vazio) | $len(termo) = 0$ | HTTP 200; busca ignorada, listando todos os artigos |
| `filtro_tag` | Limite inferior válido | $len(termo) = 1$ (`"A"`) | HTTP 200; retorna apenas conteúdos vinculados ao caractere |
| `filtro_tag` | Limite superior válido | $len(termo) = 30$ | HTTP 200; aplica filtro com string de 30 caracteres |
| `filtro_tag` | Acima do limite superior | $len(termo) = 31$ | HTTP 400: "Termo de busca excede o limite de 30 caracteres." |

#### 3.3.3 Tabela de Casos de Teste – CDU003

| ID | Cenário / Autenticação | `conteudo_id` | `quantidade_conteudos` | `filtro_tag` | Resultado Esperado | Resultado Obtido | Situação |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| CT-003-01 | Convivente autenticado | N/A (Listagem) | $N = 0$ (Vazio) | N/A | HTTP 200: "Nenhum conteúdo educacional disponível no momento." | - | Não executado |
| CT-003-02 | Convivente autenticado | N/A (Listagem) | $N = 1$ (Limite mín.) | N/A | HTTP 200; listagem com exatamente 1 artigo curado | - | Não executado |
| CT-003-03 | Convivente autenticado | $id = 1$ (Existente) | $N \ge 1$ | N/A | HTTP 200; carrega artigo completo com autoria e tags | - | Não executado |
| CT-003-04 | Convivente autenticado | $id = 0$ (Inválido) | $N \ge 1$ | N/A | HTTP 400/404: "Não foi possível carregar o conteúdo." | - | Não executado |
| CT-003-05 | Convivente autenticado | $id = 999999$ (Inexistente) | $N \ge 1$ | N/A | HTTP 404: "Não foi possível carregar o conteúdo." | - | Não executado |
| CT-003-06 | Convivente autenticado | N/A | $N \ge 1$ | $len = 1$ (`"A"`) | HTTP 200; lista filtrada por artigos com a tag correspondente | - | Não executado |
| CT-003-07 | Convivente autenticado | N/A | $N \ge 1$ | $len = 31$ (Inválido) | HTTP 400: "Termo de busca excede o limite de 30 caracteres." | - | Não executado |
| CT-003-08 | Usuário anônimo | $id = 1$ | $N \ge 1$ | N/A | HTTP 401 / Redirecionamento obrigatório para login | - | Não executado |

---

### 3.4 CDU006 – Participar de Comunidade

* **Responsável:** Fernando Yuri Vital De Aquino
* **Ator Principal:** Convivente
* **Pré-condição:** Usuário autenticado na plataforma.
* **Pós-condição:** Convivente adicionado aos membros e contador de participantes atualizado.

#### 3.4.1 Classes de Equivalência

| Variável ou Condição | Classes Válidas | Classes Inválidas | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| Perfil do Usuário | Convivente autenticado | Usuário com perfil Curador, usuário anônimo | Convivente ingressa; curador/anônimo é bloqueado |
| Comunidade | ID correspondente a comunidade ativa | ID inexistente ($id=0$, $id=4$ em base de 3) | ID válido processa adesão; inválido retorna 404 |
| Vínculo Prévio | Não participante da comunidade | Já membro, criador/moderador ou usuário banido | Não participante ingressa; membro/banido recebe erro |

#### 3.4.2 Análise do Valor Limite (AVL)

A análise de valor limite incide sobre a faixa de IDs das comunidades cadastradas na preparação do ambiente (faixa válida: $[1, 3]$):
* `0`: imediatamente abaixo do menor ID válido.
* `1`: menor ID válido cadastrado.
* `3`: maior ID válido cadastrado.
* `4`: imediatamente acima do maior ID cadastrado.

#### 3.4.3 Tabela de Casos de Teste – CDU006

| ID | Usuário | Comunidade | Vínculo Atual | Resultado Esperado | Resultado Obtido | Situação |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| PART-01 | Convivente autenticado | 1 - Autismo Adulto | Não é membro | Convivente vira membro, contador incrementa e botão exibe "Membro" | - | Não executado |
| PART-02 | Convivente autenticado | 3 - Rotina e Terapias | Não é membro | Convivente vira membro, contador incrementa e botão exibe "Membro" | - | Não executado |
| PART-03 | Convivente autenticado | 1 - Autismo Adulto | Já é membro | Erro: "Você já é membro desta comunidade." e vínculo não duplica | - | Não executado |
| PART-04 | Convivente autenticado | 2 - Pais e Mães Atípicos | É moderador | Erro: "O moderador já é membro da comunidade." | - | Não executado |
| PART-05 | Convivente autenticado | 2 - Pais e Mães Atípicos | Banido | Erro: "Você foi banido desta comunidade." e adesão é impedida | - | Não executado |
| PART-06 | Convivente autenticado | 0 (Abaixo do mín.) | - | Erro: "Comunidade não encontrada." (HTTP 404) | - | Não executado |
| PART-07 | Convivente autenticado | 4 (Acima do máx.) | - | Erro: "Comunidade não encontrada." (HTTP 404) | - | Não executado |
| PART-08 | Curador autenticado | 1 - Autismo Adulto | Não é membro | Erro: "Apenas Conviventes podem realizar esta ação." (HTTP 403) | - | Não executado |
| PART-09 | Visitante anônimo | 1 - Autismo Adulto | - | Redirecionamento para login e encerramento do caso de uso | - | Não executado |

---

### 3.5 CDU007 – Postar nas Comunidades

* **Responsável:** Fernando Yuri Vital De Aquino
* **Ator Principal:** Convivente
* **Pré-condição:** Usuário autenticado e associado como membro da comunidade.
* **Pós-condição:** Publicação registrada e visível no feed da respectiva comunidade.

#### 3.5.1 Classes de Equivalência

| Campo ou Condição | Classes Válidas | Classes Inválidas | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| `titulo` | Texto preenchido com $1 \le len \le 50$ | Vazio, composto apenas por espaços ou $len > 50$ | Válido salva o post; inválido rejeita criação |
| `conteudo` | Texto preenchido ($len \ge 1$) | Vazio ou composto apenas por espaços em branco | Válido salva o post; vazio exige preenchimento |
| Vínculo do Usuário | Membro da comunidade sem punição | Não participante da comunidade ou com restrição ativa | Apenas membro sem restrição tem permissão de postar |

#### 3.5.2 Análise do Valor Limite (AVL)

* **Título (faixa válida $[1, 50]$):**
  * `0` ou `3 espaços`: abaixo do mínimo válido (inválido).
  * `1`: limite inferior válido.
  * `49`: imediatamente abaixo do limite superior.
  * `50`: limite superior válido.
  * `51`: imediatamente acima do limite superior (inválido).
* **Conteúdo (campo `TEXT` com regra de não vazio):**
  * `0` ou `3 espaços`: abaixo do mínimo (inválido).
  * `1`: limite inferior válido.

#### 3.5.3 Tabela de Casos de Teste – CDU007

| ID | Usuário | Comunidade / Vínculo | `titulo` | `conteudo` | Resultado Esperado | Resultado Obtido | Situação |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| POST-01 | Convivente | Com. 1 / Membro | `"Minha rotina"` (12 carac.) | `"A rotina fixa me ajudou"` (25 carac.) | Post publicado com sucesso no feed | - | Não executado |
| POST-02 | Convivente | Com. 1 / Membro | `"A"` (1 carac. - Limite mín.) | `"A"` (1 carac. - Limite mín.) | Post publicado com sucesso no feed | - | Não executado |
| POST-03 | Convivente | Com. 1 / Membro | String com 49 caracteres | `"Compartilhando experiência"` | Post publicado com sucesso no feed | - | Não executado |
| POST-04 | Convivente | Com. 1 / Membro | String com 50 caracteres | `"Compartilhando experiência"` | Post publicado com sucesso no feed | - | Não executado |
| POST-05 | Convivente | Com. 1 / Membro | String com 51 caracteres | `"Compartilhando experiência"` | Erro: título excede 50 caracteres; post não criado | - | Não executado |
| POST-06 | Convivente | Com. 1 / Membro | `""` (0 carac. - Vazio) | `"Olá, pessoal!"` | Erro: "O título da postagem é obrigatório." | - | Não executado |
| POST-07 | Convivente | Com. 1 / Membro | `"   "` (3 espaços em branco) | `"Olá, pessoal!"` | Erro: "O título da postagem é obrigatório." | - | Não executado |
| POST-08 | Convivente | Com. 3 / Membro restrito | `"Dúvida sobre terapia"` | `"Alguém já passou por isso?"` | Erro: "Você está restrito de postar nesta comunidade até dd/mm/aaaa." | - | Não executado |
| POST-09 | Convivente | Com. 4 / Inexistente | `"Primeira postagem"` | `"Indicação de clínica"` | Erro: "Comunidade não encontrada." | - | Não executado |
| POST-10 | Convivente | Com. 3 / Membro | `"Dúvida sobre terapia"` | `""` (0 carac. - Vazio) | Erro: "O conteúdo da postagem não pode estar vazio" | - | Não executado |
| POST-11 | Convivente | Com. 3 / Membro | `"Dúvida sobre terapia"` | `"   "` (3 espaços em branco) | Erro: "O conteúdo da postagem não pode estar vazio" | - | Não executado |
| POST-12 | Convivente | Com. 2 / Não membro | `"Primeira postagem"` | `"Alguém de Natal?"` | Erro: "Você precisa participar da comunidade para publicar conteúdos" | - | Não executado |
| POST-13 | Anônimo | Com. 1 | `"Primeira postagem"` | `"Alguém de Natal?"` | Redirecionamento obrigatório para login | - | Não executado |

---

### 3.6 CDU008 – Criar Comunidade

* **Responsável:** Lorrany Fagundes Campos da Silva
* **Ator Principal:** Convivente
* **Pré-condição:** Usuário autenticado na plataforma.
* **Pós-condição:** Comunidade registrada no sistema e usuário definido como seu moderador.

#### 3.6.1 Classes de Equivalência e Fronteiras

| Campo | Condição | Classe Válida | Classe Inválida | Resultado Esperado |
| :--- | :--- | :--- | :--- | :--- |
| `nome` | Tamanho permitido ($3 \le len \le 50$) | $3 \le len \le 50$ caracteres | $len < 3$ ou $len > 50$ caracteres | Válido cria comunidade; inválido retorna mensagem de erro |
| `autenticacao` | Sessão ativa | Usuário logado | Usuário não autenticado | Logado permite criação; anônimo é direcionado ao login |

#### 3.6.2 Análise do Valor Limite (AVL)

* **Limite inferior:** 2 caracteres (inválido) e 3 caracteres (mínimo válido).
* **Limite superior:** 50 caracteres (máximo válido) e 51 caracteres (acima do máximo - inválido).

#### 3.6.3 Tabela de Casos de Teste – CDU008

| ID | Cenário | Dados de Entrada | Resultado Esperado | Resultado Obtido | Situação |
| :---: | :--- | :--- | :--- | :---: | :---: |
| CDT-008-01 | Limite inferior válido do Nome | Nome com 3 caracteres (`"ABC"`) | Comunidade criada com sucesso e usuário associado como moderador | - | Não executado |
| CDT-008-02 | Limite inferior inválido do Nome | Nome com 2 caracteres (`"AB"`) | Criação bloqueada: "O nome deve ter no mínimo 3 caracteres." | - | Não executado |
| CDT-008-03 | Limite superior válido do Nome | Nome com 50 caracteres inédito | Comunidade criada com sucesso e redirecionamento para o grupo | - | Não executado |
| CDT-008-04 | Limite superior inválido do Nome | Nome com 51 caracteres | Criação bloqueada: limite de 50 caracteres excedido | - | Não executado |

---

### 3.7 CDU011 – Gerenciar Conteúdo Educacional

* **Responsável:** João Pedro Dantas Magalhães
* **Ator Principal:** Curador
* **Pré-condição:** Usuário autenticado com papel de curador.
* **Pós-condição:** Artigo educacional inserido, editado ou removido com histórico de autoria.

#### 3.7.1 Classes de Equivalência

| Campo | Condição de Entrada | Classes Válidas | Classes Inválidas | Resultado Esperado |
| :--- | :--- | :--- | :--- | :--- |
| `titulo` | Obrigatório; $5 \le len \le 120$ | $5 \le len \le 120$ caracteres | Vazio, ausente, $len < 5$ ou $len > 120$ | Erro HTTP 400 no campo `titulo` |
| `fonte` | Obrigatório; $3 \le len \le 100$ | $3 \le len \le 100$ caracteres | Vazio, ausente, $len < 3$ ou $len > 100$ | Erro HTTP 400 no campo `fonte` |
| `corpo` | Obrigatório; $20 \le len \le 10000$ | $20 \le len \le 10000$ caracteres | Vazio, ausente, $len < 20$ ou $len > 10000$ | Erro HTTP 400 no campo `corpo` |
| `tags` | Array de tags; $1 \le count \le 5$ | Array com 1 a 5 tags | Array vazio ($0$) ou com mais de 5 tags ($>5$) | Erro HTTP 400 de seleção de tags |
| `anexo` | Formato PDF/JPG/PNG; tamanho $\le 5.0$ MB | Arquivo entre 0.1 e 5.0 MB; ausente (`null`) | Arquivo com mais de 5.0 MB; formato não suportado | Erro HTTP 400 no upload do arquivo |
| `perfil` | Nível de autorização | Usuário do grupo Curador | Convivente ou anônimo | Sem permissão retorna HTTP 403 Forbidden |

#### 3.7.2 Análise do Valor Limite (AVL)

* **`titulo` ($[5, 120]$):** Fronteiras testadas em $\{4, 5, 120, 121\}$.
* **`fonte` ($[3, 100]$):** Fronteiras testadas em $\{2, 3, 100, 101\}$.
* **`corpo` ($[20, 10000]$):** Fronteiras testadas em $\{19, 20, 10000, 10001\}$.
* **`tags` ($[1, 5]$):** Fronteiras testadas em $\{0, 1, 5, 6\}$.
* **`anexo` ($\le 5.0\text{ MB}$):** Fronteiras testadas em $\{0.0\text{ MB (ausente)}, 5.0\text{ MB}, 5.1\text{ MB}\}$.

#### 3.7.3 Tabela de Casos de Teste – CDU011

| ID | Perfil | Operação | `titulo` | `fonte` | `corpo` | `tags` | `anexo` | Resultado Esperado | Resultado Obtido | Situação |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| CT-011-01 | Curador | Publicar | $len = 5$ | $len = 3$ | $len = 20$ | 1 tag | Nenhum | HTTP 201; conteúdo cadastrado com autoria | - | Não executado |
| CT-011-02 | Curador | Publicar | $len = 120$ | $len = 100$ | $len = 10000$ | 5 tags | PDF 5.0 MB | HTTP 201; artigo salvo com anexo | - | Não executado |
| CT-011-03 | Curador | Publicar | $len = 4$ | $len = 10$ | $len = 50$ | 2 tags | Nenhum | HTTP 400: "Título deve conter no mínimo 5 caracteres." | - | Não executado |
| CT-011-04 | Curador | Publicar | $len = 121$ | $len = 10$ | $len = 50$ | 2 tags | Nenhum | HTTP 400: "Título não pode exceder 120 caracteres." | - | Não executado |
| CT-011-05 | Curador | Publicar | $len = 30$ | $len = 2$ | $len = 50$ | 2 tags | Nenhum | HTTP 400: "Fonte deve conter no mínimo 3 caracteres." | - | Não executado |
| CT-011-06 | Curador | Publicar | $len = 30$ | $len = 101$ | $len = 50$ | 2 tags | Nenhum | HTTP 400: "Fonte não pode exceder 100 caracteres." | - | Não executado |
| CT-011-07 | Curador | Publicar | $len = 30$ | $len = 10$ | $len = 19$ | 2 tags | Nenhum | HTTP 400: "O texto do conteúdo deve conter no mínimo 20 caracteres." | - | Não executado |
| CT-011-08 | Curador | Publicar | $len = 30$ | $len = 10$ | $len = 10001$ | 2 tags | Nenhum | HTTP 400: "O texto do conteúdo não pode ultrapassar 10000 caracteres." | - | Não executado |
| CT-011-09 | Curador | Publicar | $len = 30$ | $len = 10$ | $len = 50$ | 0 tags | Nenhum | HTTP 400: "Selecione pelo menos 1 tag." | - | Não executado |
| CT-011-10 | Curador | Publicar | $len = 30$ | $len = 10$ | $len = 50$ | 6 tags | Nenhum | HTTP 400: "Número máximo de 5 tags excedido." | - | Não executado |
| CT-011-11 | Curador | Publicar | $len = 30$ | $len = 10$ | $len = 50$ | 2 tags | PDF 5.1 MB | HTTP 400: "O tamanho do anexo não pode ser maior que 5 MB." | - | Não executado |
| CT-011-12 | Convivente | Publicar | $len = 30$ | $len = 10$ | $len = 50$ | 2 tags | Nenhum | HTTP 403: "Usuário não possui perfil de curador." | - | Não executado |
| CT-011-13 | Curador | Editar ($id=1$) | $len = 5$ | Mantido | Mantido | Mantido | Mantido | HTTP 200: "Conteúdo atualizado com sucesso." | - | Não executado |
| CT-011-14 | Curador | Editar ($id=1$) | $len = 121$ | Mantido | Mantido | Mantido | Mantido | HTTP 400; atualização rejeitada por tamanho excessivo | - | Não executado |
| CT-011-15 | Curador | Editar ($id=9999$) | $len = 30$ | Mantido | Mantido | Mantido | Mantido | HTTP 404 Not Found; artigo não localizado | - | Não executado |
| CT-011-16 | Curador | Remover ($id=1$) | Confirmação: Sim | N/A | N/A | N/A | N/A | HTTP 200/204; registro excluído com sucesso | - | Não executado |
| CT-011-17 | Curador | Remover ($id=1$) | Confirmação: Não | N/A | N/A | N/A | N/A | Exclusão cancelada; artigo preservado na base | - | Não executado |
| CT-011-18 | Curador | Remover ($id=9999$) | Confirmação: Sim | N/A | N/A | N/A | N/A | HTTP 404 Not Found; registro inexistente | - | Não executado |
| CT-011-19 | Convivente | Remover ($id=1$) | Confirmação: Sim | N/A | N/A | N/A | N/A | HTTP 403 Forbidden; apenas curadores podem excluir | - | Não executado |

---

### 3.8 CDU023 – Interação em Postagens

* **Responsável:** Lorrany Fagundes Campos da Silva
* **Ator Principal:** Convivente
* **Pré-condição:** Usuário autenticado e membro da comunidade com postagem ativa no feed.
* **Pós-condição:** Comentário registrado e listado abaixo da publicação.

#### 3.8.1 Classes de Equivalência e Fronteiras

| Campo | Condição | Classe Válida | Classe Inválida | Resultado Esperado |
| :--- | :--- | :--- | :--- | :--- |
| `comentario` | Tamanho do texto ($1 \le len \le 280$) | $1 \le len \le 280$ caracteres | $len = 0$ (vazio) ou $len > 280$ caracteres | Válido registra comentário; inválido exibe erro |
| `permissao` | Associação à comunidade | Membro da comunidade | Não membro da comunidade | Membro pode comentar; não membro é impedido |

#### 3.8.2 Análise do Valor Limite (AVL)

* **Limite inferior:** 0 caracteres (vazio - inválido) e 1 caractere (mínimo válido).
* **Limite superior:** 280 caracteres (máximo válido) e 281 caracteres (acima do limite - inválido).

#### 3.8.3 Tabela de Casos de Teste – CDU023

| ID | Cenário | Dados de Entrada | Resultado Esperado | Resultado Obtido | Situação |
| :---: | :--- | :--- | :--- | :---: | :---: |
| CDT-023-01 | Limite inferior válido de comentário | Comentário com 1 caractere (`"A"`) | Comentário publicado com sucesso na postagem | - | Não executado |
| CDT-023-02 | Limite inferior inválido (Vazio) | Comentário com 0 caracteres (`""`) | Bloqueio: "Não foi possível publicar seu comentário. Verifique o conteúdo e tente novamente." | - | Não executado |
| CDT-023-03 | Limite superior válido de comentário | Comentário com 280 caracteres | Comentário publicado e exibido integralmente sem cortes | - | Não executado |
| CDT-023-04 | Limite superior inválido de comentário | Comentário com 281 caracteres | Bloqueio do envio com alerta de limite excedido ou digitação travada em 280 caracteres | - | Não executado |

---

### 3.9 CDU024 – Moderar Conviventes

* **Responsável:** Aaron Guerra Goldberg
* **Ator Principal:** Moderador
* **Pré-condição:** Usuário autenticado como moderador da comunidade; membro alvo existente e distinto do moderador.
* **Pós-condição:** Ação de moderação registrada no histórico; se restrição, data de expiração calculada; se banimento, usuário movido para o grupo de banidos.

#### 3.9.1 Classes de Equivalência

| Campo / Condição | Classes Válidas | Classes Inválidas | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| Usuário Moderador | Autenticado e cadastrado como moderador do grupo | Anônimo ou convivente sem função de moderação | Permite moderação; inválido retorna HTTP 401/403 |
| `convivente_id` | ID de membro ativo diferente do moderador | Inexistente, não membro ou ID do moderador | Valida alvo; inválido retorna HTTP 400 ou 404 |
| `tipo` | `"restringir"` ou `"banir"` | Valor ausente ou fora das opções previstas | Aplica ação; inválido retorna HTTP 400 |
| `duracao_dias` | Inteiro maior ou igual a 1 (para restrição) | Ausente, nulo, zero ou número negativo | Restrição aplicada; inválido retorna HTTP 400 |
| `justificativa` | Texto não vazio (para banimento) | Ausente, vazio ou contendo apenas espaços | Aplica banimento; inválido retorna HTTP 400 |

#### 3.9.2 Análise do Valor Limite (AVL)

* **`duracao_dias`:**
  * `0`: abaixo do mínimo (inválido).
  * `1`: mínimo válido (expiração em 1 dia).
  * `2`: imediatamente acima do mínimo válido.
* **`justificativa`:**
  * `""` ou `"   "`: limite inválido.
  * `"a"` (1 caractere): limite inferior aceito.

#### 3.9.3 Tabela de Casos de Teste – CDU024

| ID | Cenário | Dados de Entrada | Resultado Esperado | Resultado Obtido | Situação |
| :--- | :--- | :--- | :--- | :---: | :---: |
| MOD-01 | Restringir membro com duração mínima | Moderador; membro válido; `tipo=restringir`; `duracao_dias=1` | HTTP 201; ação registrada com expiração em 24 horas | - | Não executado |
| MOD-02 | Restringir com 2 dias de duração | Moderador; membro válido; `tipo=restringir`; `duracao_dias=2` | HTTP 201; restrição salva com expiração em 48 horas | - | Não executado |
| MOD-03 | Restringir com duração zero | `duracao_dias=0` | HTTP 400; nenhuma penalidade persistida | - | Não executado |
| MOD-04 | Banir com justificativa mínima | Moderador; membro válido; `tipo=banir`; `justificativa="a"` | HTTP 201; membro movido para banidos | - | Não executado |
| MOD-05 | Banimento sem justificativa | `tipo=banir`; `justificativa=""` ou `"   "` | HTTP 400; nenhum banimento registrado | - | Não executado |
| MOD-06 | Tipo de ação inválido | `tipo="advertir"` | HTTP 400; comando de moderação inválido | - | Não executado |
| MOD-07 | Alvo inexistente | `convivente_id = 99999` | HTTP 404 Not Found | - | Não executado |
| MOD-08 | Moderar a si mesmo | `convivente_id = id_do_moderador` | HTTP 400; moderador não pode punir a si próprio | - | Não executado |
| MOD-09 | Convivente restrito tenta postar | Sessão de membro com restrição vigente | HTTP 403 Forbidden; postagem bloqueada | - | Não executado |
| MOD-10 | Convivente banido tenta entrar | Sessão de membro banido | HTTP 403 Forbidden; adesão bloqueada | - | Não executado |

---

### 3.10 CDU025 – Analisar Denúncias

* **Responsável:** Aaron Guerra Goldberg
* **Ator Principal:** Moderador
* **Pré-condição:** Moderador autenticado; existência de denúncia com status pendente na comunidade.
* **Pós-condição:** Denúncia marcada como aprovada ou reprovada com registro do moderador; se aprovada, postagem ou comentário denunciado é removido.

#### 3.10.1 Classes de Equivalência

| Campo / Condição | Classes Válidas | Classes Inválidas | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| Moderador | Usuário logado moderador da comunidade | Anônimo ou usuário sem permissão | Permite auditoria; inválido retorna HTTP 401/403 |
| `denuncia_id` | Denúncia existente vinculada à comunidade | ID inexistente ou de outra comunidade | Localiza registro; inválido retorna HTTP 404 |
| `status` | `"pendente"` | Já analisada (`"aprovada"` ou `"reprovada"`) | Permite julgamento; denúncia já julgada retorna HTTP 400 |
| `acao` | `"aprovar"` ou `"reprovar"` | Valores distintos ou ausentes | Processa decisão; valor inválido retorna HTTP 400 |

#### 3.10.2 Análise do Valor Limite (AVL)

* **Identificador de Denúncia / Rota:**
  * `0`: abaixo do primeiro ID válido (HTTP 404).
  * ID existente: limite válido.
  * Próximo ID não cadastrado: imediatamente acima do limite válido (HTTP 404).
* **Transição de Estado:**
  * Estado antes da ação: `"pendente"` (aceita deliberação com HTTP 200).
  * Estado após a ação: `"aprovada"` / `"reprovada"` (segunda submissão bloqueada com HTTP 400).

#### 3.10.3 Tabela de Casos de Teste – CDU025

| ID | Cenário | Dados de Entrada | Resultado Esperado | Resultado Obtido | Situação |
| :--- | :--- | :--- | :--- | :---: | :---: |
| DEN-01 | Aprovar denúncia de postagem | Moderador; denúncia pendente; `acao=aprovar` | HTTP 200; status `aprovada`; postagem excluída | - | Não executado |
| DEN-02 | Aprovar denúncia de comentário | Moderador; denúncia de comentário; `acao=aprovar` | HTTP 200; comentário removido; postagem mantida | - | Não executado |
| DEN-03 | Reprovar denúncia | Moderador; denúncia pendente; `acao=reprovar` | HTTP 200; status `reprovada`; conteúdo mantido ativo | - | Não executado |
| DEN-04 | Reavaliar denúncia já julgada | Denúncia já com status `aprovada` | HTTP 400; decisão anterior inalterada | - | Não executado |
| DEN-05 | ID de denúncia abaixo do limite | `denuncia_id = 0` | HTTP 404 Not Found | - | Não executado |
| DEN-06 | ID de denúncia inexistente | `denuncia_id = 99999` | HTTP 404 Not Found | - | Não executado |
| DEN-07 | Ação de moderação inválida | `acao = "arquivar"` | HTTP 400; denúncia permanece pendente | - | Não executado |
| DEN-08 | Usuário sem permissão avalia | Convivente comum enviando decisão | HTTP 403 Forbidden; julgamento bloqueado | - | Não executado |

---

## 4. Testes Não Funcionais

### 4.1 RNF01 – Segurança de Acesso e Conformidade LGPD

* **Categoria:** Segurança
* **Automatizado:** Sim (suíte de testes automatizados via `pytest` e `APITestCase` do DRF)
* **Duração Estimada:** 5 minutos
* **Executado:** Não
* **Responsáveis:** João Pedro Dantas Magalhães e Ramon Couto Santos
* **Data Prevista:** 18/09/2026
* **Procedimentos:**
  1. Enviar requisições de escrita (`POST`, `PUT`, `DELETE`) para `/api/conteudos/` utilizando credenciais de Convivente comum e de visitante não autenticado.
  2. Tentar acessar endpoints administrativos de moderação (`/api/comunidades/{id}/moderar/`) utilizando tokens sem o privilégio de moderador do respectivo grupo.
  3. Validar se os dados sensíveis de usuários em relatos de fórum não são expostos em respostas de perfis anônimos.
* **Critérios de Aceitação:** O sistema deve barrar 100% das requisições não autorizadas com respostas HTTP 401 Unauthorized ou HTTP 403 Forbidden. Nenhuma informação de identificação pessoal restrita deve ser exposta publicamente.
* **Resultado:** Não executado

### 4.2 RNF02 – Desempenho e Tempo de Resposta em Alta Concorrência

* **Categoria:** Desempenho
* **Automatizado:** Sim (via testes de carga com Locust)
* **Duração Estimada:** 10 minutos
* **Executado:** Não
* **Responsáveis:** Fernando Yuri Vital De Aquino e Aaron Guerra Goldberg
* **Data Prevista:** 18/09/2026
* **Procedimentos:**
  1. Configurar carga simulada de 50 requisições simultâneas de leitura acessando a listagem de conteúdos educacionais (`GET /api/conteudos/`) e feed de comunidades (`GET /api/comunidades/1/posts/`) no ambiente Onrender.
  2. Medir o tempo de resposta, latência de banco de dados e taxa de sucesso das requisições.
* **Critérios de Aceitação:** 95% das requisições devem retornar em tempo inferior a 1,5 segundo, mantendo taxa de disponibilidade de 99% sem erros 5xx.
* **Resultado:** Não executado

---

## 5. Referências

1. FREIRE, Marília A. **Teste de Software: Técnicas e Critérios de Testes – Particionamento em Classes de Equivalência e Análise do Valor Limite**. Natal: IFRN, 2025.
2. MATOS, S.; FREIRE, M.; DUARTE, C.; VIEIRA, M. **Lista EURECA: Diretrizes de Design para Criação e Avaliação de Interfaces**. Natal: IFRN, 2024.
3. EQUIPE TEVEJO. **Documento de Visão e Glossário de Termos de Negócio do Projeto TeVejo**. Natal: IFRN, 2026.
4. EQUIPE TEVEJO. **Detalhamentos de Casos de Uso (CDU001 a CDU025)**. Natal: IFRN, 2026.
5. IFRN. **Documentos de Casos de Teste dos Projetos Conta Comigo e Bizzu**. Natal: IFRN, 2025/2026.
6. IFRN. **Modelo Padrão de Especificação de Casos de Teste (caso_de_teste.dot)**. Natal: IFRN.
