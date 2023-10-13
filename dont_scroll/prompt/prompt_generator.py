import os


class PromptGenerator:
    def __init__(self, message: str=None, question=None):
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

    def __str__(self):
        # TODO: condition

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
    prompt_generator = PromptGenerator()

    print(prompt_generator)
