# Tutorial Completo de Git
### Do zero ao GitHub Pages com o projeto voos-brasil

---

## Índice

1. [O que é Git e por que usar](#1-o-que-é-git-e-por-que-usar)
2. [Instalação](#2-instalação)
3. [Configuração inicial](#3-configuração-inicial)
4. [Conceitos fundamentais](#4-conceitos-fundamentais)
5. [Criando um repositório](#5-criando-um-repositório)
6. [O ciclo básico: status → add → commit](#6-o-ciclo-básico-status--add--commit)
7. [Verificando o histórico](#7-verificando-o-histórico)
8. [Desfazendo alterações](#8-desfazendo-alterações)
9. [Branches (ramificações)](#9-branches-ramificações)
10. [GitHub: repositório remoto](#10-github-repositório-remoto)
11. [Clonando um repositório](#11-clonando-um-repositório)
12. [Push e Pull](#12-push-e-pull)
13. [Fork e Pull Request](#13-fork-e-pull-request)
14. [Resolvendo conflitos](#14-resolvendo-conflitos)
15. [O arquivo .gitignore](#15-o-arquivo-gitignore)
16. [Fluxo completo: publicando o voos-brasil](#16-fluxo-completo-publicando-o-voos-brasil)
17. [Referência rápida de comandos](#17-referência-rápida-de-comandos)

---

## 1. O que é Git e por que usar

**Git** é um sistema de controle de versão distribuído. Em termos simples, ele tira "fotos" do seu projeto ao longo do tempo, permitindo que você:

- Volte a qualquer ponto da história do projeto
- Trabalhe em paralelo sem quebrar o que já funciona
- Colabore com outras pessoas sem sobrescrever o trabalho delas
- Entenda o que mudou, quando e por quem

**GitHub** é uma plataforma online que hospeda repositórios Git e adiciona recursos como:

- Interface web para navegar no código
- GitHub Pages (hospedagem gratuita de sites estáticos)
- GitHub Actions (automação e CI/CD gratuitos)
- Issues, Pull Requests e revisão de código

---

## 2. Instalação

### Windows
Baixe o instalador em https://git-scm.com/download/win  
Durante a instalação, mantenha as opções padrão.

### macOS
```bash
# Via Homebrew (recomendado)
brew install git

# Ou instale as Xcode Command Line Tools
xcode-select --install
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install git
```

### Verificar instalação
```bash
git --version
# git version 2.x.x
```

---

## 3. Configuração inicial

Antes do primeiro uso, identifique-se. Essas informações aparecem em cada commit.

```bash
# Nome completo
git config --global user.name "Seu Nome"

# E-mail (use o mesmo do GitHub)
git config --global user.email "seu@email.com"

# Editor padrão (VS Code recomendado)
git config --global core.editor "code --wait"

# Branch padrão: main (padrão moderno)
git config --global init.defaultBranch main

# Verificar todas as configurações
git config --list
```

O flag `--global` aplica para todos os repositórios do seu usuário.  
Use `--local` (dentro de um repositório) para configurações específicas de projeto.

---

## 4. Conceitos fundamentais

```
┌─────────────────────────────────────────────────────────┐
│  Working Directory   │  Staging Area   │   Repository   │
│  (seus arquivos)     │  (index)        │   (.git/)      │
│                      │                 │                 │
│  arquivo.txt         │                 │                 │
│  (modificado) ──git add──►  preparado ──git commit──►  commit │
└─────────────────────────────────────────────────────────┘
```

| Conceito | O que é |
|---|---|
| **Repositório** | Pasta com todo o histórico do projeto (contém a pasta `.git/`) |
| **Commit** | Um "snapshot" salvo do projeto em um momento específico |
| **Staging Area** | Área de preparação — você escolhe o que vai entrar no próximo commit |
| **Branch** | Uma linha independente de desenvolvimento |
| **HEAD** | Ponteiro que indica em qual commit/branch você está agora |
| **Remote** | Um repositório em outro lugar (ex: GitHub) |
| **Clone** | Cópia completa de um repositório remoto para sua máquina |
| **Push** | Enviar commits locais para o remoto |
| **Pull** | Baixar e integrar commits do remoto para o local |

---

## 5. Criando um repositório

### Opção A — Iniciar do zero na sua máquina

```bash
# Criar e entrar na pasta do projeto
mkdir voos-brasil
cd voos-brasil

# Inicializar o repositório Git
git init
# Initialized empty Git repository in /caminho/voos-brasil/.git/

# A pasta .git/ foi criada — ela guarda todo o histórico
ls -la
```

### Opção B — Criar pelo GitHub e clonar (recomendado)

1. Acesse github.com → **New repository**
2. Preencha o nome: `voos-brasil`
3. Marque **Add a README file**
4. Clique em **Create repository**
5. Copie a URL do repositório e clone:

```bash
git clone https://github.com/seu-usuario/voos-brasil.git
cd voos-brasil
```

---

## 6. O ciclo básico: status → add → commit

Este é o fluxo que você vai repetir dezenas de vezes por dia.

### git status — ver o que mudou

```bash
git status
```

```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        index.html
        scripts/fetch_flights.py

nothing added to commit but untracked files present
```

Arquivos podem estar em 3 estados:
- **Untracked** — Git não conhece o arquivo ainda
- **Modified** — arquivo já rastreado mas com alterações não salvas
- **Staged** — preparado para o próximo commit

### git add — preparar arquivos

```bash
# Adicionar um arquivo específico
git add index.html

# Adicionar todos os arquivos de uma pasta
git add scripts/

# Adicionar TUDO (use com cuidado)
git add .

# Adicionar de forma interativa (recomendado para commits precisos)
git add -p
```

### git commit — salvar o snapshot

```bash
# Commit com mensagem curta
git commit -m "feat: adiciona painel de voos com filtro por estado"

# Commit com mensagem curta + descrição longa
git commit -m "feat: adiciona filtro por estado e município" -m "
- Popula select de estados a partir de airports.json
- Select de cidades filtra conforme o estado escolhido
- Select de aeroportos filtra conforme a cidade
- Seleção automática quando há apenas uma opção
"

# Atalho: add + commit juntos (só para arquivos JÁ rastreados)
git commit -am "fix: corrige horário no fuso de Brasília"
```

### Boas mensagens de commit

Use o padrão **Conventional Commits**:

| Prefixo | Quando usar |
|---|---|
| `feat:` | Nova funcionalidade |
| `fix:` | Correção de bug |
| `docs:` | Apenas documentação |
| `chore:` | Tarefas de manutenção (sem mudança funcional) |
| `refactor:` | Refatoração sem nova feature ou fix |
| `style:` | Formatação, espaçamento |
| `test:` | Testes |

```bash
# Exemplos
git commit -m "feat: adiciona filtro por companhia aérea"
git commit -m "fix: corrige exibição de data quando iso é null"
git commit -m "docs: atualiza README com instruções de deploy"
git commit -m "chore: atualiza dados de voos [skip ci]"
```

---

## 7. Verificando o histórico

```bash
# Log simples
git log

# Log compacto — uma linha por commit
git log --oneline

# Log com grafo de branches
git log --oneline --graph --all

# Ver o que mudou em um commit específico
git show abc1234

# Ver diferenças entre working directory e último commit
git diff

# Ver diferenças no staging area
git diff --staged

# Comparar dois commits
git diff abc1234 def5678
```

Exemplo de saída do `git log --oneline`:
```
a3f9c12 (HEAD -> main, origin/main) chore: atualiza dados de voos
b7e2d45 feat: adiciona filtro por estado e município
c1a8f30 feat: adiciona painel dark com bootstrap
d5b3e21 docs: cria README com instruções de deploy
e9c4f17 chore: inicializa projeto
```

---

## 8. Desfazendo alterações

### Antes do add (working directory)

```bash
# Descartar alterações em um arquivo (volta ao último commit)
git restore index.html

# Descartar TODAS as alterações não salvas
git restore .
```

### Depois do add (staging area)

```bash
# Remover do staging, mas manter as alterações no arquivo
git restore --staged index.html
```

### Depois do commit

```bash
# Criar um novo commit que desfaz o anterior (seguro — não reescreve histórico)
git revert abc1234

# Voltar o HEAD para um commit anterior (cuidado: descarta commits à frente)
# --soft: mantém alterações no staging
git reset --soft HEAD~1

# --mixed (padrão): mantém alterações no working directory
git reset HEAD~1

# --hard: descarta tudo — irreversível!
git reset --hard HEAD~1
```

> **Regra de ouro:** nunca use `reset` em commits que já foram enviados ao remoto (`push`). Use `revert` nesse caso.

### Corrigir a mensagem do último commit

```bash
git commit --amend -m "feat: mensagem corrigida"
```

---

## 9. Branches (ramificações)

Branches permitem trabalhar em funcionalidades isoladas sem afetar o código principal.

```
main       ●─────────────────────────────────●──● (merge)
                \                           /
feat/filtro      ●──●──●──●──●──●──●──●──●
```

### Criar e mudar de branch

```bash
# Ver branches existentes
git branch

# Criar uma nova branch
git branch feat/filtro-estado

# Mudar para ela
git checkout feat/filtro-estado

# Atalho: criar e mudar ao mesmo tempo (recomendado)
git checkout -b feat/filtro-estado

# Forma moderna (Git 2.23+)
git switch -c feat/filtro-estado
```

### Trabalhar na branch

```bash
# (faça suas alterações normalmente)
git add .
git commit -m "feat: adiciona select de estado"

git add .
git commit -m "feat: popula cidades conforme estado selecionado"
```

### Merge — integrar de volta ao main

```bash
# Voltar para main
git switch main

# Integrar a branch
git merge feat/filtro-estado

# Deletar a branch após o merge
git branch -d feat/filtro-estado
```

### Tipos de merge

```bash
# Fast-forward (sem commits novos no main — histórico linear)
git merge feat/filtro-estado

# Merge commit (preserva o histórico da branch)
git merge --no-ff feat/filtro-estado -m "feat: merge filtro por estado"

# Rebase (reaplica commits da branch em cima do main — histórico linear)
git rebase main
```

---

## 10. GitHub: repositório remoto

### Criar conta e repositório

1. Acesse https://github.com e crie sua conta
2. Clique em **+** → **New repository**
3. Nome: `voos-brasil` · Público · sem README (se já tem código local)
4. Clique em **Create repository**

### Autenticação

O GitHub não aceita mais senha simples. Use um **Personal Access Token**:

1. github.com → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. **Generate new token** → marque `repo` → copie o token gerado
3. Use o token no lugar da senha quando pedido

Ou configure SSH (mais seguro e confortável):

```bash
# Gerar chave SSH
ssh-keygen -t ed25519 -C "seu@email.com"

# Copiar a chave pública
cat ~/.ssh/id_ed25519.pub

# Cole no GitHub: Settings > SSH and GPG keys > New SSH key

# Testar conexão
ssh -T git@github.com
# Hi seu-usuario! You've successfully authenticated.
```

### Conectar repositório local ao GitHub

```bash
# Adicionar o remoto (origin é o nome convencional)
git remote add origin https://github.com/seu-usuario/voos-brasil.git

# Verificar remotos configurados
git remote -v

# Enviar o código pela primeira vez
git push -u origin main
# O flag -u define 'origin main' como padrão para pushes futuros
```

---

## 11. Clonando um repositório

```bash
# Clonar pelo HTTPS
git clone https://github.com/seu-usuario/voos-brasil.git

# Clonar pelo SSH
git clone git@github.com:seu-usuario/voos-brasil.git

# Clonar em uma pasta com nome diferente
git clone https://github.com/seu-usuario/voos-brasil.git meu-painel

# Entrar na pasta
cd voos-brasil
```

---

## 12. Push e Pull

### Push — enviar commits locais para o GitHub

```bash
# Enviar branch atual
git push

# Enviar uma branch específica
git push origin feat/filtro-estado

# Forçar push (reescreve histórico remoto — use com muito cuidado)
git push --force-with-lease
```

### Pull — baixar e integrar mudanças do GitHub

```bash
# Pull = fetch + merge
git pull

# Pull com rebase (histórico mais limpo)
git pull --rebase

# Só baixar, sem integrar
git fetch origin

# Ver o que foi baixado antes de integrar
git log HEAD..origin/main --oneline
```

### Manter-se atualizado em equipe

```bash
# Fluxo diário recomendado
git pull                    # baixar o que há de novo
# (faça seu trabalho)
git add .
git commit -m "feat: ..."
git push                    # enviar seu trabalho
```

---

## 13. Fork e Pull Request

O fluxo de Fork + PR é o padrão para contribuir em projetos open source.

### Fork

1. Acesse o repositório original no GitHub
2. Clique em **Fork** → **Create fork**
3. Você terá uma cópia em `github.com/seu-usuario/repositorio`

```bash
# Clone o SEU fork
git clone https://github.com/seu-usuario/voos-brasil.git
cd voos-brasil

# Adicione o repositório original como remote 'upstream'
git remote add upstream https://github.com/autor-original/voos-brasil.git

# Verificar
git remote -v
# origin    https://github.com/seu-usuario/voos-brasil.git
# upstream  https://github.com/autor-original/voos-brasil.git
```

### Criar uma contribuição

```bash
# Criar branch para a feature
git switch -c feat/adiciona-aeroportos-nordeste

# (faça as alterações)
git add .
git commit -m "feat: adiciona aeroportos do Nordeste ao airports.json"

# Enviar para SEU fork
git push origin feat/adiciona-aeroportos-nordeste
```

### Abrir o Pull Request

1. Vá ao seu fork no GitHub
2. Clique no banner **"Compare & pull request"**
3. Escreva título e descrição claros
4. Clique em **Create pull request**
5. Aguarde revisão e aprovação do mantenedor

### Manter fork atualizado

```bash
# Baixar atualizações do original
git fetch upstream

# Integrar no main local
git switch main
git merge upstream/main

# Sincronizar seu fork no GitHub
git push origin main
```

---

## 14. Resolvendo conflitos

Conflitos acontecem quando duas pessoas editam o mesmo trecho do mesmo arquivo.

```bash
git pull
# Auto-merging index.html
# CONFLICT (content): Merge conflict in index.html
# Automatic merge failed; fix conflicts and then commit the result.
```

O Git marca o conflito no arquivo:

```
<<<<<<< HEAD (seu código)
    <title>Painel de Voos Brasil</title>
=======
    <title>Voos em Tempo Real</title>
>>>>>>> origin/main (código do remoto)
```

**Para resolver:**

1. Abra o arquivo e escolha qual versão manter (ou combine as duas)
2. Remova os marcadores `<<<<<<<`, `=======` e `>>>>>>>`
3. Salve o arquivo
4. Adicione ao staging e finalize o commit:

```bash
git add index.html
git commit -m "fix: resolve conflito no título da página"
```

**Ferramentas visuais de merge:**

```bash
# Usar VS Code como merge tool
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# Abrir ferramenta visual
git mergetool
```

---

## 15. O arquivo .gitignore

O `.gitignore` lista arquivos e pastas que o Git deve ignorar.

```bash
# Criar o arquivo
touch .gitignore
```

Conteúdo do `.gitignore` para o projeto voos-brasil:

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/
.venv/
venv/
env/

# Variáveis de ambiente (NUNCA commitar senhas!)
.env
.env.local
*.env

# Sistemas operacionais
.DS_Store         # macOS
Thumbs.db         # Windows
desktop.ini       # Windows

# Editores
.vscode/settings.json
.idea/
*.swp
*.swo

# Logs
*.log
logs/
```

### Verificar o que está sendo ignorado

```bash
# Ver arquivos ignorados
git status --ignored

# Verificar por que um arquivo específico está sendo ignorado
git check-ignore -v nome-do-arquivo
```

> **Importante:** Se você commitou um arquivo por engano e depois o adicionou ao `.gitignore`, ele ainda aparecerá rastreado. Para remover:
> ```bash
> git rm --cached nome-do-arquivo
> git commit -m "chore: remove arquivo sensível do rastreamento"
> ```

---

## 16. Fluxo completo: publicando o voos-brasil

### Passo 1 — Configurar o Git (só na primeira vez)

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

### Passo 2 — Criar repositório no GitHub

1. github.com → **New repository** → nome: `voos-brasil`
2. Visibilidade: **Public** (necessário para GitHub Pages gratuito)
3. **Não** marque "Add README" (já temos arquivos locais)
4. **Create repository**

### Passo 3 — Inicializar e enviar o projeto

```bash
cd voos-brasil

git init
git add .
git status           # verifique o que será commitado
git commit -m "feat: versão inicial do painel de voos"

git remote add origin https://github.com/SEU_USUARIO/voos-brasil.git
git push -u origin main
```

### Passo 4 — Configurar GitHub Pages

1. No repositório → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` · Folder: `/ (root)`
4. **Save**

Aguarde ~2 minutos. Acesse: `https://SEU_USUARIO.github.io/voos-brasil/`

### Passo 5 — Adicionar Secrets (credenciais da OpenSky)

1. No repositório → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** → `OPENSKY_USER` → sua senha
3. **New repository secret** → `OPENSKY_PASS` → sua senha

### Passo 6 — Configurar aeroportos monitorados

1. No repositório → **Settings** → **Variables** → **Actions**
2. **New repository variable** → `AIRPORTS` → `SBCA,SBGR,SBSP,SBCT,SBGL,SBBR`

### Passo 7 — Rodar o Action pela primeira vez

1. **Actions** → **Atualizar dados de voos** → **Run workflow**
2. Aguarde ~1 minuto → o `data/SBCA.json` (e os outros) serão criados

### Passo 8 — Workflow de trabalho diário

```bash
# Antes de começar: baixar o que há de novo
git pull

# Criar uma branch para sua feature
git switch -c feat/nova-funcionalidade

# (faça as alterações)
git add .
git status
git commit -m "feat: descreva o que foi feito"

# Publicar a branch
git push origin feat/nova-funcionalidade

# Após revisão/aprovação, merge no main
git switch main
git merge feat/nova-funcionalidade
git push

# Limpar a branch local
git branch -d feat/nova-funcionalidade
```

---

## 17. Referência rápida de comandos

### Configuração
```bash
git config --global user.name "Nome"
git config --global user.email "email"
git config --list
```

### Repositório
```bash
git init                    # inicializar
git clone <url>             # clonar
git status                  # ver estado atual
```

### Ciclo básico
```bash
git add <arquivo>           # preparar arquivo
git add .                   # preparar tudo
git add -p                  # preparar interativamente
git commit -m "mensagem"    # salvar snapshot
git commit -am "mensagem"   # add + commit (só arquivos rastreados)
git commit --amend          # corrigir último commit
```

### Histórico
```bash
git log                     # histórico completo
git log --oneline           # resumido
git log --oneline --graph   # com grafo de branches
git diff                    # diferenças não staged
git diff --staged           # diferenças staged
git show <hash>             # detalhes de um commit
```

### Desfazer
```bash
git restore <arquivo>       # descartar alterações
git restore --staged <arq>  # remover do staging
git revert <hash>           # desfazer commit (seguro)
git reset --soft HEAD~1     # voltar 1 commit (mantém staging)
git reset HEAD~1            # voltar 1 commit (mantém arquivos)
git reset --hard HEAD~1     # voltar 1 commit (descarta tudo)
```

### Branches
```bash
git branch                  # listar branches
git switch -c <nome>        # criar e mudar de branch
git switch <nome>           # mudar de branch
git merge <branch>          # fazer merge
git branch -d <branch>      # deletar branch (segura)
git branch -D <branch>      # deletar branch (força)
```

### Remoto
```bash
git remote add origin <url> # conectar ao remoto
git remote -v               # listar remotos
git push -u origin main     # primeiro push
git push                    # push subsequentes
git pull                    # baixar e integrar
git fetch                   # só baixar (sem integrar)
```

### .gitignore
```bash
git check-ignore -v <arq>   # verificar por que está ignorado
git rm --cached <arq>       # parar de rastrear arquivo
```

---

## Dicas finais

- **Commite cedo, commite sempre.** Commits pequenos e frequentes são melhores que um commit gigante.
- **Nunca commite senhas ou tokens.** Use variáveis de ambiente e `.gitignore`.
- **Use branches.** Trabalhar direto no `main` é arriscado em projetos com mais de uma pessoa.
- **Escreva mensagens de commit que expliquem o "porquê"**, não apenas o "o quê" — o código já mostra o quê.
- **`git status` é seu melhor amigo.** Rode-o com frequência para saber exatamente onde está.

---

*Tutorial criado para o projeto voos-brasil — painel de voos brasileiros via OpenSky Network + GitHub Pages.*
