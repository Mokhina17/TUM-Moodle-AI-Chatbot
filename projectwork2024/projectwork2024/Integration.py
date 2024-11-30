from transformers import pipeline

class Phi35Instruct:
    def __init__(self):
        self.model = pipeline("text-generation", model="HuggingFaceTB/SmolLM-135M")

    def generate_response(self, prompt, relevant_docs):
        if self.model is None:
            return "Sorry, I am unable to generate a response at the moment."
        
        # Combine the user's query with the relevant documents
        context = "\n".join([doc for doc, _ in relevant_docs])
        full_prompt = f"{prompt}\n\nContext:\n{context}"
        
        response = self.model(full_prompt, max_length=2048,truncation=True)
        return response[0]['generated_text']

# Example usage
if __name__ == "__main__":
    phi_model = Phi35Instruct()
    response = phi_model.generate_response("Hello, how are you?")
    print(response)