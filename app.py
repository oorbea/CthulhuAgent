from pydantic_ai.messages import ModelRequest
from GraphBuilder import GraphBuilder, State, agents
import asyncio
from rich import print
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown

async def main():

    print('[bold magenta]CthulhuAssistant[/bold magenta]:', Panel('¿Cómo quieres que te llame?', expand=False, border_style='bold magenta'))

    user_name = Prompt.ask("[bold cyan]Tú: [/bold cyan]")
    print('\n')
    print('[bold magenta]CthulhuAssistant[/bold magenta]:', Panel(f'¡Hola {user_name}! Soy tu asistente de Cthulhu Dark. ¿En qué te puedo ayudar?', expand=False, border_style='bold magenta'))
    print(Panel('En cualquier momento puedes escribir "/exit" para terminar.', expand=False, border_style='bold magenta'))

    graph_builder = GraphBuilder()
    graph = graph_builder.get_graph()
    state = State([])

    while True:
        user_prompt = Prompt.ask(f"[bold cyan]{user_name}: [/bold cyan]")
        if user_prompt.lower().strip() == "/exit":
            print("\n[bold magenta]CthulhuAssistant[/bold magenta]:", Panel("¡Hasta pronto! 👋", expand=False, border_style='bold magenta'))
            break

        user_message = ModelRequest.user_text_prompt(user_prompt)
        state.agent_messages.append(user_message)
        start_node = graph_builder.build_node(agent=agents["Router"])
        start_node_instance = start_node()
        result = await graph.run(start_node=start_node_instance, state=state)
        print("\n[bold magenta]CthulhuAssistant[/bold magenta]:", Panel(Markdown(result.output), expand=False, border_style='bold magenta'), flush=True)

asyncio.run(main())
