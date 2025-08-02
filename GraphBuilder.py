from dataclasses import dataclass
from typing import Generator
from pydantic_ai import Agent
from pydantic_graph import End, Graph, BaseNode, GraphRunContext
from pydantic_ai.messages import ModelMessage

from AgentBuilder import AgentBuilder
from RouterStructuredOutput import AgentName, RouterSchema

agents = {
        "Router": AgentBuilder.build_router(),
        "StoryTeller": AgentBuilder.build_story_teller(),
        "StoryGuider": AgentBuilder.build_story_guider(),
        "CharacterMaker": AgentBuilder.build_character_maker()
    }

@dataclass
class State:
    agent_messages: list[ModelMessage]

class GraphBuilder:
    __graph: Graph

    def __init__(self):
        self.__graph = Graph(
            name='CthulhuGraph',
            nodes=tuple(self.__build_nodes())
        )

    @staticmethod
    def __create_subclass(name:str, superclass:type, attrs:dict|None=None) -> type:
        """
        Dynamically creates a subclass called `name` inheriting from `superclass`
        with the attributes and methods given in the dict `attrs`.

        Args:
            name (str): The name of the new subclass.
            superclass (type): The superclass to inherit from.
            attrs (dict, optional): A dictionary of attributes and methods to add to the subclass. Defaults to None.

        Returns:
            type: The newly created subclass.
        """
        if attrs is None:
            attrs = {}
        return type(name, (superclass,), attrs)
    
    def __create_run_router(self):
        graph_builder = self

        async def run(self_node: BaseNode, ctx: GraphRunContext[State]) -> BaseNode | End[str]:
            if not ctx.state.agent_messages:
                return End('No se ha proporcionado ningún mensaje')
            prompt = getattr(ctx.state.agent_messages[0], 'content', None) or str(ctx.state.agent_messages[0])

            result = await self_node.agent.run(prompt, message_history=ctx.state.agent_messages)
            ctx.state.agent_messages += result.new_messages()

            router_response:RouterSchema = result.output
            next_agent_name:AgentName = router_response.agent

            if next_agent_name in agents:
                next_node_cls = graph_builder.build_node(agents[next_agent_name])
                return next_node_cls()
            return End(f'Unknown agent: {next_agent_name}')
        return run

    
    @staticmethod
    def __create_run_agent():
        async def run(self_node: BaseNode, ctx: GraphRunContext[State]) -> End[str]:
            if not ctx.state.agent_messages:
                return End('No se ha proporcionado ningún mensaje')
            prompt = getattr(ctx.state.agent_messages[0], 'content', None) or str(ctx.state.agent_messages[0])
            result = await self_node.agent.run(prompt, message_history=ctx.state.agent_messages)
            ctx.state.agent_messages += result.new_messages()
            return End(result.output)
        return run



    def build_node(self, agent:Agent) -> type[BaseNode]:
        if agent.name == 'Router':
            run = self.__create_run_router()
        else:
            run = self.__create_run_agent()
        
        return self.__create_subclass(f'{agent.name}Node', BaseNode, {'run': run, 'agent': agent})


    def __build_nodes(self) -> Generator[type, None, None]:
        for agent in agents.values():
            yield self.build_node(agent)

    def get_graph(self) -> Graph:
        return self.__graph