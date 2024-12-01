from transformers import pipeline

class Model:
    def __init__(self):
        self.model = pipeline(model="Intel/dynamic_tinybert")

    def generate_response(self, prompt, relevant_docs):
        if self.model is None:
            return "Sorry, I am unable to generate a response at the moment."
        
        # Combine the user's query with the relevant documents
        context = "\n".join([doc for doc, _ in relevant_docs])
        
        # Format the input correctly for the question-answering pipeline
        input_data = {
            "question": prompt,
            "context": context
        }
        
        response = self.model(input_data)
        return response['answer']

# Example usage
if __name__ == "__main__":
    model = Model()
    relevant_docs = [("Relevant document 1", 0.1), ("Relevant document 2", 0.2)]
    response = model.generate_response("Hello, how are you?", relevant_docs)
    print(response)