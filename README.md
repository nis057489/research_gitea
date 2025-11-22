# Self-Hosted Gitea for Computational Scientists

## Introduction

Reproducibility and consistency in computational research remain persistent challenges across scientific disciplines. While software engineers have long addressed similar issues through continuous integration (CI) systems that automate testing and deployment workflows, these practices have seen limited adoption in computational science. The barriers to adoption include complex configuration requirements, reliance on external cloud platforms that may not accommodate sensitive or large-scale datasets, and systems designed primarily for software development rather than scientific computation.

## Problem Statement

Researchers frequently lack accessible infrastructure to execute their computational experiments consistently and reproducibly. Traditional approaches require manual execution of analysis scripts, leading to variability in software environments, dependency versions, and computational parameters. This variability compromises reproducibility and makes it difficult to track which exact code version produced specific results. Moreover, when collaborating across research groups or attempting to reproduce published findings, the absence of standardized execution environments creates significant obstacles.

The software engineering community has effectively addressed analogous challenges through continuous integration pipelines that automatically execute code in controlled environments upon each change. However, existing CI platforms present several limitations for computational scientists:

1. **Infrastructure constraints**: Cloud-based CI services impose time limits, resource restrictions, and lack access to specialized hardware or institutional data storage
2. **Data sovereignty**: Sensitive research data cannot be transmitted to external services due to privacy, security, or regulatory requirements  
3. **Configuration complexity**: Setting up CI systems requires substantial DevOps expertise that many researchers lack
4. **Cost**: Commercial CI services charge based on compute time, making them prohibitively expensive for long-running computational experiments

## Solution

This repository provides a turnkey self-hosted Gitea instance with integrated continuous integration specifically configured for computational research workflows. The system enables researchers to:

- Version control analysis scripts (Python, R, Julia, MATLAB, etc.) alongside their computational outputs
- Automatically execute experiments in isolated, reproducible environments upon code changes
- Retrieve results (figures, processed data, statistical outputs) through a web interface without manual server access
- Maintain complete control over computing resources and data, operating entirely within institutional infrastructure
- Leverage familiar Git workflows without requiring extensive DevOps or systems administration expertise
- Exactly match results with code by commit ID to aid reproducibility, research and dissemination

The configuration prioritizes ease of deployment and scientific productivity over enterprise-grade security features, making it appropriate for research groups, laboratory servers, and individual workstations within trusted network environments.

## Features

* **5 parallel GPU-accelerated CI runners** — run multiple computational jobs simultaneously with full NVIDIA GPU access
* **GPU support for deep learning** — PyTorch, TensorFlow, JAX, and other GPU frameworks work out of the box
* **GitHub Actions compatible** — use familiar workflow syntax
* **Artifact storage built-in** — download results (plots, data files, logs) directly from the web UI
* **LFS support** — store large datasets in your repos
* **Local execution** — your data never leaves your infrastructure
* **Simple setup** — 3 commands and you're running computations

## Quick Start (3 steps, ~2 minutes)

1. **Start the stack:**
   ```bash
   docker compose up -d
   ```

2. **Create your first user:**
   - Open `http://your-server-ip:3000` in your browser
   - The first user you register becomes the admin (no complicated setup!)

3. **Push your code and watch it run:**
   - Create a new repository in the Gitea web UI
   - Add a `.gitea/workflows/compute.yml` file (see example below)
   - Push your code — CI runs automatically
   - Download results from the "Actions" tab

That's it! You're now running computational workflows.

### 🚀 Ready-to-Use Templates

**Don't want to write YAML?** Copy a complete working example:

```bash
# See example-workflows/ directory for:
# - python-analysis.yml (NumPy, Pandas, Matplotlib, SciPy)
# - r-analysis.yml (ggplot2, dplyr, tidyverse)
# - julia-computation.yml (High-performance numerical computing)
# - long-computation.yml (Multi-hour jobs with checkpoints)
# - gpu-pytorch.yml (GPU-accelerated PyTorch training)
# - gpu-tensorflow.yml (GPU-accelerated TensorFlow training)
# - analysis.py (Sample Python script to test with)
# - train.py (Sample GPU training script)
```

Just copy any `.yml` file to your repository's `.gitea/workflows/compute.yml` and push!

See [example-workflows/README.md](example-workflows/README.md) for detailed instructions.

## Example: Running a Python Analysis in CI

Here's a complete example showing how to run a computational script and download results.

**1. Create `.gitea/workflows/compute.yml` in your repository:**

```yaml
name: Run Analysis
on: [push]

jobs:
  compute:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # Install dependencies
      - name: Setup Python
        run: |
          apt-get update && apt-get install -y python3 python3-pip
          pip3 install numpy pandas matplotlib scipy
      
      # Run your computational script
      - name: Run analysis
        run: python3 analysis.py
      
      # Save results (plots, data, logs)
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: analysis-results
          path: |
            *.png
            *.csv
            results/
            *.log
```

**2. Create your analysis script `analysis.py`:**

```python
import numpy as np
import matplotlib.pyplot as plt

# Your computational work
data = np.random.randn(1000)
mean = np.mean(data)

# Generate output
plt.hist(data, bins=50)
plt.savefig('histogram.png')
print(f"Mean: {mean}")

# Save results
np.savetxt('results.csv', data)
```

**3. Push and watch it run:**

```bash
git add .
git commit -m "Run analysis"
git push
```

**4. Download your results:**
- Go to your repository in Gitea
- Click "Actions" tab
- Click on the workflow run
- Download the "analysis-results" artifact zip file

### Other languages:

**R:**
```yaml
- name: Run R script
  run: |
    apt-get update && apt-get install -y r-base
    Rscript analysis.R
```

**Julia:**
```yaml
- name: Run Julia script
  run: |
    wget https://julialang-s3.julialang.org/bin/linux/x64/1.10/julia-1.10.0-linux-x86_64.tar.gz
    tar xzf julia-1.10.0-linux-x86_64.tar.gz
    ./julia-1.10.0/bin/julia analysis.jl
```

**MATLAB (if you have a license server):**
```yaml
- name: Run MATLAB script
  run: |
    # Mount your MATLAB installation or use MATLAB Runtime
    matlab -batch "run('analysis.m')"
```

## GPU-Accelerated Computing

All 5 runners have **full NVIDIA GPU access** for deep learning and computational workloads. The GPUs are automatically available to job containers.

### Prerequisites

**On your host system (one-time setup):**

1. **Install NVIDIA drivers:**
   ```bash
   # Check if drivers are installed
   nvidia-smi
   ```

2. **Install NVIDIA Container Toolkit:**
   ```bash
   # Ubuntu/Debian
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
   sudo systemctl restart docker
   ```

3. **Verify GPU access:**
   ```bash
   docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi
   ```

### Example: PyTorch with GPU

```yaml
name: GPU Training
on: [push]

jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install PyTorch with CUDA
        run: |
          apt-get update && apt-get install -y python3-pip
          pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu118
      
      - name: Verify GPU
        run: |
          python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"
      
      - name: Run training
        run: python3 train.py
      
      - uses: actions/upload-artifact@v3
        with:
          name: model
          path: "*.pth"
```

### Example: TensorFlow with GPU

```yaml
- name: Install TensorFlow with GPU
  run: |
    pip3 install tensorflow[and-cuda]
    python3 -c "import tensorflow as tf; print('GPUs:', tf.config.list_physical_devices('GPU'))"
```

### GPU Workflow Tips

- **Check GPU availability** in your workflow to catch configuration issues early
- **Monitor GPU memory** if training large models (use `nvidia-smi` or framework-specific tools)
- **Each runner has access to all GPUs** — for multiple parallel jobs, they'll share GPU resources
- **Use CUDA base images** for faster setup: `docker://nvidia/cuda:12.0.0-devel-ubuntu22.04`

See `example-workflows/gpu-pytorch.yml` and `example-workflows/train.py` for complete working examples.

## Tips for Computational Scientists

### Working with Large Datasets

**Use Git LFS for large files:**
```bash
# Install git-lfs locally
git lfs install

# Track large data files
git lfs track "*.h5"
git lfs track "*.nc"
git lfs track "data/*.csv"

# Add and commit
git add .gitattributes
git commit -m "Track large files with LFS"
```

### Parallel Jobs

You have 5 runners, so 5 jobs can run simultaneously. Structure your work to take advantage:

```yaml
jobs:
  simulation-1:
    runs-on: ubuntu-latest
    steps:
      - run: python3 sim_part1.py
      
  simulation-2:
    runs-on: ubuntu-latest
    steps:
      - run: python3 sim_part2.py
      
  # ... up to 5 parallel jobs
```

### Viewing Results Without Downloading

Generate HTML reports that you can view in the browser:

```yaml
- name: Generate HTML report
  run: |
    pip3 install jupyter pandas matplotlib
    jupyter nbconvert --to html analysis.ipynb

- name: Upload report
  uses: actions/upload-artifact@v3
  with:
    name: html-report
    path: "*.html"
```

### Keeping Runners Clean

Docker containers are isolated, but artifacts accumulate. Periodically clean up:

```bash
# Prune old Docker images
docker image prune -a -f

# Clean old workflow run data (optional)
docker compose exec gitea find /var/lib/gitea/actions_artifacts -mtime +30 -type f -delete
```

## Common Commands

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
  - **`act_runner-*`**: Five Gitea Actions runner containers with GPU access. They register with the Gitea instance using `GITEA_RUNNER_REGISTRATION_TOKEN` and mount the Docker socket for launching job containers. Each runner has access to all NVIDIA GPUs via the `deploy.resources.reservations.devices` configuration.

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

## Troubleshooting

**My workflow isn't running**
- Check that runners are up: `docker compose ps` (should show 5 act_runner containers)
- Look at runner logs: `docker compose logs act_runner-1`
- Make sure your workflow file is in `.gitea/workflows/` (not `.github/workflows/`)

**Where are my results?**
- Go to your repository → "Actions" tab → Click on the workflow run
- Scroll down to "Artifacts" section
- Click the artifact name to download a zip file with your results

**Jobs are queued but not running**
- Restart runners: `docker compose restart act_runner-1 act_runner-2 act_runner-3 act_runner-4 act_runner-5`
- Check if you need more runners (increase if you're running >5 jobs simultaneously)

**I need more compute power**
- Edit `docker-compose.yml` to add more runners (copy an existing `act_runner-*` block)
- Or increase runner capacity in `config.yaml` (change `capacity: 1` to `capacity: 2`)

**Job failed with "permission denied"**
- Add `chmod +x your-script.sh` before running shell scripts
- Or run with explicit interpreter: `bash script.sh` or `python3 script.py`

**GPU not detected in workflow**
- Verify host has NVIDIA drivers: `nvidia-smi` on host
- Check NVIDIA Container Toolkit is installed (see GPU section above)
- Restart Docker after installing toolkit: `sudo systemctl restart docker`
- Restart runners: `docker compose restart`
- Verify GPU access: `docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi`

**Out of GPU memory**
- Monitor GPU usage: `watch -n 1 nvidia-smi`
- Reduce batch size in your training script
- Limit concurrent GPU jobs by reducing number of runners
- Clear GPU memory between runs: `docker system prune -f`

## Security Note (for lab/internal use)

This setup is optimized for speed and ease of use in trusted environments (lab networks, research groups, personal servers). It's **not configured for public internet exposure**. 

If you need to harden it later:
- Change the DB password in `docker-compose.yml`
- Rotate the runner token after initial setup
- Add TLS/HTTPS (use Caddy or Nginx as reverse proxy)
- Restrict network access with firewall rules

For most computational research workflows on internal networks, the default config is fine.

## GPU Acceleration

To use NVIDIA GPU's your machine must have the `nvidia-container-toolkit` installed, so do that first. Then, uncomment the blocks in `docker-compose.yml` before starting the stack:

```yaml
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: all
    #           capabilities: [ gpu ]
```

If when starting the stack, you get an error similar to the following, then you probably need to verify that `nvidia-container-toolkit` is properly installed:

```sh
Error response from daemon: could not select device driver "nvidia" with capabilities: [[gpu]]
```
