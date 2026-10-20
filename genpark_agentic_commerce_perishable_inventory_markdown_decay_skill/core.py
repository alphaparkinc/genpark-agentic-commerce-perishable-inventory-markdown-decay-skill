# -*- coding: utf-8 -*-
"""Perishable Inventory Dynamic Markdown & Yield Optimizer for GenPark Agentic Commerce."""
import json
import math
from typing import Dict, Any

class PerishableInventoryMarkdownDecayEngine:
    """Dynamic perishable inventory yield and decay markdown pricing optimizer."""

    @staticmethod
    def calculate_dynamic_markdown_price(original_retail_price: float, cost_basis: float, current_stock_units: int, days_until_expiration: int, current_daily_sales_velocity: float) -> Dict[str, Any]:
        """Calculate optimal price markdown to liquidate stock before expiry while preserving margin."""
        expected_natural_sales = current_daily_sales_velocity * max(1, days_until_expiration)
        surplus_units = max(0, current_stock_units - expected_natural_sales)
        
        # Urgency decay factor: exponential pressure as expiry approaches
        if days_until_expiration <= 1:
            urgency = 0.70  # Aggressive dump
        elif days_until_expiration <= 3:
            urgency = 0.45
        elif days_until_expiration <= 7:
            urgency = 0.25
        else:
            urgency = 0.10

        # Scale discount by surplus ratio
        surplus_ratio = min(1.0, surplus_units / max(1, current_stock_units))
        recommended_discount_pct = min(75.0, round((urgency * 0.60 + surplus_ratio * 0.40) * 100.0, 1))

        markdown_price = round(original_retail_price * (1.0 - recommended_discount_pct / 100.0), 2)
        # Salvage floor: at least cover partial cost basis if possible
        floor_price = round(cost_basis * 0.80, 2)
        final_price = max(floor_price, markdown_price)

        salvaged_revenue = round(final_price * current_stock_units, 2)
        write_off_loss_avoided = round((final_price - 0.0) * current_stock_units, 2)

        return {
            "original_price": original_retail_price,
            "recommended_markdown_price": final_price,
            "effective_discount_pct": round(((original_retail_price - final_price) / original_retail_price) * 100.0, 1),
            "surplus_units_at_risk": int(surplus_units),
            "projected_salvage_revenue": salvaged_revenue,
            "write_off_loss_avoided": write_off_loss_avoided,
            "margin_status": "PROFITABLE" if final_price > cost_basis else "CAPITAL_RECOVERY"
        }

    @staticmethod
    def generate_clearance_flash_campaign(sku_id: str, recommended_discount_pct: float, units_at_risk: int, hours_remaining: int) -> Dict[str, Any]:
        """Synthesize digital shelf-tag updates and localized consumer push triggers."""
        return {
            "campaign_id": f"CLEARANCE-{sku_id}-{hours_remaining}H",
            "sku_id": sku_id,
            "headline": f"Flash Rescue Deal: {recommended_discount_pct}% OFF - Next {hours_remaining} Hours Only!",
            "merchandising_actions": [
                f"Transmit digital ESL (Electronic Shelf Label) price update: -{recommended_discount_pct}%.",
                f"Trigger geo-fenced mobile app proximity push to shoppers within 3-mile radius.",
                "Auto-bundle with high-velocity complement products (e.g. dips with chips, milk with cereal).",
                "Flag leftover stock for automated charitable food rescue network pickup at T-2 hours."
            ],
            "units_targeted": units_at_risk,
            "priority": "HIGH_URGENCY" if hours_remaining <= 24 else "STANDARD_PROMOTION"
        }
