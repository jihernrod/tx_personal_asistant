
import os



from agents import Agent, InputGuardrail, FileSearchTool, Runner
import asyncio
import guardrails

REPSOL = "Repsol S.A"
IBERDROLA = "Iberdrola"

LIST_COMPANY = [REPSOL, IBERDROLA]

ANALYST_PROMPT = """
Eres un asistente experto en análisis fundamental con enfoque exclusivo en la empresa {company}. Tu tarea es analizar e interpretar los datos financieros, operativos y macroeconómicos que afectan el desempeño y el valor intrínseco de Repsol. 

Tienes profundo conocimiento en:
    Estados financieros (balance, cuenta de resultados, flujo de caja).
    Indicadores clave (PER, ROE, EBITDA, margen operativo, deuda neta/EBITDA, etc.).
    Estrategia corporativa y planes de inversión.
    Ciclo del petróleo y gas, precios del Brent, geopolítica energética.
    Información sectorial relevante (energías renovables, regulación, competencia).
    Informes anuales y trimestrales de Repsol, así como presentaciones a inversores.
    Tu objetivo es responder preguntas de manera clara y profesional, justificando cada afirmación con fundamentos cuantitativos y cualitativos. Puedes elaborar análisis DCF (Descuento de Flujos de Caja), análisis comparativos sectoriales y evaluar riesgos específicos (regulatorios, ESG, geopolíticos). Siempre priorizas la objetividad y la transparencia.

Debes basarte en la respuesta siempre en la informacion existente en tu Vector Store usando la Tool
No debes inventarte nada.
En caso de no tener informacion de la Tool debes decir que no sabes nada de esa empresa
"""

DEFAULT_MODEL = "gpt-4o-mini-2024-07-18"

def create_financial_agent(company):
     return Agent(
        name="{company} Especialista".format(company=company),
        handoff_description="Especialista en una {company}".format(company=company),
        instructions=ANALYST_PROMPT.format(company=company),
        model=DEFAULT_MODEL,
        tools=[
             FileSearchTool(
                 max_num_results=3,
                 vector_store_ids=["vs_681f7c5abb048191869141409af2252e"],
             ),
         ]
    )



triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's question",
    handoffs=[create_financial_agent(x) for x in LIST_COMPANY],
    input_guardrails=[
        InputGuardrail(guardrail_function=guardrails.functor_guardrail),
    ],
    model=DEFAULT_MODEL
)



async def chat(msg):
    result = await Runner.run(triage_agent, msg)
    return result.final_output


if __name__ == "__main__":
    asyncio.run(chat("Hazme un resumen del informe financiero de resultados de Repsol"))