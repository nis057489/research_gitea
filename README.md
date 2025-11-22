# Gitea (local) — Quick start

This repository contains my small, self-hosted Gitea setup using Docker Compose, plus an example Gitea Actions runner config. Use this README to quickly start the stack and to understand the three main configuration files included here.

## Features

* 3 preconfigured Actions runners
* LFS storage enabled
* Utilising Docker compose

**Quick Start**

1. Clone the repo
1. Edit any defaults (see Files Explained)
1. `docker compose up -d`
1. Access it on `server-ip-address:3000`

- **Bring up the stack with the current config:**

```bash
docker compose up -d
```

- **Follow logs (Gitea):**

```bash
docker compose logs -f gitea
```

- **Stop and remove containers (and optionally volumes):**

```bash
docker compose down
# include -v to remove named volumes if you want to wipe DB and data
docker compose down -v
```

**Files explained**

- `docker-compose.yml`: Compose configuration that defines four service groups:
  - **`db`**: Runs `postgres:15`. Environment variables set `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD`.
  - **`gitea`**: Runs `gitea/gitea:latest-rootless` and mounts `./gitea` to `/var/lib/gitea` inside the container (this is your persistent Gitea data directory). It exposes ports `3000` (web) and `2222` (SSH) on the host. Important environment overrides are provided via `GITEA__*` variables (these take precedence over values inside `config/app.ini`).
  - **`act_runner-*`**: Multiple Gitea Actions runner containers. They register with the Gitea instance using `GITEA_RUNNER_REGISTRATION_TOKEN` and mount the Docker socket for launching job containers.

  Key notes:
  - The `db` service stores data in `./pgdata` (mapped to Postgres data dir). Back this up if you want to keep repositories and DB state.
  - The `gitea` service stores its app data in `./gitea` (this contains `custom`, `data`, `git`, etc.).
  - The compose file includes an explicit DB password `gitea_password` — change this in `docker-compose.yml` before using in production.

- `config/app.ini` (example contents included in `config/app.ini`):
  - **Purpose:** Gitea configuration file used by the app at runtime. When running inside Docker, environment variables (`GITEA__...`) override values in `app.ini`.
  - **Important sections/values from this repo:**
    - `[server]`: `HTTP_PORT=3000`, `SSH_PORT=2222`, `START_SSH_SERVER=true`, `APP_DATA_PATH=/var/lib/gitea` — these reflect how the container is expected to run.
    - `[database]`: shows `DB_TYPE = postgres` and `HOST = db:5432`. The password in `app.ini` may differ from the Docker Compose environment variable; the Compose env will be used at container runtime.
    - `[security]`: `INSTALL_LOCK` and `SECRET_KEY` — keep `SECRET_KEY` secret and set `INSTALL_LOCK=true` after initial setup to prevent accidental re-initialization.

  Tip: If you prefer to edit settings via the web UI, you can leave `app.ini` alone and configure through Gitea's admin panels. If you edit `app.ini` on the host, restart the container to apply changes.

- `config.yaml` (for `act_runner` / runner configuration):
  - **Purpose:** Config for the Gitea Actions runner (if you run `act_runner` from this repo / container). It contains runner settings such as `capacity`, `envs`, `labels`, and cache options.
  - **Key fields:**
    - `runner.file`: file to store registration result (default: `.runner`).
    - `runner.capacity`: how many concurrent jobs the runner will execute.
    - `container.valid_volumes`, `container.docker_host`, `container.force_pull`: control how job containers are launched.
    - `cache`: enabling `actions/cache` server and related host/port values.

  Warning: The `docker-compose.yml` includes `GITEA_RUNNER_REGISTRATION_TOKEN` environment values for runner services. Treat these tokens as secrets — rotate them if they are exposed.

**Useful commands**

- Start (detached):

```bash
docker compose up -d
```

- Tail all logs:

```bash
docker compose logs -f
```

- Access a shell in the Gitea container:

```bash
docker compose exec gitea /bin/bash
```

**Where data lives on host**

- Gitea app data: `./gitea` (mounted into `/var/lib/gitea` in the container).
- Postgres data: `./pgdata` (mounted into Postgres container's data dir).

**Security & customization checklist**

This configuration is intended for local testing or trusted-network use only. It is NOT hardened for untrusted or public-facing deployments. Before running these services in any environment you don't control, harden the configuration by doing at minimum:

- Change default DB password in `docker-compose.yml` and update `config/app.ini` if you hardcode it there.
- Remove or rotate any published `GITEA_RUNNER_REGISTRATION_TOKEN` values and store secrets in a secure secrets manager.
- Configure TLS (use a reverse proxy with valid certificates or enable HTTPS in front of Gitea) and set `ROOT_URL` to the secure address.
- Harden Postgres access (non-default users/ports, network restrictions, backups) and secure host volumes.
- Secure the runner registration token(s): do not commit usable tokens publicly. If the token in `docker-compose.yml` is a live token, create a new one in your Gitea instance and replace it.
- Set `GITEA__SECURITY__INSTALL_LOCK=true` (or through the UI) after finishing initial setup to prevent re-installation.
- If exposing Gitea to the internet, configure TLS and set `REVERSE_PROXY_TRUSTED_PROXIES` appropriately (or run behind a reverse proxy).
