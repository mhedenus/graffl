import logging
import yaml
from pathlib import Path
from rdflib import URIRef

logger = logging.getLogger(__name__)


def apply_profile(profile_name: str, interpreter) -> None:
    """
    Locates and loads a YAML profile.
    Search order:
    1. Relative to the current .graffl file (interpreter.base_path)
    2. Predefined in the graffl module
    3. Relative to current working directory
    """
    if not profile_name.endswith(".yaml"):
        profile_name += ".yaml"

    module_dir = Path(__file__).parent

    # Check paths in order of priority
    paths_to_check = []

    # 1. Highest priority: Relative to the source file
    if interpreter.base_path:
        paths_to_check.append(interpreter.base_path / profile_name)

    # 2. Predefined profiles
    paths_to_check.append(module_dir / "profiles" / profile_name)

    # 3. Local file (CWD)
    paths_to_check.append(Path(profile_name))

    target_path = None
    for path in paths_to_check:
        if path.exists():
            target_path = path
            logger.debug(f"Found profile at: {target_path}")
            break

    if not target_path:
        logger.warning(f"Profile '{profile_name}' could not be found in any location.")
        return

    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            profile_data = yaml.safe_load(f)

            if not profile_data:
                logger.debug(f"Profile '{profile_name}' is empty.")
                return

            # Apply dictionary (aliases)
            if "dictionary" in profile_data:
                interpreter.dictionary.update(profile_data["dictionary"])

            if "vocabularies" in profile_data:
                for base_uri, terms in profile_data["vocabularies"].items():
                    # Hilfslogik: Setzt automatisch ein '#', falls die Base-URI
                    # nicht bereits mit '/' oder '#' endet (Standard-RDF-Praxis).
                    separator = "" if base_uri.endswith(("/", "#")) else "#"

                    if terms:
                        for term in terms:
                            interpreter.dictionary[term] = f"{base_uri}{separator}{term}"

            # Apply URI properties
            if "uri_properties" in profile_data:
                for uri in profile_data["uri_properties"]:
                    interpreter.uri_properties.add(URIRef(uri))

            # Apply Group Graph settings
            if "group_graphs" in profile_data:
                gg_settings = profile_data["group_graphs"]
                if "group_contains" in gg_settings:
                    interpreter.group_contains = URIRef(gg_settings["group_contains"])
                if "group_type" in gg_settings:
                    interpreter.group_type = URIRef(gg_settings["group_type"])

            logger.debug(f"Successfully applied profile '{profile_name}' to interpreter instance.")

    except Exception as e:
        logger.error(f"Failed to load or apply profile '{target_path}': {e}")