# 04-05-2026 — OpenSky

Sub-projeto do programa **SN-2026**, focado em consumo da API OpenSky Network
para exibição de voos brasileiros em tempo real.

Organização GitHub: [github.com/SN-2026](https://github.com/SN-2026)  
Repositório: [github.com/SN-2026/04-05-2026-opensky](https://github.com/SN-2026/04-05-2026-opensky)  
Site publicado: [SN-2026.github.io/04-05-2026-opensky](https://SN-2026.github.io/04-05-2026-opensky/)

---

## Arquitetura

```
GitHub Actions (a cada 30 min)
   → scripts/fetch_flights.py
   → busca dados na OpenSky Network API
   → salva em data/{ICAO}.json
   → commit automático no repositório
         ↓
GitHub Pages serve index.html + data/*.json
         ↓
Navegador lê /data/{ICAO}.json (mesmo domínio — sem CORS)
```

## Estrutura

```
├── index.html                        ← Painel de voos (dark theme)
├── data/
│   ├── airports.json                 ← 63 aeroportos brasileiros mapeados
│   └── {ICAO}.json                   ← Gerado automaticamente pelo Actions
├── scripts/
│   └── fetch_flights.py              ← Coleta dados da OpenSky
└── .github/
    └── workflows/
        └── update-flights.yml        ← Cron: a cada 30 min
```

---

## Como configurar

### 1. Pré-requisito: Organização criada
Este repositório deve estar dentro da organização **SN-2026** no GitHub.
Veja o guia de publicação PDF para instruções completas.

### 2. Criar conta na OpenSky Network
Acesse [opensky-network.org](https://opensky-network.org) e registre-se gratuitamente.

### 3. Adicionar Secrets na organização ou no repositório
**Settings → Secrets and variables → Actions → New repository secret**

| Secret         | Valor                    |
|----------------|--------------------------|
| `OPENSKY_USER` | seu usuário da OpenSky   |
| `OPENSKY_PASS` | sua senha da OpenSky     |

### 4. Configurar aeroportos monitorados
**Settings → Variables → Actions → New repository variable**

| Variável   | Valor exemplo                        |
|------------|--------------------------------------|
| `AIRPORTS` | `SBCA,SBGR,SBSP,SBCT,SBGL,SBBR`    |

### 5. Ativar GitHub Pages
**Settings → Pages → Source: Deploy from a branch → main / (root)**

### 6. Rodar o Action manualmente
**Actions → Atualizar dados de voos → Run workflow**

### 7. Acessar o site
```
https://SN-2026.github.io/04-05-2026-opensky/
```

---

## Desenvolvimento local

```bash
pip install requests
python scripts/fetch_flights.py
python -m http.server 8080
# Acesse: http://localhost:8080
```

---

## Programa SN-2026

| Sub-projeto          | Descrição                  | Status  |
|----------------------|----------------------------|---------|
| 04-05-2026-opensky   | Painel de voos OpenSky     | Ativo   |

---

## Licença
MIT
