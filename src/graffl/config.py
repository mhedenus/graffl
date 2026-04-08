import json
import os
import logging

logger = logging.getLogger(__name__)


class GrafflConfig:
    def __init__(self):
        # Default fallback value
        self.uri_prefix = "https://www.hedenus.de/graffl/"

    def load_from_json(self, filepath: str):
        """Loads configurations from a JSON file and overrides defaults."""
        if not os.path.exists(filepath):
            logger.debug(f"Config file '{filepath}' not found. Using defaults.")
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if "uri_prefix" in data:
                    self.uri_prefix = data["uri_prefix"]
                    logger.debug(f"Loaded URI prefix from config: {self.uri_prefix}")
            except json.JSONDecodeError:
                logger.debug(f"Error: '{filepath}' is not a valid JSON file.")


CONFIG = GrafflConfig()