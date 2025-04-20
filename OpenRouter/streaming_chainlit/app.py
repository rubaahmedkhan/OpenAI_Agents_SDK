import chainlit as cl
import asyncio
import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from openai.types.responses import ResponseTextDeltaEvent


import os

# 🔐 Load API Key from environment
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.5-flash-preview"

client = AsyncOpenAI(
    api_key=os.getenv('OPENROUTER_API_KEY'),
    base_url=BASE_URL
)

set_tracing_disabled(disabled=True)



@cl.on_message
async def on_message(message: cl.Message):
    agent = Agent(
        name="Joker",
        instructions="""You are a funny assistant who ONLY tells jokes.
       If someone asks anything other than a joke, politely reply: 
       'Sorry, I only tell jokes!'""",
        model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    )

    result = Runner.run_streamed(agent, input=message.content)

    response_msg = cl.Message(content="")  # placeholder for streaming
    await response_msg.send()

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            response_msg.content += event.data.delta
            await response_msg.update()
