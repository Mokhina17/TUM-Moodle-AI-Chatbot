from transformers import pipeline

class Model:
    def __init__(self):
        # deepset/roberta-base-squad2 model for QA tasks
        self.model = pipeline('question-answering', model="deepset/roberta-base-squad2", tokenizer="deepset/roberta-base-squad2")

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

    # Simulate relevant documents (in practice, these would come from your `docstore`)
    relevant_docs = [("The RoBERTa model is a transformer-based model designed for NLP tasks.", 0.1),
                     ("RoBERTa was pre-trained on a large corpus of text and fine-tuned for SQuAD.", 0.2)]

    # Test the model with a sample user query
    user_query = "What is RoBERTa?"
    response = model.generate_response(user_query, relevant_docs)

    print(f"Response: {response}")