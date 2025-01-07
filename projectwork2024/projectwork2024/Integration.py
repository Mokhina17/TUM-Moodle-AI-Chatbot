from huggingface_hub import InferenceClient
import string

class Model:
    def __init__(self):
        self.client = InferenceClient(api_key="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") 

    def clean_text(self, text):
        # Remove non-printable ASCII characters except for newlines and spaces
        printable = set(string.printable)
        cleaned_text = ''.join([char if char in printable or char == '\n' else ' ' for char in text])
        # Replace multiple spaces with a single space
        cleaned_text = ' '.join(cleaned_text.split())
        return cleaned_text
    
    def generate_response(self, prompt, relevant_docs):
        try:
            # Select and combine all relevant chunks
            top_chunks = [doc for doc, _ in relevant_docs]
            context = " ".join(top_chunks)

            # Clean the context text
            cleaned_context = self.clean_text(context)
            print(f"Cleaned context: {cleaned_context}")

            # Prepare messages for the chat API
            messages = [
                {
                    "role": "system",
                    "content": "You are TUM GPT a helpful assistant that provides answers based on the provided context."
                },
                {
                    "role": "user",
                    "content": f"Context: {cleaned_context}\nQuestion: {prompt}"
                }
            ]

            # Send request to the Llama-3.1 model
            completion = self.client.chat.completions.create(
                model="microsoft/Phi-3.5-mini-instruct",
                messages=messages,
                max_tokens=1024
            )

            # Extract and return the assistant's response
            response = completion.choices[0].message.content.strip()
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"