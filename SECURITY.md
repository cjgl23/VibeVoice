# Security Policy

## Supported versions

Security updates target the most recent version on `main`.

## Reporting a vulnerability

Use **Security → Report a vulnerability** if available. If private vulnerability reporting is not enabled, open a public issue **without exploit details or private audio**, asking the maintainer to arrange private communication.

## Running demos safely

The Gradio demos are not authenticated production services. Bind to localhost unless you have added appropriate authentication and network controls. Only load model weights from trusted sources, review models that require `trust_remote_code=True`, and never process private audio on a publicly shared demo.

## Dependency changes

GPU, PyTorch and Transformers upgrades may change inference behavior. Review Dependabot PRs and run a GPU-backed smoke test on a trusted machine before deploying updated models.
