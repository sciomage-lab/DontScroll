from llama_cpp import Llama
from dont_scroll.prompt.prompt_generator import PromptGenerator

if __name__ == "__main__":

    llm = Llama(model_path="models/tinyllama-1.1b-1t-openorca.Q5_K_M.gguf", n_ctx=1024)

    prompt_generator = PromptGenerator()
    prompt = str(prompt_generator)

    print(f"prompt : {prompt}")

    output = llm(prompt)
    print(output)
    print("===== RESULT =====")
    print(output["choices"][0]["text"].strip())
