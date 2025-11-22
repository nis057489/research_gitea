# Example Computational Workflows

Copy these workflow files into your repository's `.gitea/workflows/` directory to run computational analyses automatically.

## Quick Start

1. In your Gitea repository, create a directory: `.gitea/workflows/`
2. Copy one of the example files below and name it `compute.yml`
3. Push your code — the workflow runs automatically!

## Available Examples

### `python-analysis.yml`
**Best for:** General Python data analysis, machine learning, numerical computing

Includes: NumPy, Pandas, Matplotlib, SciPy, Seaborn, Jupyter

### `r-analysis.yml`
**Best for:** Statistical analysis, ggplot2 visualizations, tidyverse workflows

Includes: ggplot2, dplyr, tidyr, readr

### `julia-computation.yml`
**Best for:** High-performance numerical computing, scientific simulations

Includes: Plots, DataFrames, CSV, Statistics

### `long-computation.yml`
**Best for:** Multi-hour or multi-day computations with checkpoint saving

Includes: Progress tracking, intermediate checkpoints, resilient computation

### `gpu-pytorch.yml`
**Best for:** Deep learning with PyTorch, neural network training, GPU-accelerated computation

Includes: PyTorch with CUDA, GPU verification, model checkpointing

### `gpu-tensorflow.yml`
**Best for:** Deep learning with TensorFlow/Keras, GPU-accelerated training

Includes: TensorFlow with GPU support, GPU detection, model saving

### `analysis.py`
**Sample Python script** that generates plots and CSV results — use this to test your workflow!

### `train.py`
**Sample PyTorch GPU training script** — demonstrates GPU usage, memory monitoring, and model saving

## How to Use

### Method 1: Copy directly from this repo

```bash
# In your research repository
mkdir -p .gitea/workflows
cp /path/to/this/gitea/example-workflows/python-analysis.yml .gitea/workflows/compute.yml
git add .gitea/
git commit -m "Add CI workflow"
git push
```

### Method 2: Create manually

Copy the contents of any example file and paste into your repository at `.gitea/workflows/compute.yml`.

## Customizing Workflows

All examples follow the same structure:

```yaml
name: Your Analysis Name
on: [push]  # Run on every push

jobs:
  compute:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Install dependencies
        run: |
          # Your installation commands
          
      - name: Run analysis
        run: |
          # Your computation commands
          
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: results
          path: |
            # Your output files
```

### Common Customizations

**Run only on specific branches:**
```yaml
on:
  push:
    branches: [main, production]
```

**Run on a schedule (e.g., nightly):**
```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM daily
```

**Add more dependencies:**
```yaml
- name: Install dependencies
  run: |
    apt-get update && apt-get install -y python3-pip
    pip3 install numpy pandas scikit-learn tensorflow
```

**Run multiple scripts:**
```yaml
- name: Run analysis
  run: |
    python3 preprocess.py
    python3 train_model.py
    python3 generate_report.py
```

## Tips

- **Test locally first:** Use `act` (GitHub Actions local runner) or just run your script manually
- **Check the logs:** If a workflow fails, click on it in the Actions tab to see detailed logs
- **Start simple:** Use `python-analysis.yml` + `analysis.py` to verify everything works, then customize
- **Parallel jobs:** If you have multiple independent analyses, create separate jobs to run them simultaneously

## Need Help?

Common issues:
- **Workflow not appearing:** Check file path is `.gitea/workflows/` (not `.github/workflows/`)
- **Dependencies failing:** Add explicit versions: `pip3 install numpy==1.24.0`
- **No artifacts:** Make sure your script actually creates the files you're trying to upload
- **Timeout:** Default timeout is 24h (set in config.yaml), increase if needed

Happy computing! 🚀
