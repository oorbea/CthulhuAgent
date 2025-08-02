from pydantic_ai.messages import ModelRequest
from GraphBuilder import GraphBuilder, State, agents
import asyncio
from rich.prompt import Prompt

async def main():


    user_name = Prompt.ask("[magenta]CthulhuAssistant[/magenta]: ¿Cómo quieres que te llame?\n\n[cyan]Tú: [/cyan]")
    print(f'CthulhuAssistant: ¡Hola {user_name}! Soy tu asistente de Cthulhu Dark. ¿En qué te puedo ayudar?\nEn cualquier momento puedes escribir "/exit" para terminar.')
    graph_builder = GraphBuilder()
    graph = graph_builder.get_graph()
    state = State([])

    while True:
        user_prompt = input(f"\n{user_name}: ")
        if user_prompt.lower().strip() == "/exit":
            print("CthulhuAssistant: ¡Hasta pronto! 👋")
            break

        user_message = ModelRequest.user_text_prompt(user_prompt)
        state.agent_messages.append(user_message)
        start_node = graph_builder.build_node(agent=agents["Router"])
        start_node_instance = start_node()
        result = await graph.run(start_node=start_node_instance, state=state)
        print(f"\nCthulhuAssistant: {result.output}", flush=True)

asyncio.run(main())
