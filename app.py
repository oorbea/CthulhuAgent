from pydantic_ai.messages import ModelRequest
from GraphBuilder import GraphBuilder, State, agents
import asyncio
from rich import print
from rich.prompt import Prompt
from rich.panel import Panel

async def main():

    print('[magenta]CthulhuAssistant[/magenta]:', Panel('¿Cómo quieres que te llame?', expand=False, border_style='magenta'))

    user_name = Prompt.ask("[cyan]Tú: [/cyan]")
    print('\n')
    print('[magenta]CthulhuAssistant[/magenta]:', Panel(f'¡Hola {user_name}! Soy tu asistente de Cthulhu Dark. ¿En qué te puedo ayudar?', expand=False, border_style='magenta'))
    print(Panel('En cualquier momento puedes escribir "/exit" para terminar.', expand=False, border_style='magenta'))

    graph_builder = GraphBuilder()
    graph = graph_builder.get_graph()
    state = State([])

    while True:
        user_prompt = Prompt.ask(f"[cyan]{user_name}: [/cyan]")
        if user_prompt.lower().strip() == "/exit":
            print("\n[magenta]CthulhuAssistant[/magenta]:", Panel("¡Hasta pronto! 👋", expand=False, border_style='magenta'))
            break

        user_message = ModelRequest.user_text_prompt(user_prompt)
        state.agent_messages.append(user_message)
        start_node = graph_builder.build_node(agent=agents["Router"])
        start_node_instance = start_node()
        result = await graph.run(start_node=start_node_instance, state=state)
        print("\n[magenta]CthulhuAssistant[/magenta]:", Panel(result.output, expand=False, border_style='magenta'), flush=True)

asyncio.run(main())
