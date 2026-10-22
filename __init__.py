from .updated_prompt_randomizer import HealingArtyPromptRandomizerV11

NODE_CLASS_MAPPINGS = {
    "HealingArtyPromptRandomizerV11": HealingArtyPromptRandomizerV11
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "HealingArtyPromptRandomizerV11": "HealingArty Prompt Randomizer V11"
}

WEB_DIRECTORY = "./js"
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

from .compact_library import HealingArtyPromptLibrary, register_routes
NODE_CLASS_MAPPINGS["HealingArtyPromptLibrary"] = HealingArtyPromptLibrary
NODE_DISPLAY_NAME_MAPPINGS["HealingArtyPromptLibrary"] = "🎲 HealingArty Prompt Randomizer · Library"
register_routes()
