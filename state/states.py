from typing import TypedDict, List, Optional
from datetime import datetime

class ScriptState(TypedDict, total=False):
    idea: str
    characters: List[str]
    genre: str
    dialogues: str
    outline: List[str]
    draft: str
    feedback: str
    research_notes: List[str]
    metadata: dict
    timestamp: Optional[str]