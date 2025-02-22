# Copyright (c) 2023 SciomageLAB
#
# This file is part of a project licensed under the Sciomage LAB Public License.
# 
# You are free to copy, modify, and distribute this file for commercial and non-commercial purposes,
# provided that you adhere to the license terms and conditions.
# 
# For more information, see the Sciomage LAB Public License which should accompany this project.


import os
from dont_scroll.core.text_message import TextMessage


class PromptGenerator:
    def __init__(self, message: str = None, question=None, template=None):
        # TODO: Options
        self.prompt_root = os.path.dirname(os.path.abspath(__file__))

        if not os.path.exists(f"{self.prompt_root}/system.txt"):
            print(f"not exists {self.prompt_root}/system.txt")
        if not os.path.exists(f"{self.prompt_root}/user-pre.txt"):
            print(f"not exists {self.prompt_root}/user-pre.txt")
        if not os.path.exists(f"{self.prompt_root}/user-post.txt"):
            print(f"not exists {self.prompt_root}/user-post.txt")
        if not os.path.exists(f"{self.prompt_root}/chat.txt"):
            print(f"not exists {self.prompt_root}/chat.txt")

        self.message = message
        self.question = question
        self.template = template

    def __str__(self):
        # TODO: condition

        # Default
        if self.template is None:
            return self.gen_chat_ml()
        if self.template == "llama2-chat":
            return self.gen_llama2_chat()
        elif self.template == "chat-ml":
            return self.gen_chat_ml()
        if self.template == "llama32":
            return self.gen_llama32()
        if self.template == "llama32_ko":
            return self.gen_llama32ko()
        else:
            return self.gen_chat_ml()

    def gen_chat_ml(self):
        ret = ""

        # System
        ret += "<|im_start|>system\n"
        ret += self.read_txt_file(f"{self.prompt_root}/system.txt")
        ret += "<|im_end|>\n"

        # User
        ret += "<|im_start|>user\n"
        ret += self.read_txt_file(f"{self.prompt_root}/user-pre.txt")
        ret += "\n"

        # Chat
        ret += "```text\n"
        if self.message is None:
            ret += self.read_txt_file(f"{self.prompt_root}/chat.txt")
        else:
            ret += self.message
        ret += "```"
        ret += "\n"

        # Question
        if self.question is None:
            ret += self.read_txt_file(f"{self.prompt_root}/user-post.txt")
        else:
            ret += self.question
        ret += "<|im_end|>\n"
        ret += "<|im_start|>assistant"

        return ret

    def gen_llama2_chat(self):
        ret = ""

        # System
        ret += "[INST] <<SYS>>\n"
        ret += self.read_txt_file(f"{self.prompt_root}/system.txt")
        ret += "\n<</SYS>>\n"

        # User
        ret += self.read_txt_file(f"{self.prompt_root}/user-pre.txt")
        ret += "\n"

        # Chat
        ret += "```text\n"
        if self.message is None:
            ret += self.read_txt_file(f"{self.prompt_root}/chat.txt")
        else:
            ret += self.message
        ret += "```"
        ret += "\n"

        # Question
        if self.question is None:
            ret += self.read_txt_file(f"{self.prompt_root}/user-post.txt")
        else:
            ret += self.question
        ret += "[/INST]"

        return ret

    def gen_llama32(self):
        ret = ""

        # System
        ret += "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
        ret += "Cutting Knowledge Date: December 2023\n"
        ret += "Today Date: 9 Oct 2024\n\n"
        ret += self.read_txt_file(f"{self.prompt_root}/system.txt")
        ret += "\n<|eot_id|><|start_header_id|>user<|end_header_id|>\n"

        # User
        ret += self.read_txt_file(f"{self.prompt_root}/user-pre.txt")
        ret += "\n"

        # Chat
        ret += "```text\n"
        if self.message is None:
            ret += self.read_txt_file(f"{self.prompt_root}/chat.txt")
        else:
            ret += self.message
        ret += "```"
        ret += "\n"

        # Question
        if self.question is None:
            ret += self.read_txt_file(f"{self.prompt_root}/user-post.txt")
        else:
            ret += self.question
        ret += "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"

        return ret

    def gen_llama32ko(self):
        ret = ""

        # System
        ret += "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
        ret += "Cutting Knowledge Date: December 2023\n"
        ret += "Today Date: 9 Oct 2024\n\n"
        ret += self.read_txt_file(f"{self.prompt_root}/system_ko.txt")
        ret += "\n<|eot_id|><|start_header_id|>user<|end_header_id|>\n"

        # User
        ret += self.read_txt_file(f"{self.prompt_root}/user-pre_ko.txt")
        ret += "\n"

        # Chat
        ret += "```text\n"
        if self.message is None:
            ret += self.read_txt_file(f"{self.prompt_root}/chat.txt")
        else:
            ret += self.message
        ret += "```"
        ret += "\n"

        # Question
        if self.question is None:
            ret += "Question : "
            ret += self.read_txt_file(f"{self.prompt_root}/user-post.txt")
        else:
            ret += "질문 : "
            ret += self.question
        ret += "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"

        return ret



    def read_txt_file(self, file_path):
        if not os.path.exists(file_path):
            print(f"not exists {file_path}")
            return None

        text = ""
        with open(file_path, "r") as f:
            for line in f:
                text += line

        return text.rstrip("\n")


if __name__ == "__main__":
    # Text Message
    text_message = TextMessage()
    test_messages = text_message.get_all_message()

    prompt_generator = PromptGenerator(test_messages, "query", template="llama2-chat")

    print(prompt_generator)
