
# submodule

```bash
git submodule update --init
```

# Build

```bash
cd llama.cpp
make -j8
```

# Get gguf Model

```bash
wget https://huggingface.co/TheBloke/llama-2-13B-chat-limarp-v2-merged-GGUF/resolve/main/llama-2-13b-chat-limarp-v2-merged.Q3_K_S.gguf
```

# Run

prompt save to `prompt.txt`
```bash
./main -m llama-2-13b-chat-limarp-v2-merged.Q3_K_S.gguf -f prompt.txt -c 1024 -t 8
```

