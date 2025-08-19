# 📊 Dashboard de Salários na Área de Dados

[![Demo – Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](<SUA_URL_PUBLICA>)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B.svg?logo=streamlit&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/FelipeBNogueira/dash-salarios-tech?style=social)](https://github.com/FelipeBNogueira/dash-salarios-tech/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/FelipeBNogueira/dash-salarios-tech)](https://github.com/FelipeBNogueira/dash-salarios-tech/commits)
[![Repo Size](https://img.shields.io/github/repo-size/FelipeBNogueira/dash-salarios-tech)](https://github.com/FelipeBNogueira/dash-salarios-tech)

**Análise interativa de salários na área de dados** (USD/BRL), com filtros por ano, senioridade, contrato, tamanho da empresa, busca por cargo e visualizações com Plotly.  
Construído com **Streamlit + Pandas + Plotly**.

> **Análise:** 
> https://dash-salaries-tech.streamlit.app/

## 📓 Sumário
- [Visão Geral](#-visão-geral)
- [Destaques](#-destaques)
- [Screenshots](#-screenshots)
- [Arquitetura & Dados](#-arquitetura--dados)
- [Começando (Local)](#comecando-local)
- [Configurações Opcionais](#configuracoes-opcionais)
- [Deploy no Streamlit Cloud](#deploy-streamlit-cloud)
- [Estrutura do Projeto](#estrutura-projeto)
- [Roadmap](#roadmap)
- [Contribuição](#contribuicao)
- [Licença](#licenca)
- [Suporte](#suporte)
- [FAQ](#faq)

## 🧩 Visão Geral
Este dashboard permite explorar **salários anuais** na área de dados por múltiplas dimensões:
**cargo**, **senioridade**, **tipo de contrato**, **tamanho da empresa**, **localidade** e
**modalidade de trabalho** (remoto/presencial/híbrido). Ele inclui **KPIs**, **gráficos
interativos** (Plotly) e a opção de **download** dos dados filtrados.

As visualizações foram pensadas para leitura rápida:
- **Top 10 cargos por salário médio** (rótulos **dentro** das barras);
- **Mediana por ano e senioridade** (rótulos nos pontos);
- **Distribuição de salários** (rótulos **fora** do histograma e espaçamento entre barras);
- **Mapa por país** para *Data Scientist*.

A moeda padrão é **USD**, com conversão opcional para **BRL** através de uma taxa configurável.
O carregamento de dados é otimizado com `@st.cache_data`.

## ✨ Destaques
- 🎛️ **Filtros completos**: ano, senioridade, tipo de contrato, tamanho da empresa e **busca por cargo digitando** (ex.: `data scientist; engineer`).
- 💱 **Conversão de moeda**: USD → BRL com taxa configurável na sidebar.
- 🧮 **KPIs principais**: média, mediana, P90, máximo, nº de registros e **cargo mais frequente**.
- 📈 **Gráficos otimizados (Plotly)**:
  - Top 10 cargos por salário médio (rótulos **dentro** das barras).
  - Mediana por ano e senioridade (rótulos nos pontos).
  - Distribuição de salários (histograma com rótulos **fora** e espaçamento entre barras).
  - Mapa por país para *Data Scientist*.
- ⤵️ **Exportação**: download do CSV conforme filtros ativos.
- ⚡ **Performance**: cache de dados com `@st.cache_data`.

## 🖼 Screenshots

| Visão Geral | Distribuições |
|---|---|
| ![Dashboard – Visão Geral](https://raw.githubusercontent.com/FelipeBNogueira/dash-salarios-tech/main/assets/capt-1.png) | ![Dashboard – Distribuições](https://raw.githubusercontent.com/FelipeBNogueira/dash-salarios-tech/main/assets/capt-2.png) |

| Geografia | Analítico |
|---|---|
| ![Dashboard – Analítico](https://raw.githubusercontent.com/FelipeBNogueira/dash-salarios-tech/main/assets/capt-3.png) | ![Dashboard – Geografia](https://raw.githubusercontent.com/FelipeBNogueira/dash-salarios-tech/main/assets/capt-4.png) |

## 🧱 Arquitetura & Dados

**Stack**
- **App/UI:** Streamlit
- **Gráficos:** Plotly Express
- **ETL leve / análise:** Pandas
- **Cache:** `@st.cache_data` (TTL 1h)

**Fonte de dados**
- CSV remoto (GitHub):
https://raw.githubusercontent.com/FelipeBNogueira/dash-salarios-tech/refs/heads/main/dados-imersao-final.csv


**Esquema esperado (colunas)**
- `ano` *(int)*  
- `cargo` *(str)*  
- `senioridade` *(str)*  
- `contrato` *(str)*  
- `tamanho_empresa` *(str)*  
- `remoto` *(str)*  
- `residencia_iso3` *(str, ISO-3166-1 alpha-3)*  
- `usd` *(float, salário anual em USD)*

**Observações**
- Conversão de moeda: USD → BRL pela taxa definida na sidebar.
- A filtragem ocorre antes do render; os gráficos usam a coluna derivada `valor = usd * fator`.

<a id="comecando-local"></a>
## 🚀 Começando (Local)

> Requisitos: **Python 3.10+**

### Passo a passo

```bash
# 1) Clonar o repositório
git clone https://github.com/FelipeBNogueira/dash-salarios-tech.git
cd dash-salarios-tech
```

```bash
# 2) (opcional) Criar ambiente virtual
python -m venv .venv
```

**Ativar o ambiente**

**Windows (PowerShell)**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

```bash
# 3) Instalar dependências
pip install -r requirements.txt
```

```bash
# 4) Executar o app
streamlit run app.py
```

**Dicas rápidas**
```bash
# Porta ocupada
streamlit run app.py --server.port 8502

# Teste do Streamlit
streamlit hello
```

**Windows/PowerShell (se scripts bloquearem)**
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

<a id="configuracoes-opcionais"></a>
## ⚙️ Configurações Opcionais

### `.streamlit/config.toml`
Crie a pasta `.streamlit/` na raiz do projeto e adicione o arquivo `config.toml`:

```toml
[server]
headless = true
runOnSave = true
port = 8502

[browser]
gatherUsageStats = false

# (opcional) Tema do app
[theme]
base = "light"                 # "dark" ou "light"
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#000000"
```

### Variáveis de ambiente (opcional)
Defina padrão de moeda e taxa de conversão se desejar:

**macOS/Linux**
```bash
export DEFAULT_CURRENCY=USD
export USD_BRL_RATE=5.50
streamlit run app.py
```

**Windows (PowerShell)**
```powershell
$env:DEFAULT_CURRENCY="USD"
$env:USD_BRL_RATE="5.50"
streamlit run app.py
```
<a id="deploy-streamlit-cloud"></a>
## ☁️ Deploy no Streamlit Cloud

### Passo a passo
1) **Commit & push** do projeto no GitHub (com `app.py`, `requirements.txt` e, se quiser, `.streamlit/config.toml`).
2) Acesse **https://share.streamlit.io/** e conecte sua conta do GitHub.
3) Clique em **New app** e selecione:
   - **Repository**: `FelipeBNogueira/dash-salarios-tech`
   - **Branch**: `main` (ou a que você usa)
   - **Main file path**: `app.py`
4) (Opcional) Em **Advanced settings**:
   - **Python version**: 3.10+
   - **Secrets** / **Environment variables** (se você usar):  
     `DEFAULT_CURRENCY=USD` • `USD_BRL_RATE=5.50`
5) Clique em **Deploy**. Ao finalizar, copie a **URL pública** e atualize o bloco “Demo” no topo do README.

### `requirements.txt` mínimo (se ainda não criou)
```txt
streamlit>=1.32
pandas
plotly
numpy
```

### Pós-deploy
- Atualize o README:  
  **Demo:** `https://SEU-APP.streamlit.app`
- Se precisar trocar a porta local ao testar: `streamlit run app.py --server.port 8502`

### Troubleshooting rápido
- **ModuleNotFoundError** → falta no `requirements.txt`.
- **App reiniciando a cada salvamento** → verifique `runOnSave=true` no `.streamlit/config.toml`.
- **Erro de dados remotos** → confirme a URL do CSV e conexão de rede do serviço.

<a id="estrutura-projeto"></a>
## 🗂️ Estrutura do Projeto

```
.
├── app.py                      # Aplicação Streamlit
├── requirements.txt            # Dependências do projeto
├── .streamlit/
│   └── config.toml             # Configurações opcionais (tema, porta, etc.)
├── assets/                     # Imagens usadas no README/app
│   ├── capt-1.png
│   ├── capt-2.png
│   ├── capt-3.png
│   └── capt-4.png
├── LICENSE                     # Licença MIT
└── README.md                   # Documentação do projeto
```

**Notas rápidas**
- **`app.py`**: contém o dashboard completo (filtros, KPIs e gráficos Plotly).
- **`requirements.txt`**: mínimo recomendado:
  ```
  streamlit>=1.32
  pandas
  plotly
  numpy
  ```
- **`assets/`**: mantenha as imagens referenciadas no README.
- **`.streamlit/config.toml`**: útil para `runOnSave`, tema e porta customizada.

<a id="roadmap"></a>
## 🗺️ Roadmap

- [ ] **Comparação de períodos** (ex.: 2025 vs 2023 lado a lado).
- [ ] **Salvar estado dos filtros na URL** (compartilhar links: `st.query_params`).
- [ ] **Exportar gráficos como imagem** (Plotly + `kaleido`).
- [ ] **Internacionalização (PT/EN)** com seletor de linguagem.
- [ ] **Aprimorar acessibilidade** (descrições de gráficos, contraste, teclado).
- [ ] **Melhorar performance** (tipagem de colunas, cache seletivo, TTL por recurso).
- [ ] **Validação de dados** (schema leve antes do render, tratamento de outliers).
- [ ] **Testes e CI** (lint/format com Ruff/Black, GitHub Actions).
- [ ] **Documentação ampliada** (tutorial rápido GIF/MP4, FAQ com prints).
- [ ] **Novas análises** (faixas por país para outros cargos, séries temporais por contrato).

<a id="contribuicao"></a>
## 🤝 Contribuição

Agradecemos contribuições! Siga este fluxo:

### 1) Fork & Branch
```bash
# (Contribuidores externos) clone o SEU fork — troque <seu_usuario> pelo seu GitHub
git clone https://github.com/<seu_usuario>/dash-salarios-tech.git
cd dash-salarios-tech
git checkout -b feat/minha-feature

# (Autor / acesso direto ao repositório oficial) você pode usar:
# git clone https://github.com/FelipeBNogueira/dash-salarios-tech.git
# cd dash-salarios-tech
# git checkout -b feat/minha-feature

# (opcional) manter seu fork atualizado com o repo oficial
git remote add upstream https://github.com/FelipeBNogueira/dash-salarios-tech.git
git fetch upstream
git merge upstream/main    # ou: git rebase upstream/main
```

### 2) Ambiente & Dependências
```bash
python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3) Padrões de Código
- **Formatação/Lint**: recomenda-se `black` e `ruff`.
```bash
python -m pip install -U black ruff
black .
ruff check .
```
- **Estilo de commit**: **Conventional Commits**  
  Exemplos:
  - `feat: adiciona filtro de país`
  - `fix: corrige rótulos do histograma`
  - `docs: atualiza seção de deploy`
  - `refactor: otimiza agrupamento por cargo`

### 4) Teste local
- Rode o app e verifique se tudo funciona:
```bash
streamlit run app.py
```

### 5) Pull Request
Abra um **PR** apontando para `main` e inclua:
- **Descrição clara** da mudança (o que/por quê).
- **Screenshots/GIF** quando visual.
- **Checklist**:
  - [ ] Código formatado/lintado
  - [ ] Testado localmente
  - [ ] README atualizado (se necessário)
  - [ ] Sem quebras conhecidas

### 6) Issues
- Use labels como `bug`, `feature`, `docs`, `help wanted`.
- Descreva *passos para reproduzir* (quando bug) e inclua **prints** se possível.

> Dica: mantenha PRs pequenos e focados para revisão mais rápida.

<a id="licenca"></a>
## 📝 Licença

Este projeto é distribuído sob a **MIT License**.  
Consulte o arquivo **[LICENSE](./LICENSE)** para os termos completos.

> Dica: mantenha o ano e o titular atualizados no arquivo `LICENSE`.

<a id="suporte"></a>
## 🆘 Suporte

- Abra uma **Issue** descrevendo o problema ou a sugestão:  
  https://github.com/FelipeBNogueira/dash-salarios-tech/issues
- Para **bugs**, inclua:
  - Passos para reproduzir
  - Comportamento esperado vs. observado
  - Logs/erros (se houver)
  - Print(s) de tela
  - Sistema operacional e versão do Python
- Para **features** (ideias/melhorias), descreva:
  - Caso de uso
  - Exemplo de interação/fluxo desejado
  - Mockups/prints (se possível)
- Contato direto (opcional): **felipe@potionsolutions.com**

> Dica: use labels nas issues (`bug`, `feature`, `docs`, `help wanted`) para acelerar o triage.

<a id="faq"></a>
## ❓ FAQ

**1) O app não abre em `localhost:8501`. O que fazer?**  
Use outra porta:
```bash
streamlit run app.py --server.port 8502
```

**2) Recebo `ModuleNotFoundError` ao fazer deploy.**  
Falta dependência no `requirements.txt`. Adicione e faça novo deploy.
```txt
streamlit>=1.32
pandas
plotly
numpy
```

**3) O PowerShell bloqueia a ativação do venv no Windows.**  
Abra o PowerShell como usuário e rode:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**4) Os gráficos não exibem os rótulos como no README.**  
Confirme que está usando a versão mais recente do `app.py`.  
No histograma, os rótulos estão **fora**; no Top 10, **dentro** das barras.

**5) O mapa por país não aparece.**  
Ele filtra somente *Data Scientist*. Verifique se o filtro de cargo permite essa categoria.  
Cheque também a coluna `residencia_iso3` no dataset filtrado.

**6) A conversão USD→BRL parece errada.**  
Ajuste a taxa de conversão na sidebar e confirme que a moeda está setada para **BRL**.

**7) O cache mostra dados antigos.**  
Limpe o cache do Streamlit:
```bash
streamlit cache clear
```
Ou altere o `ttl` do `@st.cache_data`.

**8) Minhas imagens não aparecem no README.**  
Use caminho relativo (`assets/capt-1.png`) **ou** URL crua do GitHub:
```
https://raw.githubusercontent.com/FelipeBNogueira/dash-salarios-tech/main/assets/capt-1.png
```

**9) O CSV remoto não carrega.**  
Verifique a URL:
```
https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/main/dados-imersao-final.csv
```
Teste local:
```python
import pandas as pd; print(pd.read_csv("URL_AQUI").head())
```

**10) Quero contribuir: clono o repo oficial ou faço fork?**  
- Quem contribui externamente: **fork** e depois `git clone https://github.com/<seu_usuario>/dash-salarios-tech.git`.  
- Autor/mantenedor: pode clonar direto `FelipeBNogueira/dash-salarios-tech`.

> Não achou sua dúvida aqui? Abra uma **Issue**:  
> https://github.com/FelipeBNogueira/dash-salarios-tech/issues
