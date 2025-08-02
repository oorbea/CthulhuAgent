from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel, GeminiModelSettings
from pydantic_ai.providers.google_gla import GoogleGLAProvider
import os
from dotenv import load_dotenv

from RouterStructuredOutput import RouterSchema, AGENT_DESCRIPTIONS

load_dotenv()

class AgentBuilder:
    @classmethod
    def __build_agent(cls, name:str, instructions:tuple[str] | str, model:str = 'gemini-2.5-flash-lite', output_type:type=str, model_settings:dict|None = None) -> Agent:
        """
        Creates and returns an Agent instance configured with the specified name, instructions, and model.

        Args:
            name (str): The name to assign to the agent.
            instructions (tuple[str] | str): The instructions or description for the agent's behavior.
            model (str, optional): The model identifier to use for the agent. Defaults to 'gemini-2.5-flash-lite'.
            output_type (type, optional): The expected output type of the agent's responses. Defaults to str.
            model_settings (dict|None, optional): Additional settings for the model. Defaults to None.

        Returns:
            Agent: An instance of Agent initialized with the provided parameters.

        Raises:
            EnvironmentError: If the GEMINI_API_KEY environment variable is not set.
        """
        if not os.getenv('GEMINI_API_KEY'):
            raise EnvironmentError("GEMINI_API_KEY environment variable is not set.")
        _model = GeminiModel(model, provider=GoogleGLAProvider(api_key=os.getenv('GEMINI_API_KEY')))
        settings = GeminiModelSettings(**model_settings) if model_settings else GeminiModelSettings()
        agent = Agent(model=_model, name=name, instructions=instructions, output_type=output_type, model_settings=settings)
        return agent
    
    @classmethod
    def build_router(cls) -> Agent:
        name = 'Router'
        system_prompt = """Decide which agent is more helpful to continue with the process. You have to choose one of following agents and you have to return the name of the agent. Return only the name of the agent without any additional text and characters.
        Agents:
            {agents}""".format(agents='\n'.join([f"-{agent.get('name')}: {agent.get('description')}" for agent in AGENT_DESCRIPTIONS]))
        
        settings = {
            "max_tokens": 200,
            "temperature": 0,
        }
        
        return cls.__build_agent(name, system_prompt, 'gemini-2.5-flash-lite', RouterSchema, model_settings=settings)
    
    @classmethod
    def build_story_teller(cls) -> Agent:
        name = 'StoryTeller'
        system_prompt = 'Eres un agente que narra historias de Cthulhu Dark'

        settings = {
            "temperature": 0.4,
        }
        return cls.__build_agent(name, system_prompt, 'gemini-2.5-flash', model_settings=settings)
    
    @classmethod
    def build_story_guider(cls) -> Agent:
        name = 'StoryGuider'
        system_prompt = 'Eres un agente que guía la historia de Cthulhu Dark, ayudando a los jugadores a tomar decisiones'

        settings = {
            "temperature": 0.4,
        }
        return cls.__build_agent(name, system_prompt, 'gemini-2.5-flash', model_settings=settings)
    
    @classmethod
    def build_character_maker(cls) -> Agent:
        name = 'CharacterMaker'
        system_prompt = 'Eres un agente que ayuda a los jugadores a crear personajes para Cthulhu Dark'

        settings = {
            "temperature": 0.4,
        }
        return cls.__build_agent(name, system_prompt, 'gemini-2.5-flash', model_settings=settings)