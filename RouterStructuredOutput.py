from enum import Enum
from typing import TypedDict
from pydantic import BaseModel

class AgentName(str, Enum):
    StoryTeller = "StoryTeller"
    StoryGuider  = "StoryGuider"
    CharacterMaker = "CharacterMaker"

class RouterSchema(BaseModel):
    agent: AgentName

class AgentDescription(TypedDict):
    name:str
    description:str

AGENT_DESCRIPTIONS = (AgentDescription(name=AgentName.StoryTeller, description="Agent to create Cthulhu Dark Stories"),
                      AgentDescription(name=AgentName.StoryGuider, description="Agent that helps the game master and the players to continue the story"),
                      AgentDescription(name=AgentName.CharacterMaker, description="Agent to help players create characters for Cthulhu Dark games"))