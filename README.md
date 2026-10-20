# Perishable Inventory Dynamic Markdown & Yield Optimizer Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

Real-time price markdown optimization for shelf-life decaying SKUs (fresh produce, airline tickets, event seats), dynamic reservation price clearance, and margin preservation. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `calculate_dynamic_markdown_price`: Compute the revenue-maximizing discount percentage for decaying inventory based on days to expiry, current sell-through velocity, and salvage floor.
- `generate_clearance_flash_campaign`: Synthesize a multi-channel inventory clearance campaign (app push, shelf digital tag, discount bundle) to zero out stock before write-off.

## 🚀 Installation & Usage
Run directly with pure Python standard library:
```bash
python -m genpark_agentic_commerce_perishable_inventory_markdown_decay_skill.server --test
```
