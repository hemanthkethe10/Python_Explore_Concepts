import os
from langfuse import Langfuse
import openai
 
# get keys for your project from https://cloud.langfuse.com
os.environ["LANGFUSE_PUBLIC_KEY"] = "<YOUR_LANGFUSE_PUBLIC_KEY>"
os.environ["LANGFUSE_SECRET_KEY"] = "<YOUR_LANGFUSE_SECRET_KEY>"
 
# your openai key
os.environ["OPENAI_API_KEY"] = "<YOUR_OPENAI_API_KEY>"
 
# Your host, defaults to https://cloud.langfuse.com
# For US data region, set to "https://us.cloud.langfuse.com"
os.environ["LANGFUSE_HOST"] = "https://us.cloud.langfuse.com"
 
langfuse = Langfuse()
langfuse.auth_check() 

# Define a prompt
prompt = "Explain the concept of Langfuse in simple terms."

# Define the prompt and messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain the concept of Langfuse in simple terms."}
]

# Start a span
span = langfuse.span(
    name="LLM Interaction",
    input_data={"prompt": prompt},
    metadata={"source": "example_script"}
)

try:
    # Interact with OpenAI's API
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # prompt=prompt,
        messages = messages,
        max_tokens=150
    )
    # output = response.choices[0].text.strip()
    output = response['choices'][0]['message']['content']

    # Log response
    # span.log(
    #     name="LLM Response",
    #     output_data={"response": output}
    # )
    print("LLM Response:", output)

except Exception as e:
    # Log error
    span.log(
        name="LLM Error",
        output_data={"error": str(e)}
    )
    raise e

finally:
    # Close the span
    span.end()