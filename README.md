# FastAPI ClickHouse API

API REST moderne et scalable construite avec FastAPI et ClickHouse avec **support multithreading complet**.

## ✨ Fonctionnalités

- 🚀 **Multithreading activé** : Gère plusieurs requêtes simultanées
- 🔄 **Pool de connexions** : Un nouveau client ClickHouse par requête
- ⚡ **Thread-safe** : Isolation complète entre les requêtes
- 📊 **Performance optimale** : Support de requêtes concurrentes
- 🛠️ **Production-ready** : Configuration multi-workers

## Architecture

- **FastAPI** : Framework ASGI haute performance
- **ClickHouse** : Base de données analytique distribuée
- **uvicorn** : Serveur ASGI production-ready avec support multithreading
- **clickhouse-connect** : Client thread-safe avec pool de connexions

### Principes

- Stateless : scalabilité horizontale sans contrainte
- Pool de connexions : nouveau client par requête (thread-safe)
- Configuration externalisée : variables d'environnement
- Code minimal : pas de dépendances superflues
- **Multithreading** : Chaque requête utilise son propre client isolé

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

### Mode développement (avec hot-reload)

```bash
python run.py
```

### Mode production (avec multithreading)

```bash
# 4 workers pour gérer les requêtes simultanées
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

L'API sera disponible sur `http://localhost:8000`

Documentation interactive : `http://localhost:8000/docs`

## Routes disponibles

### Routes de base

- `GET /health` : Health check basique
- `GET /clickhouse-status` : Vérifie la connexion ClickHouse

### Routes de test multithreading

- `GET /concurrent/simple-query` : Requête simple pour test
- `GET /concurrent/heavy-query` : Requête lourde pour test de charge
- `GET /concurrent/test-isolation?delay=N` : Test d'isolation (délai en secondes)

## 🧪 Tester le multithreading

### Avec le script de test inclus

```bash
python test_concurrent.py
```

Ce script lance automatiquement plusieurs requêtes en parallèle et affiche les statistiques de performance.

### Avec curl (manuel)

```bash
# Lancer 5 requêtes en parallèle
for i in {1..5}; do
  curl http://localhost:8000/concurrent/test-isolation?delay=2 &
done
wait
```

## Production

Pour la production, lancer avec plusieurs workers :

```bash
# Avec uvicorn (recommandé pour la plupart des cas)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Avec gunicorn (pour plus de contrôle)
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Calcul du nombre de workers optimal

- Formule : `(2 × nombre_de_CPU) + 1`
- Exemple : 4 CPU → 9 workers

### Recommandations scalabilité

- Utiliser un reverse proxy (nginx/traefik)
- Load balancer pour distribuer la charge
- Monitoring (Prometheus + Grafana)
- Rate limiting au niveau du reverse proxy
- Augmenter le nombre de workers selon CPU disponibles
- **Pool de connexions ClickHouse** : Ajuster `pool_mgr_max_size` dans `app/database.py`

## 📚 Documentation détaillée

Voir [MULTITHREADING.md](MULTITHREADING.md) pour plus de détails sur :

- Configuration avancée du pool de connexions
- Tests de charge
- Optimisation des performances
- Déploiement Docker
