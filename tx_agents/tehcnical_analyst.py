
import warnings
warnings.simplefilter("ignore", ResourceWarning)
warnings.simplefilter("ignore", DeprecationWarning)


import asyncio
asyncio.get_event_loop().set_debug(False)

from agents.mcp import MCPServer, MCPServerStdio
from agents import Agent, InputGuardrail, FileSearchTool, Runner
from config import prop
import time

DEFAULT_MODEL : str = prop.models().default_model

PROMPT = """
Eres un agente especializado en recopilación de datos financieros en tiempo real, 
enfocado exclusivamente en obtener el precio actual de activos financieros (acciones, índices, ETFs, criptomonedas, etc.) 
desde Yahoo Finance, usando la herramienta conectada vía MCP (Model Context Protocol).

Objetivo principal:

Recuperar y devolver únicamente el precio actual de un activo financiero especificado por el usuario.

Instrucciones:
Usa la tool MCP conectada a Yahoo Finance para consultar los datos.
Extrae únicamente el valor del precio actual de mercado (por ejemplo, el último precio de cotización).
Responde de forma clara y concisa, con este formato:


Precio actual de [símbolo]: $[valor]
Ejemplo:
    Precio actual de AAPL: $187.45

Si el símbolo no existe o hay un error al recuperar los datos, responde:

    No se pudo obtener el precio de [símbolo] : [error].
Supuestos:

    Los símbolos siguen el formato estándar de Yahoo Finance (ej. AAPL, TSLA, ^GSPC, BTC-USD).
    No necesitas realizar ningún análisis técnico ni interpretación adicional.
"""

LIST_MSG = []

async def chat():
    global LIST_MSG

    async with MCPServerStdio(
            params={
                "command": "uv",
                "args": ["--directory",r"D:\dev\test_mcp\yahoo-finance-mcp","run","server.py"],},
            cache_tools_list=True) as mcp_server:

        technica_analyst = Agent(
            name="Especialista en analisis tecnico",
            handoff_description="Especialista en analisis tecnico",
            instructions=PROMPT,
            model=DEFAULT_MODEL,
            mcp_servers=[mcp_server]
        )
        while (True):
            msg: str = input(">")
            LIST_MSG.append(msg)
            result: str = await Runner.run(technica_analyst, "\n".join(LIST_MSG))
            LIST_MSG.append(result.final_output)
            print (result.final_output)


if __name__ == '__main__':

    import os
    from config import prop as cfg

    os.environ['OPENAI_API_KEY'] = cfg.secrets().api_key
    result = asyncio.run(chat())
    print (result)


