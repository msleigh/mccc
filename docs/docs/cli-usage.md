# CLI Usage

## Command format

Activate the project environment first:

```bash
source .venv/bin/activate
```

```bash
mccc [OPTIONS]
```

Options:

- `-g, --generations INTEGER`: number of generations.
- `-p, --particles INTEGER`: particle count (repeat for convergence mode).
- `--seed INTEGER`: random seed for reproducible sampling.
- `-t, --type TEXT`: plot type (`convergence`, `generations`, `fission_rate`).

## Examples

Default run (no plots):

```bash
mccc -g 6 -p 128000
```

Reproducible default run:

```bash
mccc -g 6 -p 128000 --seed 12345
```

Convergence sweep:

```bash
mccc -t convergence -g 1 -p 1000 -p 2000 -p 4000 -p 8000 -p 16000
```

Generations plot:

```bash
mccc -t generations -g 6 -p 128000
```

Fission-rate plot:

```bash
mccc -t fission_rate -g 12 -p 1024000
```

Multi-generation convergence workflow (as in the project write-up):

```bash
# One generation
mccc -t convergence -g 1 -p 1000 -p 2000 -p 4000 -p 8000 \
    -p 16000 -p 32000 -p 64000 -p 128000 -p 256000 -p 512000 \
    -p 1024000

# Two generations
mccc -t convergence -g 2 -p 1000 -p 2000 -p 4000 -p 8000 \
    -p 16000 -p 32000 -p 64000 -p 128000 -p 256000 -p 512000 \
    -p 1024000

# Three generations
mccc -t convergence -g 3 -p 1000 -p 2000 -p 4000 -p 8000 \
    -p 16000 -p 32000 -p 64000 -p 128000 -p 256000 -p 512000 \
    -p 1024000
```

## Output files

Depending on `--type`, the following files are written in the working
directory:

- `particle_convergence.png`
- `generations.png`
- `fission_rate.png`
