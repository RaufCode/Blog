from dotenv import load_dotenv
from openai import AsyncOpenAI
import os

load_dotenv()

client = AsyncOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"],
)

async def summarize_text(content: str) -> str:
    completion = await client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[
            {"role": "user", "content": f"Summarize this blog post in 2-3 sentences:\n\n{content}"}
        ],
        temperature=0.2,
        top_p=0.7,
        max_tokens=150,
        stream=False,
    )
    if completion.choices[0].message.content is not None:
        return completion.choices[0].message.content
    return ""
