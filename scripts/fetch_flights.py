"""
fetch_flights.py
Busca chegadas e partidas dos últimos 2 dias na OpenSky Network API
para um ou mais aeroportos e salva cada um em data/{ICAO}.json.

Variáveis de ambiente:
  AIRPORTS      → ICAO(s) separados por vírgula, ex: SBCA,SBGR,SBSP
                  Padrão: SBCA
  OPENSKY_USER  → usuário OpenSky (GitHub Secret)
  OPENSKY_PASS  → senha OpenSky (GitHub Secret)
"""

import json
import os
import time
from datetime import datetime, timezone

import requests

# ── Configurações ─────────────────────────────────────────────────────────────

airports_env = os.environ.get("AIRPORTS", "SBCA")
AIRPORTS     = [a.strip().upper() for a in airports_env.split(",") if a.strip()]
API_BASE     = "https://opensky-network.org/api"
USERNAME     = os.environ.get("OPENSKY_USER", "")
PASSWORD     = os.environ.get("OPENSKY_PASS", "")
AUTH         = (USERNAME, PASSWORD) if USERNAME else None

now   = int(time.time())
begin = now - 172800  # 48 horas atrás

AIRPORT_NAMES = {
    "SBRB":"Rio Branco","SBMO":"Maceió","SBMQ":"Macapá","SBEG":"Manaus",
    "SBSV":"Salvador","SBIL":"Ilhéus","SBPS":"Porto Seguro","SBFE":"Feira de Santana",
    "SBFZ":"Fortaleza","SBJU":"Juazeiro do Norte","SBBR":"Brasília","SBVT":"Vitória",
    "SBGO":"Goiânia","SBSL":"São Luís","SBIM":"Imperatriz","SBCY":"Cuiabá",
    "SBCG":"Campo Grande","SBPP":"Ponta Porã","SBCF":"Belo Horizonte / Confins",
    "SBBH":"Belo Horizonte / Pampulha","SBUL":"Uberlândia","SBUR":"Uberaba",
    "SBMK":"Montes Claros","SBIP":"Ipatinga","SBVG":"Varginha","SBGV":"Gov. Valadares",
    "SBBE":"Belém","SBSN":"Santarém","SBMA":"Marabá","SBJP":"João Pessoa",
    "SBCT":"Curitiba","SBFI":"Foz do Iguaçu","SBCA":"Cascavel","SBLO":"Londrina",
    "SBMG":"Maringá","SBRF":"Recife","SBPL":"Petrolina","SBTE":"Teresina",
    "SBGL":"Rio de Janeiro / Galeão","SBRJ":"Rio de Janeiro / Santos Dumont",
    "SBCB":"Cabo Frio","SBSG":"Natal","SBPA":"Porto Alegre","SBCX":"Caxias do Sul",
    "SBPK":"Pelotas","SBUG":"Uruguaiana","SBPV":"Porto Velho","SBJI":"Ji-Paraná",
    "SBBV":"Boa Vista","SBFL":"Florianópolis","SBJV":"Joinville","SBNF":"Navegantes",
    "SBJA":"Jaguaruna","SBGR":"São Paulo / Guarulhos","SBSP":"São Paulo / Congonhas",
    "SBKP":"Campinas / Viracopos","SBRP":"Ribeirão Preto","SBSJ":"São José dos Campos",
    "SBDN":"Presidente Prudente","SBAQ":"Araraquara","SBML":"Marília","SBAU":"Araçatuba",
    "SBSE":"Aracaju","SBPJ":"Palmas",
}

AIRLINES = {
    "GLO":"GOL","TAM":"LATAM","AZU":"Azul","ONE":"VOEPASS",
    "PTB":"Passaredo","ABL":"Azul Cargo","TLA":"Total Linhas Aéreas",
}


def get_airline(callsign):
    if not callsign:
        return "—"
    cs = callsign.strip().upper()
    for prefix, name in AIRLINES.items():
        if cs.startswith(prefix):
            return name
    return cs[:3]


def unix_to_iso(ts):
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def process_flights(flights, kind):
    result = []
    for f in flights:
        if not isinstance(f, dict):
            continue
        callsign = (f.get("callsign") or "").strip()
        if not callsign:
            continue
        airport_key = (
            f.get("estDepartureAirport") if kind == "arrival"
            else f.get("estArrivalAirport")
        ) or ""
        time_key = f.get("lastSeen") if kind == "arrival" else f.get("firstSeen")
        result.append({
            "callsign":     callsign,
            "airline":      get_airline(callsign),
            "icao24":       f.get("icao24", ""),
            "airport":      airport_key,
            "airport_name": AIRPORT_NAMES.get(airport_key, airport_key or "—"),
            "time_unix":    time_key,
            "time_iso":     unix_to_iso(time_key),
        })
    result.sort(key=lambda x: x["time_unix"] or 0)
    return result


def fetch(endpoint, airport):
    url    = f"{API_BASE}/flights/{endpoint}"
    params = {"airport": airport, "begin": begin, "end": now}
    try:
        r = requests.get(url, params=params, auth=AUTH, timeout=30)
        r.raise_for_status()
        data = r.json()
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"  [AVISO] {endpoint} para {airport}: {e}")
        return []


# ── Execução ──────────────────────────────────────────────────────────────────

os.makedirs("data", exist_ok=True)

for icao in AIRPORTS:
    name = AIRPORT_NAMES.get(icao, icao)
    print(f"\nBuscando {icao} - {name}...")

    arrivals   = process_flights(fetch("arrival",   icao), "arrival")
    departures = process_flights(fetch("departure", icao), "departure")

    output = {
        "updated_at":   datetime.now(timezone.utc).isoformat(),
        "airport_icao": icao,
        "airport_name": name,
        "window_hours": 48,
        "arrivals":     arrivals,
        "departures":   departures,
    }

    with open(f"data/{icao}.json", "w", encoding="utf-8") as fh:
        json.dump(output, fh, ensure_ascii=False, indent=2)

    print(f"  OK: {len(arrivals)} chegadas, {len(departures)} partidas.")

print("\nConcluido.")
