
from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel


DEFAULT_MODEL = "gpt-4o-mini-2024-07-18"

class GuardrailOutput(BaseModel):
    is_ok: bool
    reasoning: str


def create_guardrail_agent():
    return Agent(
        name="Guardrail check",
        instructions="Actúa como un verificador de contenido. Tu única tarea es analizar el siguiente texto de entrada y determinar si contiene una solicitud de información financiera sobre una empresa. Esto incluye preguntas sobre ingresos, ganancias, balances, cotizaciones de acciones, reportes financieros, márgenes, EBITDA, deudas, activos, pasivos, etc.",
        output_type=GuardrailOutput,
        model=DEFAULT_MODEL,
    )

async def functor_guardrail(ctx, agent, input_data):
    result = await Runner.run(create_guardrail_agent(), input_data, context=ctx.context)
    final_output = result.final_output_as(GuardrailOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_ok,
    )

