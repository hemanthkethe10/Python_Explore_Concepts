from ollama import Client

client = Client()

# Request full response at once without streaming
resp = client.generate(
    model="qwen3:4b", 
    prompt="What things can you do? Answer in less than 10 words", 
    stream=False
    )

print(resp["response"])