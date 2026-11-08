# Contributing to SDCU

We welcome contributions from engineers, designers, and AI developers worldwide!

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/<your-username>/sdcu.git
   cd sdcu
   ```

2. **Python Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -e packages/core
   ```

3. **Run Tests**:
   ```bash
   PYTHONPATH=packages/core python3 -m unittest discover tests
   ```

4. **Run CLI**:
   ```bash
   ./packages/cli/bin/sdcu.js audit
   ```

## Adding Checkpoints or Rules
* Security & Scale checkpoints are located in `skills/sdcu-sd/references/20-checkpoints.md` and enforced in `packages/core/sdcu_core/sd/linter.py`.
* UI craft passes are defined in `skills/sdcu-u/references/` and audited in `packages/core/sdcu_core/ui/auditor.py`.
* Context graph algorithms live in `packages/core/sdcu_core/graph/engine.py`.

Please submit PRs with corresponding automated unit tests in `tests/`.
