# FastAPI ClickHouse API

API REST moderne et scalable construite avec FastAPI et ClickHouse.

## Architecture

- **FastAPI** : Framework ASGI haute performance
- **ClickHouse** : Base de données analytique distribuée
- **uvicorn** : Serveur ASGI production-ready

### Principes

- Stateless : scalabilité horizontale sans contrainte
- Pool de connexions : connexions réutilisables via dependency injection
- Configuration externalisée : variables d'environnement
- Code minimal : pas de dépendances superflues

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Copier `.env.example` vers `.env` et configurer les paramètres ClickHouse :

```bash
cp .env.example .env
```

Éditer `.env` avec vos paramètres de connexion.

## Lancer l'API

```bash
uvicorn app.main:app --reload
```

L'API sera disponible sur `http://localhost:8000`

Documentation interactive : `http://localhost:8000/docs`

## Routes disponibles

- `GET /health` : Health check basique
- `GET /clickhouse-status` : Vérifie la connexion ClickHouse

## Production

Pour la production, lancer avec plusieurs workers :

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Recommandations scalabilité

- Utiliser un reverse proxy (nginx/traefik)
- Load balancer pour distribuer la charge
- Monitoring (Prometheus + Grafana)
- Rate limiting au niveau du reverse proxy
- Augmenter le nombre de workers selon CPU disponibles
