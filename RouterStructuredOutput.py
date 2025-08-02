from enum import Enum
from typing import TypedDict
from pydantic import BaseModel

class AgentName(str, Enum):
    StoryTeller = "StoryTeller"
    StoryGuider  = "StoryGuider"
    CharacterMaker = "CharacterMaker"
    RuleExplainer = "RuleExplainer"

class RouterSchema(BaseModel):
    agent: AgentName

class AgentDescription(TypedDict):
    name:str
    description:str

AGENT_DESCRIPTIONS = (AgentDescription(name=AgentName.StoryTeller, description="Agent to create Cthulhu Dark Stories"),
                      AgentDescription(name=AgentName.StoryGuider, description="Agent that helps the game master or the players to continue the story in case they get stuck"),
                      AgentDescription(name=AgentName.CharacterMaker, description="Agent to help players create characters for Cthulhu Dark games"),
                      AgentDescription(name=AgentName.RuleExplainer, description="Agent to explain the rules of Cthulhu Dark to the players"))