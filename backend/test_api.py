import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def test():
    api_key = os.getenv("OPENROUTER_API_KEY")
    print(f"Key: {api_key[:20]}...")

    models = [
        "google/gemini-2.0-flash-exp:free",
        "meta-llama/llama-3.1-8b-instruct:free",
        "mistralai/mistral-7b-instruct:free",
        "openai/gpt-4o-mini",
    ]

    for model in models:
        print(f"\n--- Testing: {model} ---")
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://mediscan-ai.local",
                    "X-Title": "MediScan AI Pro",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": "Say hello in one sentence"}],
                    "max_tokens": 50,
                },
            )
            print(f"Status: {r.status_code}")
            if r.status_code == 200:
                data = r.json()
                if "choices" in data:
                    print(f"SUCCESS: {data['choices'][0]['message']['content']}")
                    return
            else:
                print(f"Error: {r.text[:200]}")

    print("\nAll models failed.")

asyncio.run(test())
