# Relatório de Cobertura de Testes - Projeto TeVejo

**Aluno:** João Pedro Dantas Magalhães  
**Casos de Uso Responsáveis:**  
- **CDU003** – Visualizar Conteúdo Educacional  
- **CDU011** – Gerenciar Conteúdo Educacional  

---

## Parte 1: Cobertura Baseada em Requisitos (CDU003 e CDU011)

Segundo o material da disciplina, a cobertura de requisitos avalia quantos fluxos dos Casos de Uso foram planejados, implementados, executados e bem-sucedidos usando a fórmula:
**Cobertura = T / RfT** (onde **RfT** é o total de fluxos/requisitos dos casos de uso).

### 1.1. Levantamento dos Fluxos dos CDUs (RfT = 8 fluxos no total)

Somando todos os fluxos descritos nos documentos do CDU003 (3 fluxos) e do CDU011 (5 fluxos), temos **8 requisitos de teste (RfT = 8)**:

| Fluxo / Requisito | CDU | Planejado (Tp) | Implementado (Ti) | Executado (Tx) | Bem-sucedido (Ts) | Como foi testado no código |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1. Fluxo Principal:** Visualizar conteúdo disponível | CDU003 | Sim | Sim | Sim | Sim | Testado na criação e leitura de `ConteudoEducacional` e `Tags` |
| **2. Exceção I:** Nenhum conteúdo disponível | CDU003 | Sim | Não | Não | Não | Pendente teste de interface/view |
| **3. Exceção II:** Erro ao carregar o conteúdo | CDU003 | Sim | Não | Não | Não | Pendente teste de falha de conexão |
| **4. Fluxo Principal:** Adicionar conteúdo educacional | CDU011 | Sim | Sim | Sim | Sim | Testado por `test_conteudo_cria_com_sucesso` e `test_tag_cria_com_sucesso` |
| **5. Alternativo I:** Editar conteúdo existente | CDU011 | Sim | Não | Não | Não | Pendente teste unitário na camada de view/service |
| **6. Alternativo II:** Remover conteúdo | CDU011 | Sim | Não | Não | Não | Pendente teste unitário na camada de view/service |
| **7. Exceção I:** Dados inválidos no formulário | CDU011 | Sim | Sim | Sim | Sim | Testado por `test_conteudo_titulo_curto_falha`, `test_conteudo_fonte_curta_falha` e `test_tag_nome_curto_falha` |
| **8. Exceção II:** Falha técnica ao persistir | CDU011 | Sim | Não | Não | Não | Pendente simulação de queda do banco |

### 1.2. Cálculo das 4 Medições Obrigatórias

- **Testes Planejados (Tp):** Foram planejados testes para todos os 8 fluxos.
  `Cobertura (Tp) = 8 / 8 = 100%`
- **Testes Implementados (Ti):** Nesta etapa focada em Models, 3 fluxos possuem scripts de teste unitário implementados no arquivo `test_models.py` (compostos por 5 funções de teste).
  `Cobertura (Ti) = 3 / 8 = 37,5%`
- **Testes Executados (Tx):** Os 3 fluxos implementados foram executados via terminal.
  `Cobertura (Tx) = 3 / 8 = 37,5%`
- **Testes Bem-Sucedidos (Ts):** Todos os testes executados passaram sem erros (`OK`).
  `Cobertura (Ts) = 3 / 8 = 37,5%` (Taxa de êxito de **100%** dos testes executados: 3 de 3).

---

## Parte 2: Cobertura Baseada em Código (coverage.py)

Para medir a porcentagem exata de código executada pelos testes unitários no aplicativo `conteudos`, utilizamos a biblioteca **`coverage.py`** (versão 7.16.2).

### 2.1. Comandos Executados no Terminal

```bash
pip install coverage
coverage run --source='conteudos' manage.py test conteudos
coverage report -m
coverage html
