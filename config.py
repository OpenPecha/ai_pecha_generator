import os
import anthropic

ANTHROPIC_KEY = os.getenv("ANTHROPIC_KEY")
ANTHROPIC_CLIENT = anthropic.Anthropic(api_key=ANTHROPIC_KEY)


