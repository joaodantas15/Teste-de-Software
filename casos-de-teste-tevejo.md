# 1. Introdução

Este documento reúne os casos de teste elaborados para validar os principais fluxos da aplicação TeVejo, desenvolvida no contexto da disciplina de Prática de Desenvolvimento de Software (PDS) no IFRN. Os testes aqui descritos abrangem diferentes casos de uso da aplicação, com o objetivo de assegurar que cada funcionalidade opere conforme os requisitos definidos.

Cada caso de teste inclui informações detalhadas sobre o cenário a ser avaliado, os dados de entrada necessários, resultados esperados e a aplicação formal dos critérios de Particionamento em Classes de Equivalência e Análise do Valor Limite (AVL).

### 1.1 Visão geral

O documento foi estruturado para garantir clareza e facilitar a consulta aos testes da aplicação TeVejo. Ele apresenta a introdução ao propósito dos testes, uma visão geral dos critérios de seleção dos casos de uso e, por fim, os testes funcionais com seus respectivos cenários, dados e resultados esperados, servindo como referência para as equipes de desenvolvimento e qualidade. <br> <br>
|-🗂️ **1. Introdução** <br>
| |- 📑 1.1 Visão geral <br>
|- 🗂️ **2. Histórico de Revisões** <br>
|- 🗂️ **3. Responsáveis pela escrita** <br>
|- 🗂️ **4. Testes Funcionais** <br>
| |- 📑 4.1 CDU001. Fazer login <br>
| |- 📑 4.2 CDU002. Autocadastro <br>
| |- 📑 4.3 CDU003. Visualizar conteúdo educacional <br>
| |- 📑 4.4 CDU006. Participar de comunidade <br>
| |- 📑 4.5 CDU007. Postar nas comunidades <br>
| |- 📑 4.6 CDU008. Criar comunidade <br>
| |- 📑 4.7 CDU011. Gerenciar conteúdo educacional <br>
| |- 📑 4.8 CDU023. Interação em postagens <br>
| |- 📑 4.9 CDU024. Moderar conviventes <br>
| |- 📑 4.10 CDU025. Analisar denúncias <br>
|- 🗂️ **5. Testes Não Funcionais** <br>
|- 🗂️ **6. Referências** <br>

## 2. Histórico de Revisões

|    Data    | Versão |            Descrição            |      Autores      |
| :--------: | :----: | :-----------------------------: | :---------------: |
| 13/09/2026 |  1.0   | Testes dos CDU 003 e CDU 011    | João Pedro Dantas |
| 15/09/2026 |  2.0   | Testes dos CDU 001 e CDU 002    | Ramon Couto       |
| 15/09/2026 |  3.0   | Testes dos CDU 006 e CDU 007    | Fernando Yuri     |
| 15/09/2026 |  4.0   | Testes dos CDU 024 e CDU 025    | Aaron Goldberg    |
| 15/09/2026 |  5.0   | Testes dos CDU 008 e CDU 023    | Lorrany Fagundes  |
| 15/09/2026 |  6.0   | Unificação e padronização final | Equipe TeVejo     |

## 3. Responsáveis pela escrita
> Cada integrante ficou responsável pela escrita do teste por CDU implementado.

| CDU | Responsável |
| :--- | :--- |
| CDU001. Fazer login | Ramon Couto Santos |
| CDU002. Autocadastro | Ramon Couto Santos |
| CDU003. Visualizar conteúdo educacional | João Pedro Dantas Magalhães |
| CDU006. Participar de comunidade | Fernando Yuri Vital De Aquino |
| CDU007. Postar nas comunidades | Fernando Yuri Vital De Aquino |
| CDU008. Criar comunidade | Lorrany Fagundes Campos da Silva |
| CDU011. Gerenciar conteúdo educacional | João Pedro Dantas Magalhães |
| CDU023. Interação em postagens | Lorrany Fagundes Campos da Silva |
| CDU024. Moderar conviventes | Aaron Guerra Goldberg |
| CDU025. Analisar denúncias | Aaron Guerra Goldberg |

---

## 4. Testes funcionais

### 4.1. CDU001 - Fazer Login
Este documento especifica os testes que devem ser realizados para o caso de uso 001 - Fazer Login. Ele contém as informações necessárias para a construção dos scripts de teste, como preparação do ambiente, dados de entrada e resultados esperados.

#### Especificação do CDU
- **Ator principal:** Convivente, Curador, Moderador ou Administrador
- **Resumo:** O usuário pode se autenticar na plataforma utilizando seu username ou e-mail juntamente com sua senha.
- **Pré-condição:** Estar previamente cadastrado na plataforma; para sucesso, a conta deve estar ativa.
- **Pós-condição:** Usuário autenticado, sessão mantida e redirecionado para a página inicial ou para a URL indicada em `next`.

#### Casos essenciais derivados das classes

| Identificador | Senha | Parâmetro next | Status da conta | CSRF Token | Resultado Esperado | Resultado Obtido | Situação |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Username válido | Senha correta | ausente | Ativo (`True`) | Válido | HTTP 302 para página inicial; usuário autenticado | - | Não executado |
| E-mail válido | Senha correta | ausente | Ativo (`True`) | Válido | HTTP 302 para página inicial; usuário autenticado | - | Não executado |
| Username válido | Senha correta | `/conteudos/` | Ativo (`True`) | Válido | HTTP 302 para o destino solicitado em `next` | - | Não executado |
| Inexistente | Qualquer | ausente | N/A | Válido | Formulário reapresentado: "Usuário ou senha inválidos." | - | Não executado |
| Válido | Senha incorreta | ausente | Ativo (`True`) | Válido | Formulário reapresentado: "Usuário ou senha inválidos." | - | Não executado |
| Válido | Senha correta | ausente | Inativo (`False`)| Válido | Formulário reapresentado: "Usuário ou senha inválidos." | - | Não executado |
| Com espaços | Senha válida | ausente | Ativo (`True`) | Válido | Erro: "O nome de usuário não pode conter espaços." | - | Não executado |
| Vazio | Vazio | ausente | N/A | Válido | Formulário reapresentado com erro de campo obrigatório | - | Não executado |
| Válido | Senha correta | ausente | Ativo (`True`) | Ausente/Inválido | HTTP 403 Forbidden ou erro de sessão expirada | - | Não executado |

#### Classes de equivalência

- Obrigatórias: `identificador`, `senha`
- Opcionais: `next`

| Campo | Condições | Classes válidas | Classes inválidas | Resultado esperado |
| :--- | :--- | :--- | :--- | :--- |
| Identificador | Username ou e-mail cadastrado | Username ou e-mail existente (case-insensitive) | Identificador inexistente, vazio ou ausente | Inválido retorna erro de credenciais inválidas |
| Senha | Texto obrigatório | Senha exata vinculada ao usuário | Senha incorreta, vazia ou ausente | Inválido retorna erro de credenciais inválidas |
| Status da conta | Booleano `is_active` | `is_active=True` | `is_active=False` | Conta inativa não pode efetuar login |
| Username | Texto sem espaços | String sem espaços | String contendo um ou mais espaços | Erro: "O nome de usuário não pode conter espaços." |

#### Análise de valor limite

O campo `username` possui `max_length=150`. A análise avalia as fronteiras do tamanho do identificador e o tratamento de espaços.

| Caso | Entrada | Resultado esperado |
| :--- | :--- | :--- |
| Limite inferior válido | Username com 1 caractere | Campo validado; autenticação prossegue |
| Limite superior válido | Username com 150 caracteres | Campo validado; autenticação prossegue |
| Limite superior inválido | Username com 151 caracteres | HTTP 200/400 com erro de tamanho máximo |
| Espaço interno | Um caractere de espaço entre palavras | Erro: "O nome de usuário não pode conter espaços." |
| Espaços nas bordas | Espaços antes e depois de username válido | Espaços removidos via strip; autentica com sucesso |

---

### 4.2. CDU002 - Autocadastro
Este documento especifica os testes que devem ser realizados para o caso de uso 002 - Autocadastro. Ele contém as informações necessárias para a construção dos scripts de teste, como preparação do ambiente, dados de entrada e resultados esperados.

#### Especificação do CDU
- **Ator principal:** Convivente
- **Resumo:** Um novo usuário realiza seu próprio cadastro no sistema para acessar as comunidades e conteúdos.
- **Pré-condição:** Visitante não estar autenticado no sistema.
- **Pós-condição:** Conta persistida, vinculada ao grupo de permissão `Convivente` e direcionada para a tela de login.

#### Casos essenciais derivados das classes

| Username | Nome | E-mail | Senha | Confirmação | Foto (opcional) | Resultado Esperado | Resultado Obtido | Situação |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Inédito | 3 a 100 carac. | Válido e livre | >= 6 carac. | Idêntica | Vazio | HTTP 302 para login, conta criada como Convivente | - | Não executado |
| Inédito | 3 a 100 carac. | Válido e livre | >= 6 carac. | Idêntica | PNG válido | Conta criada com foto e redirecionamento | - | Não executado |
| Já cadastrado | 3 a 100 carac. | Válido e livre | >= 6 carac. | Idêntica | Vazio | Erro: "Nome de usuário já cadastrado." | - | Não executado |
| Inédito | 3 a 100 carac. | Já cadastrado | >= 6 carac. | Idêntica | Vazio | Erro: "E-mail já cadastrado." | - | Não executado |
| Inédito | 2 caracteres | Válido e livre | >= 6 carac. | Idêntica | Vazio | Erro: "O nome deve ter pelo menos 3 caracteres." | - | Não executado |
| Inédito | 3 a 100 carac. | Válido e livre | >= 6 carac. | Diferente | Vazio | Erro: "As senhas não coincidem." | - | Não executado |
| Inédito | 3 a 100 carac. | Válido e livre | 5 carac. | Idêntica | Vazio | Erro de validação: tamanho mínimo de senha | - | Não executado |
| Inédito | 3 a 100 carac. | Inválido | >= 6 carac. | Idêntica | Vazio | Erro de formato no campo de e-mail | - | Não executado |

#### Classes de equivalência

- Obrigatórias: `username`, `nome`, `email`, `password`, `password_confirm`
- Opcionais: `foto`, `biografia`

| Campo | Condições | Classes válidas | Classes inválidas | Resultado esperado |
| :--- | :--- | :--- | :--- | :--- |
| `username` | Texto único, sem espaços, até 150 caracteres | Inédito, sem espaços, $1 \le len \le 150$ | Vazio, com espaços, duplicado, $len > 150$ | Inválido impede criação e exibe erro |
| `nome` | Texto com $3 \le len \le 100$ | $3 \le len \le 100$ | Vazio, ausente, $len < 3$, $len > 100$ | Inválido retorna erro específico de tamanho |
| `email` | Formato padrão de e-mail | Endereço válido e inédito | Vazio, formato inválido, já existente | Inválido retorna erro de validação ou unicidade |
| `password` | Mínimo de 6 caracteres | $len \ge 6$ e aprovada no validador | Vazia, $len < 6$, reprovada em política | Inválido rejeita o cadastro |
| `password_confirm`| Confirmação de senha | Igual à senha | Diferente da senha, vazia | Rejeitado com "As senhas não coincidem." |

#### Análise de valor limite

| Caso | Campo | Entrada | Resultado esperado |
| :--- | :--- | :--- | :--- |
| Limite inferior inválido | `nome` | 2 caracteres | Erro: "O nome deve ter pelo menos 3 caracteres." |
| Limite inferior válido | `nome` | 3 caracteres | Cadastro prossegue |
| Limite superior válido | `nome` | 100 caracteres | Cadastro prossegue |
| Limite superior inválido | `nome` | 101 caracteres | Erro de tamanho máximo |
| Limite superior válido | `username` | 150 caracteres | Cadastro prossegue |
| Limite superior inválido | `username` | 151 caracteres | Erro de tamanho máximo |
| Limite inferior inválido | `password` | 5 caracteres | Erro de tamanho mínimo |
| Limite inferior válido | `password` | 6 caracteres | Cadastro prossegue se aprovada em validadores |
| Limite inferior divergente | `password_confirm`| 1 caractere divergente | Erro: "As senhas não coincidem." |

---

### 4.3. CDU003 - Visualizar Conteúdo Educacional
Este documento especifica os testes que devem ser realizados para o caso de uso 003 - Visualizar Conteúdo Educacional. Ele contém as informações necessárias para a construção dos scripts de teste, como preparação do ambiente, dados de entrada e resultados esperados.

#### Especificação do CDU
- **Ator principal:** Convivente
- **Atores secundários:** Curador
- **Resumo:** O convivente acessa a área de conteúdos e pode listar ou ler artigos informativos verificados por profissionais sobre TEA.
- **Pré-condição:** Estar logado na plataforma e existirem conteúdos educacionais disponíveis.
- **Pós-condição:** O conteúdo educacional selecionado é exibido de maneira completa.

#### Casos essenciais derivados das classes

| Autenticação | conteudo_id | Quantidade de conteúdos na base | Filtro / Tag | Resultado Esperado | Resultado Obtido | Situação |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Convivente logado | N/A (listagem) | 0 artigos | N/A | HTTP 200, exibe "Nenhum conteúdo educacional disponível no momento." | - | Não executado |
| Convivente logado | N/A (listagem) | 1 artigo | N/A | HTTP 200, exibe listagem com exatamente 1 artigo curado | - | Não executado |
| Convivente logado | ID 1 (existente) | >= 1 artigos | N/A | HTTP 200, abre página do artigo com corpo completo e autor | - | Não executado |
| Convivente logado | ID 0 (inválido) | >= 1 artigos | N/A | HTTP 400 / 404, exibe "Não foi possível carregar o conteúdo." | - | Não executado |
| Convivente logado | ID 999999 (inexistente) | >= 1 artigos | N/A | HTTP 404, exibe "Não foi possível carregar o conteúdo. Tente novamente mais tarde." | - | Não executado |
| Convivente logado | N/A | >= 1 artigos | 1 caractere ("A") | HTTP 200, listagem filtrada pelos artigos com a tag | - | Não executado |
| Convivente logado | N/A | >= 1 artigos | 31 caracteres | HTTP 400, "Termo de busca excede o limite de 30 caracteres." | - | Não executado |
| Visitante anônimo | ID 1 | >= 1 artigos | N/A | HTTP 401 / Redirecionamento obrigatório para login | - | Não executado |

#### Classes de equivalência

- Obrigatórias: `conteudo_id` (para leitura)
- Contexto / Busca: `quantidade_conteudos`, `filtro_tag`

| Campo | Condições | Classes válidas | Classes inválidas | Resultado esperado |
| :--- | :--- | :--- | :--- | :--- |
| `conteudo_id` | Identificador primário no banco | Inteiro existente ($id \ge 1$) | ID zero ($0$), negativo ($< 0$), não numérico | Válido retorna HTTP 200; inválido retorna HTTP 400 ou 404 |
| `quantidade_conteudos` | Registros cadastrados na base | $N \ge 1$ artigos | $N = 0$ artigos | Válido lista os itens; inválido exibe mensagem de repositório vazio |
| `filtro_tag` | Tamanho da string de busca | $1 \le len \le 30$ caracteres | String vazia ($0$) ou $len > 30$ | Válido filtra a lista; acima do limite retorna HTTP 400 |

#### Análise de valor limite

#### 1) `quantidade_conteudos` (listagem no repositório)
Faixa válida para lista com itens: $N \ge 1$.

| Caso | Entrada | Resultado esperado |
| :--- | :--- | :--- |
| Limite inferior inválido | $N = 0$ artigos no banco | HTTP 200, mensagem "Nenhum conteúdo educacional disponível no momento." |
| Limite inferior válido | $N = 1$ artigo no banco | HTTP 200, listagem renderiza exatamente 1 card |
| Valor nominal | $N = 5$ artigos no banco | HTTP 200, listagem renderiza os 5 cards com sucesso |

#### 2) `conteudo_id` (recuperação de artigo)
Faixa válida: $id \in [1, \infty)$.

| Caso | Entrada | Resultado esperado |
| :--- | :--- | :--- |
| Abaixo do mínimo | `conteudo_id = 0` | HTTP 400 / 404, identificador inválido |
| Limite inferior válido | `conteudo_id = 1` | HTTP 200, exibe artigo completo |
| Limite superior inexistente | `conteudo_id = 999999` | HTTP 404, "Não foi possível carregar o conteúdo. Tente novamente mais tarde." |

#### 3) `filtro_tag` (tamanho da busca)
Faixa válida: $1 \le len(termo) \le 30$.

| Caso | Entrada | Resultado esperado |
| :--- | :--- | :--- |
| Abaixo do mínimo | $len(termo) = 0$ | HTTP 200, busca ignorada, listagem completa |
| Limite inferior válido | $len(termo) = 1$ (`"A"`) | HTTP 200, listagem filtrada por "A" |
| Limite superior válido | $len(termo) = 30$ | HTTP 200, filtro aplicado com 30 caracteres |
| Acima do máximo | $len(termo) = 31$ | HTTP 400, "Termo de busca excede o limite de 30 caracteres." |

---

### 4.4. CDU006 - Participar de Comunidade
Este documento especifica os testes que devem ser realizados para o caso de uso 006 - Participar de Comunidade. Ele contém as informações necessárias para a construção dos scripts de teste, como preparação do ambiente, dados de entrada e resultados esperados.

#### Especificação do CDU
- **Ator principal:** Convivente
- **Resumo:** O usuário convivente pode se vincular como membro a comunidades de seu interesse para interagir nas postagens.
- **Pré-condição:** Estar autenticado na plataforma.
- **Pós-condição:** Convivente incluído no grupo de membros da comunidade e contador atualizado.

#### Casos essenciais derivados das classes

| Usuário | Comunidade | Vínculo Atual | Resultado Esperado | Resultado Obtido | Situação |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Convivente autenticado | ID 1 (Autismo Adulto) | Não é membro | Membro adicionado, contador incrementado, botão exibe "Membro" | - | Não executado |
| Convivente autenticado | ID 3 (Rotina e Terapias)| Não é membro | Membro adicionado, contador incrementado, botão exibe "Membro" | - | Não executado |
| Convivente autenticado | ID 1 (Autismo Adulto) | Já é membro | Erro: "Você já é membro desta comunidade." | - | Não executado |
| Convivente autenticado | ID 2 (Pais e Mães) | Moderador | Erro: "O moderador já é membro da comunidade." | - | Não executado |
| Convivente autenticado | ID 2 (Pais e Mães) | Banido | Erro: "Você foi banido desta comunidade." | - | Não executado |
| Convivente autenticado | ID 0 (Abaixo do mín.) | - | Erro: "Comunidade não encontrada." (HTTP 404) | - | Não executado |
| Convivente autenticado | ID 4 (Acima do máx.) | - | Erro: "Comunidade não encontrada." (HTTP 404) | - | Não executado |
| Curador autenticado | ID 1 (Autismo Adulto) | Não é membro | Erro: "Apenas Conviventes podem realizar esta ação." (HTTP 403) | - | Não executado |
| Visitante não autenticado| ID 1 (Autismo Adulto) | - | Redirecionamento obrigatório para login | - | Não executado |

#### Classes de equivalência

| Campo | Condições | Classes válidas | Classes inválidas | Resultado esperado |
| :--- | :--- | :--- | :--- | :--- |
| Perfil | Usuário autenticado | Perfil Convivente | Curador, visitante anônimo | Convivente ingressa; curador/anônimo é barrado |
| Comunidade | Identificador da comunidade | ID existente na base | ID inexistente ($id=0$, $id=4$) | Existente associa; inexistente retorna HTTP 404 |
| Vínculo | Estado de participação | Não participante | Já membro, moderador da com., banido | Apenas não participante tem adesão permitida |

#### Análise de valor limite

A AVL aplica-se sobre a faixa de IDs das comunidades existentes cadastradas na preparação do ambiente (faixa válida: $[1, 3]$):

| Caso | Entrada | Resultado esperado |
| :--- | :--- | :--- |
| Abaixo do menor ID | `id = 0` | HTTP 404, "Comunidade não encontrada." |
| Menor ID válido | `id = 1` | Processamento de adesão realizado com sucesso |
| Maior ID cadastrado | `id = 3` | Processamento de adesão realizado com sucesso |
| Acima do maior ID | `id = 4` | HTTP 404, "Comunidade não encontrada." |

---

### 4.5. CDU007 - Postar nas Comunidades
Este documento especifica os testes que devem ser realizados para o caso de uso 007 - Postar nas Comunidades. Ele contém as informações necessárias para a construção dos scripts de teste, como preparação do ambiente, dados de entrada e resultados esperados.

#### Especificação do CDU
- **Ator principal:** Convivente
- **Resumo:** O usuário membro de uma comunidade pode redigir e submeter postagens/discussões no feed da comunidade.
- **Pré-condição:** Estar autenticado e ser membro ativo sem restrições na comunidade.
- **Pós-condição:** Publicação salva e exibida no feed da comunidade.

#### Casos essenciais derivados das classes

| Usuário | Comunidade / Vínculo | Título | Conteúdo | Resultado Esperado | Resultado Obtido | Situação |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Convivente | Com. 1 / Membro | `"Minha rotina"` (12 carac.) | `"Rotina estruturada ajudou"` (27 carac.) | Post publicado com sucesso no feed | - | Não executado |
| Convivente | Com. 1 / Membro | `"A"` (1 carac.) | `"A"` (1 carac.) | Post publicado com sucesso no feed | - | Não executado |
| Convivente | Com. 1 / Membro | 49 caracteres | `"Texto explicativo"` | Post publicado com sucesso no feed | - | Não executado |
| Convivente | Com. 1 / Membro | 50 caracteres | `"Texto explicativo"` | Post publicado com sucesso no feed | - | Não executado |
| Convivente | Com. 1 / Membro | 51 caracteres | `"Texto explicativo"` | Erro: título excede 50 caracteres | - | Não executado |
| Convivente | Com. 1 / Membro | `""` (0 carac.) | `"Olá comunidade"` | Erro: "O título da postagem é obrigatório." | - | Não executado |
| Convivente | Com. 1 / Membro | `"   "` (3 espaços) | `"Olá comunidade"` | Erro: "O título da postagem é obrigatório." | - | Não executado |
| Convivente | Com. 3 / Restrito | `"Dúvida"` | `"Texto"` | Erro: "Você está restrito de postar nesta comunidade." | - | Não executado |
| Convivente | Com. 3 / Membro | `"Dúvida"` | `""` (0 carac.) | Erro: "O conteúdo da postagem não pode estar vazio" | - | Não executado |
| Convivente | Com. 2 / Não membro | `"Primeiro post"` | `"Texto"` | Erro: "Você precisa participar da comunidade para publicar" | - | Não executado |
| Anônimo | Com. 1 | `"Primeiro post"` | `"Texto"` | Redirecionamento obrigatório para login | - | Não executado |

#### Classes de equivalência

| Campo | Condições | Classes válidas | Classes inválidas | Resultado esperado |
| :--- | :--- | :--- | :--- | :--- |
| `titulo` | Texto obrigatório; até 50 caracteres | Preenchido com $1 \le len \le 50$ | Vazio, só espaços, $len > 50$ | Inválido bloqueia criação |
| `conteudo` | Texto obrigatório | Preenchido com $len \ge 1$ | Vazio, composto só por espaços | Inválido bloqueia criação |
| Vínculo | Participação na comunidade | Membro ativo sem restrição | Não participante, usuário restrito | Inválido retorna erro de permissão |

#### Análise de valor limite

#### 1) `titulo` (faixa válida $[1, 50]$)

| Caso | Entrada | Resultado esperado |
| :--- | :--- | :--- |
| Limite inferior inválido | `""` (0) ou `"   "` (espaços) | Erro: "O título da postagem é obrigatório." |
| Limite inferior válido | 1 caractere (`"A"`) | Post publicado com sucesso |
| Limite superior válido | 50 caracteres | Post publicado com sucesso |
| Limite superior inválido | 51 caracteres | Erro: o título não pode ter mais de 50 caracteres |

#### 2) `conteudo` (campo TEXT com presença obrigatória)

| Caso | Entrada | Resultado esperado |
| :--- | :--- | :--- |
| Limite inferior inválido | `""` (0) ou `"   "` (espaços) | Erro: "O conteúdo da postagem não pode estar vazio" |
| Limite inferior válido | 1 caractere (`"A"`) | Post publicado com sucesso |

---

### 4.6. CDU008 - Criar Comunidade
Este documento especifica os testes que devem ser realizados para o caso de uso 008 - Criar Comunidade. Ele contém as informações necessárias para a construção dos scripts de teste, como preparação do ambiente, dados de entrada e resultados esperados.

#### Especificação do CDU
- **Ator principal:** Convivente
- **Resumo:** O usuário pode fundar uma nova comunidade temática, tornando-se automaticamente seu moderador responsável.
- **Pré-condição:** Estar autenticado na plataforma.
- **Pós-condição:** Comunidade persistida no sistema e usuário definido como moderador.

#### Casos essenciais derivados das classes

| Cenário | Entrada (Nome da comunidade) | Autenticação | Resultado Esperado | Resultado Obtido | Situação |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Limite inferior válido | Nome com 3 caracteres (`"ABC"`) | Convivente logado | Comunidade criada com sucesso; usuário é moderador | - | Não executado |
| Limite inferior inválido | Nome com 2 caracteres (`"AB"`) | Convivente logado | Erro: o nome deve ter no mínimo 3 caracteres | - | Não executado |
| Limite superior válido | Nome inédito com 50 caracteres | Convivente logado | Comunidade criada com sucesso e redirecionamento | - | Não executado |
| Limite superior inválido | Nome com 51 caracteres | Convivente logado | Erro: o limite máximo de 50 caracteres foi excedido | - | Não executado |
| Usuário não autenticado | Nome válido de 15 caracteres | Não logado | Redirecionamento obrigatório para a tela de login | - | Não executado |

#### Classes de equivalência

| Campo | Condições | Classes válidas | Classes inválidas | Resultado esperado |
| :--- | :--- | :--- | :--- | :--- |
| `nome` | Obrigatório; tamanho restrito | $3 \le len \le 50$ caracteres | $len < 3$, $len > 50$, vazio | Inválido bloqueia criação e exibe erro |
| `autenticacao` | Sessão ativa | Usuário logado | Usuário anônimo | Anônimo é redirecionado para login |

#### Análise de valor limite

Faixa válida de caracteres do nome: $[3, 50]$.

| Caso | Entrada | Resultado esperado |
| :--- | :--- | :--- |
| Limite inferior inválido | 2 caracteres | Erro indicando mínimo de 3 caracteres |
| Limite inferior válido | 3 caracteres | Comunidade criada com sucesso |
| Limite superior válido | 50 caracteres | Comunidade criada com sucesso |
| Limite superior inválido | 51 caracteres | Erro indicando limite máximo de 50 caracteres |

---

### 4.7. CDU011 - Gerenciar Conteúdo Educacional
Este documento especifica os testes que devem ser realizados para o caso de uso 011 - Gerenciar Conteúdo Educacional. Ele contém as informações necessárias para a construção dos scripts de teste, como preparação do ambiente, dados de entrada e resultados esperados.

#### Especificação do CDU
- **Ator principal:** Curador
- **Resumo:** O curador pode cadastrar novos artigos educativos, editar postagens existentes e remover materiais desatualizados.
- **Pré-condição:** Estar autenticado com perfil ativo de Curador.
- **Pós-condição:** Conteúdo educacional salvo, atualizado ou removido do repositório da plataforma.

#### Casos essenciais derivados das classes

| Perfil | Operação | titulo | fonte | corpo | tags | anexo | Resultado Esperado | Resultado Obtido | Situação |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Curador | Publicar | len = 5 | len = 3 | len = 20 | 1 tag | Nenhum | HTTP 201 Created; conteúdo salvo com autoria | - | Não executado |
| Curador | Publicar | len = 120 | len = 100 | len = 10000 | 5 tags | PDF 5.0 MB | HTTP 201 Created; conteúdo salvo com anexo | - | Não executado |
| Curador | Publicar | len = 4 | len = 10 | len = 50 | 2 tags | Nenhum | HTTP 400: "Título deve conter no mínimo 5 caracteres." | - | Não executado |
| Curador | Publicar | len = 121 | len = 10 | len = 50 | 2 tags | Nenhum | HTTP 400: "Título não pode exceder 120 caracteres." | - | Não executado |
| Curador | Publicar | len = 30 | len = 2 | len = 50 | 2 tags | Nenhum | HTTP 400: "Fonte deve conter no mínimo 3 caracteres." | - | Não executado |
| Curador | Publicar | len = 30 | len = 101 | len = 50 | 2 tags | Nenhum | HTTP 400: "Fonte não pode exceder 100 caracteres." | - | Não executado |
| Curador | Publicar | len = 30 | len = 10 | len = 19 | 2 tags | Nenhum | HTTP 400: "O texto do conteúdo deve conter no mínimo 20 caracteres." | - | Não executado |
| Curador | Publicar | len = 30 | len = 10 | len = 10001 | 2 tags | Nenhum | HTTP 400: "O texto do conteúdo não pode ultrapassar 10000 caracteres." | - | Não executado |
| Curador | Publicar | len = 30 | len = 10 | len = 50 | 0 tags | Nenhum | HTTP 400: "Selecione pelo menos 1 tag." | - | Não executado |
| Curador | Publicar | len = 30 | len = 10 | len = 50 | 6 tags | Nenhum | HTTP 400: "Número máximo de 5 tags excedido." | - | Não executado |
| Curador | Publicar | len = 30 | len = 10 | len = 50 | 2 tags | PDF 5.1 MB | HTTP 400: "O tamanho do anexo não pode ser maior que 5 MB." | - | Não executado |
| Convivente | Publicar | len = 30 | len = 10 | len = 50 | 2 tags | Nenhum | HTTP 403 Forbidden; apenas curadores podem gerenciar | - | Não executado |
| Curador | Editar (id 1) | len = 5 | Mantido | Mantido | Mantido | Mantido | HTTP 200; "Conteúdo atualizado com sucesso." | - | Não executado |
| Curador | Editar (id 1) | len = 121 | Mantido | Mantido | Mantido | Mantido | HTTP 400; atualização rejeitada por título longo | - | Não executado |
| Curador | Remover (id 1)| Confirmação: Sim | N/A | N/A | N/A | N/A | HTTP 200/204; conteúdo excluído do banco | - | Não executado |
| Curador | Remover (id 1)| Confirmação: Não | N/A | N/A | N/A | N/A | Exclusão abortada; conteúdo preservado | - | Não executado |

#### Classes de equivalência

- Obrigatórias: `titulo`, `fonte`, `corpo`, `tags`
- Opcionais: `anexo`

| Campo | Condições | Classes válidas | Classes inválidas | Resultado esperado |
| :--- | :--- | :--- | :--- | :--- |
| `titulo` | Texto obrigatório | $5 \le len \le 120$ caracteres | Vazio, $len < 5$, $len > 120$ | Inválido retorna HTTP 400 no campo `titulo` |
| `fonte` | Texto obrigatório | $3 \le len \le 100$ caracteres | Vazio, $len < 3$, $len > 100$ | Inválido retorna HTTP 400 no campo `fonte` |
| `corpo` | Texto obrigatório | $20 \le len \le 10000$ caracteres | Vazio, $len < 20$, $len > 10000$ | Inválido retorna HTTP 400 no campo `corpo` |
| `tags` | Seleção de tags | 1 a 5 tags | 0 tags, mais de 5 tags | Inválido retorna HTTP 400 para tags |
| `anexo` | Arquivo opcional | PDF/JPG/PNG com $\le 5.0$ MB | Arquivo $> 5.0$ MB, executável | Inválido retorna HTTP 400 para anexo |
| `perfil` | Autorização do usuário | Pertencente ao grupo Curador | Convivente ou anônimo | Sem perfil retorna HTTP 403 Forbidden |

#### Análise de valor limite

#### 1) `titulo` ($[5, 120]$)
- $len = 4$: abaixo do mínimo (HTTP 400).
- $len = 5$: limite inferior aceito.
- $len = 120$: limite superior aceito.
- $len = 121$: acima do máximo (HTTP 400).

#### 2) `fonte` ($[3, 100]$)
- $len = 2$: abaixo do mínimo (HTTP 400).
- $len = 3$: limite inferior aceito.
- $len = 100$: limite superior aceito.
- $len = 101$: acima do máximo (HTTP 400).

#### 3) `corpo` ($[20, 10000]$)
- $len = 19$: abaixo do mínimo (HTTP 400).
- $len = 20$: limite inferior aceito.
- $len = 10000$: limite superior aceito.
- $len = 10001$: acima do máximo (HTTP 400).

#### 4) `tags` ($[1, 5]$)
- $count = 0$: abaixo do mínimo (HTTP 400).
- $count = 1$: limite inferior aceito.
- $count = 5$: limite superior aceito.
- $count = 6$: acima do máximo (HTTP 400).

#### 5) `anexo` ($\le 5.0\text{ MB}$)
- $0.0\text{ MB}$ (sem anexo): aceito.
- $5.0\text{ MB}$: limite superior aceito.
- $5.1\text{ MB}$: acima do máximo (HTTP 400).

---

### 4.8. CDU023 - Interação em Postagens
Este documento especifica os testes que devem ser realizados para o caso de uso 023 - Interação em Postagens. Ele contém as informações necessárias para a construção dos scripts de teste, como preparação do ambiente, dados de entrada e resultados esperados.

#### Especificação do CDU
- **Ator principal:** Convivente
- **Resumo:** O usuário membro da comunidade pode interagir enviando comentários em postagens abertas no feed.
- **Pré-condição:** Estar autenticado e ser membro da comunidade em que o post está alocado.
- **Pós-condição:** Comentário registrado e listado abaixo do post.

#### Casos essenciais derivados das classes

| Cenário | Entrada (Tamanho do comentário) | Vínculo | Resultado Esperado | Resultado Obtido | Situação |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Limite inferior válido | 1 caractere (`"A"`) | Membro ativo | Comentário publicado com sucesso na postagem | - | Não executado |
| Limite inferior inválido | 0 caracteres (vazio) | Membro ativo | Erro: "Não foi possível publicar seu comentário." | - | Não executado |
| Limite superior válido | 280 caracteres | Membro ativo | Comentário publicado e renderizado sem cortes | - | Não executado |
| Limite superior inválido | 281 caracteres | Membro ativo | Bloqueio do envio por limite de caracteres excedido | - | Não executado |
| Convivente não membro | Comentário de 20 caracteres | Não membro | Erro: "Apenas membros podem comentar nesta postagem." | - | Não executado |

#### Classes de equivalência

| Campo | Condições | Classes válidas | Classes inválidas | Resultado esperado |
| :--- | :--- | :--- | :--- | :--- |
| `comentario` | Texto obrigatório; limite de caracteres | $1 \le len \le 280$ caracteres | $len = 0$ (vazio) ou $len > 280$ | Inválido bloqueia envio |
| `permissao` | Vínculo de membro | Membro da comunidade | Não membro da comunidade | Apenas membros podem enviar comentários |

#### Análise de valor limite

Faixa válida de caracteres do comentário: $[1, 280]$.

| Caso | Entrada | Resultado esperado |
| :--- | :--- | :--- |
| Abaixo do mínimo | 0 caracteres (vazio) | Bloqueio do envio e mensagem de erro |
| Limite inferior válido | 1 caractere | Comentário publicado com sucesso |
| Limite superior válido | 280 caracteres | Comentário publicado integralmente |
| Acima do máximo | 281 caracteres | Bloqueio do envio por violação do limite |

---

### 4.9. CDU024 - Moderar Conviventes
Este documento especifica os testes que devem ser realizados para o caso de uso 024 - Moderar Conviventes. Ele contém as informações necessárias para a construção dos scripts de teste, como preparação do ambiente, dados de entrada e resultados esperados.

#### Especificação do CDU
- **Ator principal:** Moderador
- **Resumo:** O moderador gerencia os conviventes de sua comunidade, podendo aplicar restrições temporárias ou banimentos permanentes.
- **Pré-condição:** Estar autenticado como moderador da respectiva comunidade; o alvo da ação deve ser um membro diferente do próprio moderador.
- **Pós-condição:** Ação registrada em histórico de auditoria; membro restrito recebe data de expiração ou banido é transferido para a lista de banidos.

#### Casos essenciais derivados das classes

| Cenário | Entrada | Resultado Esperado | Resultado Obtido | Situação |
| :--- | :--- | :--- | :--- | :--- |
| Restringir membro com duração mínima | Moderador; membro válido; `tipo=restringir`; `duracao_dias=1` | HTTP 201; restrição salva com expiração em 24h | - | Não executado |
| Restringir membro com 2 dias | Moderador; membro válido; `tipo=restringir`; `duracao_dias=2` | HTTP 201; restrição salva com expiração em 48h | - | Não executado |
| Duração de restrição inválida | `duracao_dias=0` | HTTP 400; nenhuma penalidade persistida | - | Não executado |
| Banir com justificativa mínima | Moderador; membro válido; `tipo=banir`; `justificativa="a"` | HTTP 201; membro movido para banidos | - | Não executado |
| Banimento sem justificativa | `tipo=banir`; `justificativa=""` ou `"   "` | HTTP 400; nenhum banimento registrado | - | Não executado |
| Tipo de ação inválido | `tipo="advertir"` | HTTP 400; comando de moderação inválido | - | Não executado |
| Alvo inexistente | `convivente_id = 99999` | HTTP 404 Not Found | - | Não executado |
| Auto-moderação | `convivente_id = id_do_moderador` | HTTP 400; moderador não pode aplicar ação contra si | - | Não executado |
| Convivente restrito tenta postar | Sessão de membro com restrição ativa | HTTP 403 Forbidden; postagem bloqueada | - | Não executado |
| Convivente banido tenta ingressar | Sessão de usuário banido | HTTP 403 Forbidden; ingresso impedido | - | Não executado |

#### Classes de equivalência

- Obrigatórias: `convivente_id`, `tipo`
- Condicionais: `duracao_dias` (para restrição), `justificativa` (para banimento)

| Campo | Condições | Classes válidas | Classes inválidas | Resultado esperado |
| :--- | :--- | :--- | :--- | :--- |
| Moderador | Permissão no grupo | Moderador da comunidade | Convivente comum ou anônimo | Apenas moderador tem acesso permitido |
| `convivente_id` | Alvo da penalidade | Membro da comunidade ($\ne$ moderador) | Inexistente, não membro ou o moderador | Inválido retorna HTTP 400 ou 404 |
| `tipo` | Domínio fechado | `"restringir"` ou `"banir"` | Fora do domínio, ausente | Inválido retorna HTTP 400 |
| `duracao_dias` | Prazo da restrição | Inteiro $\ge 1$ | Zero, negativo, nulo | Inválido retorna HTTP 400 |
| `justificativa` | Motivação do banimento| Texto preenchido | Vazio, composto apenas por espaços | Inválido retorna HTTP 400 |

#### Análise de valor limite

- **`duracao_dias`:**
  - `0`: abaixo do mínimo (HTTP 400).
  - `1`: limite inferior aceito (expiração em 1 dia).
  - `2`: valor acima do mínimo aceito.
- **`justificativa`:**
  - `""` ou `"   "`: limite inválido (HTTP 400).
  - `"a"` (1 caractere): limite inferior válido aceito.

---

### 4.10. CDU025 - Analisar Denúncias
Este documento especifica os testes que devem ser realizados para o caso de uso 025 - Analisar Denúncias. Ele contém as informações necessárias para a construção dos scripts de teste, como preparação do ambiente, dados de entrada e resultados esperados.

#### Especificação do CDU
- **Ator principal:** Moderador
- **Resumo:** O moderador acessa a fila de postagens e comentários denunciados pelos membros e delibera pela aprovação ou reprovação.
- **Pré-condição:** Estar autenticado como moderador e existir denúncia pendente na comunidade.
- **Pós-condição:** Denúncia concluída com auditoria do moderador; se aprovada, o conteúdo é excluído.

#### Casos essenciais derivados das classes

| Cenário | Entrada | Resultado Esperado | Resultado Obtido | Situação |
| :--- | :--- | :--- | :--- | :--- |
| Aprovar denúncia de postagem | Moderador; denúncia pendente de post; `acao=aprovar` | HTTP 200; status `aprovada`; postagem removida | - | Não executado |
| Aprovar denúncia de comentário| Moderador; denúncia de comentário; `acao=aprovar` | HTTP 200; status `aprovada`; comentário excluído | - | Não executado |
| Reprovar denúncia | Moderador; denúncia pendente; `acao=reprovar` | HTTP 200; status `reprovada`; conteúdo mantido | - | Não executado |
| Denúncia já analisada | Denúncia já com status `aprovada` | HTTP 400; decisão prévia inalterada | - | Não executado |
| ID abaixo do mínimo | `denuncia_id = 0` | HTTP 404 Not Found | - | Não executado |
| ID inexistente | `denuncia_id = 99999` | HTTP 404 Not Found | - | Não executado |
| Ação de moderação inválida | `acao = "arquivar"` | HTTP 400; denúncia permanece pendente | - | Não executado |
| Usuário comum tenta moderar | Convivente comum enviando deliberação | HTTP 403 Forbidden | - | Não executado |

#### Classes de equivalência

| Campo | Condições | Classes válidas | Classes inválidas | Resultado esperado |
| :--- | :--- | :--- | :--- | :--- |
| Moderador | Permissão na comunidade | Moderador autenticado da comunidade | Convivente comum ou anônimo | Apenas moderador acessa e analisa |
| `denuncia_id` | Identificador da denúncia | Denúncia pendente existente no grupo | ID inexistente ou de outra comunidade | Inválido retorna HTTP 404 |
| `status` | Estado da denúncia | `"pendente"` | `"aprovada"` ou `"reprovada"` | Apenas pendente aceita decisão |
| `acao` | Decisão tomada | `"aprovar"` ou `"reprovar"` | Valores divergentes ou ausente | Inválido retorna HTTP 400 |

#### Análise de valor limite

- **`denuncia_id`:**
  - `0`: abaixo do menor ID válido (HTTP 404).
  - ID cadastrado: válido, retorna denúncia.
  - Próximo ID não cadastrado: acima do limite, retorna HTTP 404.
- **Transição de estado:**
  - `"pendente"`: permite análise e transição (HTTP 200).
  - `"aprovada"` / `"reprovada"`: rejeita nova análise sobre a mesma denúncia (HTTP 400).

---

## 5. Testes Não Funcionais

### 5.1 RNF01 – Segurança de Acesso e Conformidade LGPD

* **Categoria:** Segurança
* **Automatizado:** Sim (via testes de integração Django REST Framework / `APITestCase`)
* **Duração Estimada:** 5 minutos
* **Executado:** Não
* **Responsáveis:** João Pedro Dantas Magalhães e Ramon Couto Santos
* **Data Prevista:** 18/09/2026
* **Procedimentos:**
  1. Enviar requisições de escrita (`POST`, `PUT`, `DELETE`) para `/api/conteudos/` utilizando credenciais de Convivente comum e de visitante não autenticado.
  2. Acessar endpoints de moderação (`/api/comunidades/{id}/moderar/`) utilizando tokens sem privilégio de moderador.
  3. Validar se relatos sensíveis de conviventes não são expostos em respostas de usuários anônimos.
* **Critérios de Aceitação:** O sistema deve barrar 100% das requisições não autorizadas com respostas HTTP 401 Unauthorized ou HTTP 403 Forbidden. Nenhuma informação pessoal sensível deve ser exposta publicamente.
* **Resultado:** Não executado

### 5.2 RNF02 – Desempenho e Tempo de Resposta em Alta Concorrência

* **Categoria:** Desempenho
* **Automatizado:** Sim (via testes de carga com Locust)
* **Duração Estimada:** 10 minutos
* **Executado:** Não
* **Responsáveis:** Fernando Yuri Vital De Aquino e Aaron Guerra Goldberg
* **Data Prevista:** 18/09/2026
* **Procedimentos:**
  1. Simular 50 requisições simultâneas de leitura na listagem de conteúdos educacionais (`GET /api/conteudos/`) e feed de comunidades (`GET /api/comunidades/1/posts/`) no ambiente Onrender.
  2. Medir o tempo de resposta e latência de banco de dados.
* **Critérios de Aceitação:** 95% das requisições devem responder em tempo inferior a 1,5 segundo, mantendo disponibilidade sem erros 5xx.
* **Resultado:** Não executado

---

## 6. Referências

1. FREIRE, Marília A. **Teste de Software: Técnicas e Critérios de Testes – Particionamento em Classes de Equivalência e Análise do Valor Limite**. Natal: IFRN, 2025.
2. MATOS, S.; FREIRE, M.; DUARTE, C.; VIEIRA, M. **Lista EURECA: Diretrizes de Design para Criação e Avaliação de Interfaces**. Natal: IFRN, 2024.
3. EQUIPE TEVEJO. **Documento de Visão e Glossário de Termos de Negócio do Projeto TeVejo**. Natal: IFRN, 2026.
4. EQUIPE TEVEJO. **Detalhamentos de Casos de Uso (CDU001 a CDU025)**. Natal: IFRN, 2026.
5. IFRN. **Documentos de Casos de Teste dos Projetos Conta Comigo e Bizzu**. Natal: IFRN, 2025/2026.
6. IFRN. **Modelo Padrão de Especificação de Casos de Teste (caso_de_teste.dot)**. Natal: IFRN.
