import io
from pathlib import Path
from typing import Iterable
import PyPDF2
from pydantic_ai import Agent, Tool
from pydantic_ai.messages import ToolReturn
from pydantic_ai.models.gemini import GeminiModel, GeminiModelSettings
from pydantic_ai.providers.google_gla import GoogleGLAProvider
import os
from dotenv import load_dotenv
import json
from pymegatools import Megatools, MegaError

from RouterStructuredOutput import RouterSchema, AGENT_DESCRIPTIONS

load_dotenv()

with open('system_prompts.json', 'r', encoding='utf-8') as f:
    SYS_PROMPTS:dict[str, str] = json.load(f)

def chunk_text(text: str, chunk_chars: int = 2_000) -> Iterable[str]:
    for start in range(0, len(text), chunk_chars):
        yield text[start:start + chunk_chars]

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
    
    @staticmethod
    def __mega_pdf_loader(mega_url:str, filename:str) -> ToolReturn:
        mega = Megatools()
        pdf_path = Path('documents', filename)
        try:
            if not pdf_path.exists():
                os.makedirs(pdf_path.parent, exist_ok=True)
                mega.download(mega_url, path=pdf_path)
        except MegaError as e:
            return ToolReturn(
                return_value="error",
                content=f"Error downloading Mega.nz: {e}",
                metadata={"mega_url": mega_url, "error": str(e)},
            )

        raw = io.BytesIO(pdf_path.read_bytes())
        reader = PyPDF2.PdfReader(raw)
        pages = [page.extract_text() or "" for page in reader.pages]
        full = "\n\n".join(pages)
        chunks = list(chunk_text(full))
        return ToolReturn(
            return_value=f"loaded {len(chunks)} text chunks",
            content=chunks,
            metadata={"mega_url": mega_url, "pdf_file": filename},
        )
    
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

        tools:list[Tool] = []

        def _get_lo_profundo() -> ToolReturn:
            """
            Retrieves a Cthulhu Dark story called "Lo Profundo" and returns it as a list of text chunks.
            This story is about a group of transport workers that spend 9 months in a space ship, and it is used as an example of a Cthulhu Dark story.

            Returns:
                ToolReturn: An object containing the result of the operation, including the text chunks extracted from the PDF.
            """
            return cls.__mega_pdf_loader("https://mega.nz/file/7FUExIZY#5cP6qIkDcUycD2AHSF9kGYwHXQAwojUgo95Up2hpgE8", 'LoProfundo.pdf')
        
        tools.append(Tool(_get_lo_profundo, name='get_lo_profundo', description='Retrieves a Cthulhu Dark story called "Lo Profundo" and returns it as a list of text chunks.\nThis story is about a group of transport workers that spend 9 months in a space ship, and it is used as an example of a Cthulhu Dark story.', takes_ctx=False))

        def _get_malos_augurios() -> ToolReturn:
            """
            Retrieves a Cthulhu Dark story called "Malos Augurios" and returns it as a list of text chunks.
            This story is an improvised story that takes place in New York from 1920, and it is used as an example of a Cthulhu Dark story.

            Returns:
                ToolReturn: An object containing the result of the operation, including the text chunks extracted from the PDF.
            """
            return cls.__mega_pdf_loader("https://mega.nz/file/6Js1BJxI#mb6hgTkySfrQE4m5-rbDBswvxsrpodCQK0za1XKB058", 'MalosAugurios.pdf')
        
        tools.append(Tool(_get_malos_augurios, name='get_malos_augurios', description='Retrieves a Cthulhu Dark story called "Malos Augurios" and returns it as a list of text chunks.\nThis story is an improvised story that takes place in New York from 1920, and it is used as an example of a Cthulhu Dark story.', takes_ctx=False))

        def _get_phasma() -> ToolReturn:
            """
            Retrieves a Cthulhu Dark story called "Phasma" and returns it as a list of text chunks.
            This story takes place in Italy from 273 bC in the house of a rich family. They are throwing a party when things start to get scary, and it is used as an example of a Cthulhu Dark story.

            Returns:
                ToolReturn: An object containing the result of the operation, including the text chunks extracted from the PDF.
            """
            return cls.__mega_pdf_loader("https://mega.nz/file/eZ9DCB6S#U_gOPtzm_GLdakfPO0EUjO-zgS-D3dbuLVaTn4pQzew", 'Phasma.pdf')
        
        tools.append(Tool(_get_phasma, name='get_phasma', description='Retrieves a Cthulhu Dark story called "Phasma" and returns it as a list of text chunks.\nThis story takes place in Italy from 273 bC in the house of a rich family. They are throwing a party when things start to get scary, and it is used as an example of a Cthulhu Dark story.', takes_ctx=False))

        def _get_demonios_de_antano() -> ToolReturn:
            """
            Retrieves a Cthulhu Dark story called "Demonios de Antaño" and returns it as a list of text chunks.
            This story is about the niece of one of the players, which is in a comma due to strange circumstances that seem to be related with her mother but actually have religious reasons, and it is used as an example of a Cthulhu Dark story.

            Returns:
                ToolReturn: An object containing the result of the operation, including the text chunks extracted from the PDF.
            """
            return cls.__mega_pdf_loader("https://mega.nz/file/GUNyBJ4K#5UXPIaBWH5ZrdkaqdwBevUGZr0d3IQem7YArCFfjpA8", 'DemoniosDeAntano.pdf')
        
        tools.append(Tool(_get_demonios_de_antano, name='get_demonios_de_antano', description='Retrieves a Cthulhu Dark story called "Demonios de Antaño" and returns it as a list of text chunks.\nThis story is about the niece of one of the players, which is in a comma due to strange circumstances that seem to be related with her mother but actually have religious reasons, and it is used as an example of a Cthulhu Dark story.', takes_ctx=False))

        def _get_la_herencia_de_los_horrores() -> ToolReturn:
            """
            Retrieves a Cthulhu Dark story called "La Herencia de los Horrores" and returns it as a list of text chunks.
            This story is about a group of players that are invited to a house in the countryside in order to read the testament of a strange doctor that passed away a few days ago, and it is used as an example of a Cthulhu Dark story.

            Returns:
                ToolReturn: An object containing the result of the operation, including the text chunks extracted from the PDF.
            """
            return cls.__mega_pdf_loader("https://mega.nz/file/TAdhXTSR#oqJdJJhuPG7KmHET7CwFM6ScGtoga675Cqjoqog9hSs", 'LaHerenciaDeLosHorrores.pdf')
        
        tools.append(Tool(_get_la_herencia_de_los_horrores, name='get_la_herencia_de_los_horrores', description='Retrieves a Cthulhu Dark story called "La Herencia de los Horrores" and returns it as a list of text chunks.\nThis story is about a group of players that are invited to a house in the countryside in order to read the testament of a strange doctor that passed away a few days ago, and it is used as an example of a Cthulhu Dark story.', takes_ctx=False))

        def _get_el_eco_de_las_sombras_olvidadas() -> ToolReturn:
            """
            Retrieves a Cthulhu Dark story called "El Eco de las Sombras Olvidadas" and returns it as a list of text chunks.
            This story is about a group of players that are invited to a house in order to attend a lesson about ancient magic, and it is used as an example of a Cthulhu Dark story.

            Returns:
                ToolReturn: An object containing the result of the operation, including the text chunks extracted from the PDF.
            """
            return cls.__mega_pdf_loader("https://mega.nz/file/nZFxzBwA#Kv-qSQEsyjHq8DzRK7TzP5ZQXyFPJ-3RlI6KHEuk5vI", 'ElEcoDeLasSombrasOlvidadas.pdf')
        
        tools.append(Tool(_get_el_eco_de_las_sombras_olvidadas, name='get_el_eco_de_las_sombras_olvidadas', description='Retrieves a Cthulhu Dark story called "El Eco de las Sombras Olvidadas" and returns it as a list of text chunks.\nThis story is about a group of players that are invited to a house in order to attend a lesson about ancient magic, and it is used as an example of a Cthulhu Dark story.', takes_ctx=False))

        return cls.__build_agent(name, system_prompt, 'gemini-2.5-flash', model_settings=settings, tools=tuple(tools))
    
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


        def _get_rules_document() -> ToolReturn:
            """
            Retrieves the Cthulhu Dark rules document from a Mega.nz link, extracts text from the PDF,
            and returns it as a list of text chunks.

            Returns:
                ToolReturn: An object containing the result of the operation, including the text chunks extracted from the PDF.
            """
            
            return cls.__mega_pdf_loader("https://mega.nz/file/3Rli0QQb#F5x0M7nR7SDcHL4M6aP_QENWaXKJ2E-JbakldNwoFrA", 'CthulhuDarkRulesES.pdf')
        
        tool = Tool(_get_rules_document, name='get_rules_document', description='Returns the Cthulhu Dark rules document as a PDF file.', takes_ctx=False)
        return cls.__build_agent(name, system_prompt, 'gemini-2.5-flash', model_settings=settings, tools=[tool])