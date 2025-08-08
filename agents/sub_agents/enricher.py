"""Enricher agent that augments investor data using Apollo.io."""

from __future__ import annotations

from typing import Dict, List


class EnricherAgent:
    async def enrich(self, investors: List[Dict]) -> List[Dict]:
        """Enrich investor records with contact information."""

        # Placeholder for Apollo integration
        return investors
