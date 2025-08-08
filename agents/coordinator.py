"""Coordinator agent for orchestrating the multi-agent workflow."""

from __future__ import annotations

from typing import Any

from .sub_agents.browser import BrowserAgent
from .sub_agents.classifier import ClassifierAgent
from .sub_agents.enricher import EnricherAgent
from .sub_agents.scorer import ScorerAgent
from .sub_agents.scraper import ScraperAgent
from .sub_agents.searcher import SearcherAgent


class CoordinatorAgent:
    """High level agent responsible for coordinating sub-agents."""

    def __init__(self) -> None:
        self.scraper = ScraperAgent()
        self.classifier = ClassifierAgent()
        self.searcher = SearcherAgent()
        self.enricher = EnricherAgent()
        self.scorer = ScorerAgent()
        self.browser = BrowserAgent()

    async def start_workflow(self, startup_url: str) -> Any:
        """Execute the full investor discovery workflow.

        The implementation is simplified and primarily demonstrates how the
        various sub-agents are expected to interact.
        """

        scraped = await self.scraper.scrape(startup_url)
        classification = await self.classifier.classify(scraped.get("text", ""))
        provider_results = await self.searcher.parallel_search(classification)
        enriched = await self.enricher.enrich([])
        scored = self.scorer.score(enriched)
        return scored
