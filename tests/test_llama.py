import os
from dont_scroll import config
from llama_cpp import Llama
from dont_scroll.prompt.prompt_generator import PromptGenerator
from dont_scroll.core.db.search import SearchEngine
from dont_scroll.core.text_message import TextMessage

if __name__ == "__main__":

    text_message = TextMessage()
    test_messages = text_message.get_all_message()
    print(f"{test_messages}")

    llm = Llama(model_path="models/llama-2-7b-arguments.Q4_K_M.gguf", n_ctx=2048)

    prompt_generator = PromptGenerator(test_messages, "Where is the company car?")
    prompt = str(prompt_generator)

    print(f"prompt : {prompt}")

    output = llm(prompt, temperature=0.2)
    print(output)
    print("===== RESULT =====")
    print(output["choices"][0]["text"].strip())
