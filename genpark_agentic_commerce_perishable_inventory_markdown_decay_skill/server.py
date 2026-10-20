# -*- coding: utf-8 -*-
"""MCP Server for Perishable Inventory Dynamic Markdown & Yield Optimizer Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import PerishableInventoryMarkdownDecayEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "calculate_dynamic_markdown_price",
        "description": "Compute the revenue-maximizing discount percentage for decaying inventory based on days to expiry, current sell-through velocity, and salvage floor.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "original_retail_price": {
                    "type": "number"
                },
                "cost_basis": {
                    "type": "number"
                },
                "current_stock_units": {
                    "type": "integer"
                },
                "days_until_expiration": {
                    "type": "integer"
                },
                "current_daily_sales_velocity": {
                    "type": "number"
                }
            },
            "required": [
                "original_retail_price",
                "cost_basis",
                "current_stock_units",
                "days_until_expiration",
                "current_daily_sales_velocity"
            ]
        }
    },
    {
        "name": "generate_clearance_flash_campaign",
        "description": "Synthesize a multi-channel inventory clearance campaign (app push, shelf digital tag, discount bundle) to zero out stock before write-off.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sku_id": {
                    "type": "string"
                },
                "recommended_discount_pct": {
                    "type": "number"
                },
                "units_at_risk": {
                    "type": "integer"
                },
                "hours_remaining": {
                    "type": "integer"
                }
            },
            "required": [
                "sku_id",
                "recommended_discount_pct",
                "units_at_risk",
                "hours_remaining"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-perishable-inventory-markdown-decay-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(PerishableInventoryMarkdownDecayEngine, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    print("[TEST] Running internal RPC self-test for genpark-agentic-commerce-perishable-inventory-markdown-decay-skill...")
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-perishable-inventory-markdown-decay-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    print(f"[TEST] SUCCESS: {len(list_res['result']['tools'])} tools verified.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
