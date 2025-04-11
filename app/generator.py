import os
import requests

def generate_response(query, context_chunks):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    messages = [
        {"role": "system", "content": "Answer the query based on the provided context."},
        {"role": "user", "content": f"Context:\n{''.join(context_chunks)}\n\nQuery: {query}"}
    ]

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": messages
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise error for non-2xx responses
        data = response.json()

        # Defensive: make sure response is as expected
        if 'choices' not in data or not data['choices']:
            print("Unexpected API response:", data)
            return "⚠️ Unexpected response from language model."

        return data['choices'][0]['message']['content']

    except requests.exceptions.RequestException as e:
        print("HTTP request failed:", str(e))
        return "⚠️ Failed to connect to the language model API."

    except ValueError as e:
        print("Invalid JSON in response:", response.text)
        return "⚠️ Invalid response from the API."

    except KeyError as e:
        print("Missing expected field in response:", response.json())
        return "⚠️ Could not find expected data in the response."
