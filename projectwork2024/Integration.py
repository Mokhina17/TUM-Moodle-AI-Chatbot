from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "microsoft/Phi-3.5-mini-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_response(prompt, max_length=150):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=max_length, do_sample=True)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

#this one is to test but later when DocStore is ready
# if __name__ == "__main__":
    user_input = "..."
    response = generate_response(user_input)
    print("Model response:", response)

