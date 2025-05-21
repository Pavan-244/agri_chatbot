import openai

openai.api_key = ""

def ask_chatgpt(prompt):
    """Send a prompt to ChatGPT and return the reply."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-0.28.0",  # Or use gpt-4 if available
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

# Example
if __name__ == "__main__":
    print(ask_chatgpt("What is the price of rice in Telangana?"))
