from pydantic_ai import Agent, Tool, BinaryContent
from pydantic_ai.models.gemini import GeminiModel, GeminiModelSettings
from pydantic_ai.providers.google_gla import GoogleGLAProvider
import os
from dotenv import load_dotenv
import json
from pathlib import Path

from RouterStructuredOutput import RouterSchema, AGENT_DESCRIPTIONS

load_dotenv()

with open('system_prompts.json', 'r') as f:
    SYS_PROMPTS:dict[str, str] = json.load(f)


class AgentBuilder:
    @classmethod
    def __build_agent(cls, name:str, instructions:tuple[str] | str, model:str = 'gemini-2.5-flash-lite', output_type:type=str, model_settings:dict|None = None, tools:tuple[Tool] = ()) -> Agent:
        """
        Creates and returns an Agent instance configured with the specified name, instructions, and model.

        Args:
            name (str): The name to assign to the agent.
            instructions (tuple[str] | str): The instructions or description for the agent's behavior.
            model (str, optional): The model identifier to use for the agent. Defaults to 'gemini-2.5-flash-lite'.
            output_type (type, optional): The expected output type of the agent's responses. Defaults to str.
            model_settings (dict|None, optional): Additional settings for the model. Defaults to None.
            tools (tuple[Tool], optional): A tuple of tools that the agent can use. Defaults to an empty tuple.

        Returns:
            Agent: An instance of Agent initialized with the provided parameters.

        Raises:
            EnvironmentError: If the GEMINI_API_KEY environment variable is not set.
        """
        if not os.getenv('GEMINI_API_KEY'):
            raise EnvironmentError("GEMINI_API_KEY environment variable is not set.")
        _model = GeminiModel(model, provider=GoogleGLAProvider(api_key=os.getenv('GEMINI_API_KEY')))
        settings = GeminiModelSettings(**model_settings) if model_settings else GeminiModelSettings()
        agent = Agent(model=_model, name=name, instructions=instructions, output_type=output_type, model_settings=settings, tools=tools)
        return agent
    
    @classmethod
    def build_router(cls) -> Agent:
        name = 'Router'
        system_prompt = SYS_PROMPTS.get(name).format(agents='\n'.join([f"-{agent.get('name')}: {agent.get('description')}" for agent in AGENT_DESCRIPTIONS]))
        
        settings = {
            "max_tokens": 200,
            "temperature": 0,
        }
        
        return cls.__build_agent(name, system_prompt, 'gemini-2.5-flash-lite', RouterSchema, model_settings=settings)
    
    @classmethod
    def build_story_teller(cls) -> Agent:
        name = 'StoryTeller'
        system_prompt = SYS_PROMPTS.get(name)

        settings = {
            "temperature": 0.6,
        }
        return cls.__build_agent(name, system_prompt, 'gemini-2.5-flash', model_settings=settings)
    
    @classmethod
    def build_story_guider(cls) -> Agent:
        name = 'StoryGuider'
        system_prompt = SYS_PROMPTS.get(name)

        settings = {
            "temperature": 0.7,
        }
        return cls.__build_agent(name, system_prompt, 'gemini-2.5-flash', model_settings=settings)
    
    @classmethod
    def build_character_maker(cls) -> Agent:
        name = 'CharacterMaker'
        system_prompt = SYS_PROMPTS.get(name)

        settings = {
            "temperature": 0.75,
        }
        return cls.__build_agent(name, system_prompt, 'gemini-2.5-flash', model_settings=settings)
    
    @classmethod
    def build_rule_explainer(cls) -> Agent:
        name = 'RuleExplainer'
        system_prompt = SYS_PROMPTS.get(name)

        settings = {
            "temperature": 0.2,
        }


        def _get_rules_document() -> BinaryContent:
            """
            Returns the Cthulhu Dark rules document as a PDF file.

            Returns:
                BinaryContent: A BinaryContent object containing the PDF data and media type.
            """
            rules_path = Path('documents', 'CthulhuDarkRulesES.pdf')
            return BinaryContent(data=rules_path.read_bytes(), media_type='application/pdf')
        
        tool = Tool(_get_rules_document, name='get_rules_document', description='Returns the Cthulhu Dark rules document as a PDF file.', takes_ctx=False)
        return cls.__build_agent(name, system_prompt, 'gemini-2.5-flash', model_settings=settings, tools=[tool])