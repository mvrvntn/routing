# Agent Instructions

## Package Manager & Toolchain
- Use **uv** (system `python` resolves to a dead WindowsApps stub): `uv venv`, `uv pip install -r requirements.txt`
- Or run ad-hoc: `uv run --with pyyaml --with requests python <script>`
- PowerShell: Use `;` instead of `&&` and verify `$LASTEXITCODE`

## File-Scoped Commands
| Task | Command |
|------|---------|
| Run all tests | `uv run --with pyyaml --with requests python -m unittest discover tests` |
| Run test file | `uv run --with pyyaml --with requests python tests/test_tools.py` |
| Run single test | `uv run --with pyyaml --with requests python -m unittest tests.test_tools.TestToolsSuite.<name>` |
| Build OpenWrt | `uv run --with pyyaml --with requests python tools/openwrt/build_openwrt_lists.py` |
| Build Shadowrocket | `uv run --with pyyaml --with requests python tools/shadowrocket/generate_shadowrocket.py` |
| Update geoblock | `uv run --with pyyaml --with requests python scripts/update_geoblock.py` |

## Commit Attribution
AI commits MUST include:
```
Co-Authored-By: Antigravity <antigravity@google.com>
```

## Key Conventions & Quirks
- **OpSec**: Never commit private server node hostnames or selfsteal domains to `data/` or public files.
- **Safety Gate**: Do NOT proxy `.ru`, `.рф`, `.su` or RU critical infrastructure. Enforced by `scripts/update_geoblock.py`.
- **Source vs Targets**: Edit domains in `data/` and CIDRs in `data-ip/`. Files in `HAPP/`, `INCY/`, `MIHOMO/`, `OPENWRT/`, `RELOCANT/`, and `SHADOWROCKET/` are generated outputs.
- **AdBlock vs Analytics**: Keep analytics in `category-ads-all` so web services do not break; `category-ads` drops strict ads.
- **Push & Gaming Direct**: Keep Apple APNs (5223), Google FCM (5228-5230), and Vivox/matchmaking DIRECT to avoid disconnects.
- **Binary Compilations**: `.srs`, `.mrs`, `geosite.dat`, and `geoip.dat` are compiled in GitHub Actions CI, not locally.
