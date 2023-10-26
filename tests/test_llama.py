# Copyright (c) 2023 SciomageLAB
#
# This file is part of a project licensed under the Sciomage LAB Public License.
# 
# You are free to copy, modify, and distribute this file for commercial and non-commercial purposes,
# provided that you adhere to the license terms and conditions.
# 
# For more information, see the Sciomage LAB Public License which should accompany this project.


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

    llm = Llama(model_path="models/tinyllama-1.1b-1t-openorca.Q5_K_M.gguf", n_ctx=2048)

    prompt_generator = PromptGenerator(test_messages, "Where is the company car?")
    prompt = str(prompt_generator)

    print(f"prompt : {prompt}")

    output = llm(prompt, temperature=0.2)
    print(output)
    print("===== RESULT =====")
    print(output["choices"][0]["text"].strip())
