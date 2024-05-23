from generation import Llama
import torch

import os
os.environ['RANK'] = '0'  # Example rank, adjust accordingly
os.environ['WORLD_SIZE'] = '1'  # Example world size, adjust accordingly
os.environ['MASTER_ADDR'] = 'localhost'  # Example master address
os.environ['MASTER_PORT'] = '12355'  # Example master port

llama = Llama.build(ckpt_dir= "../llama3/Meta-Llama-3-8B-Instruct/", tokenizer_path="../llama3/Meta-Llama-3-8B-Instruct/tokenizer.model", max_seq_len= 512, max_batch_size = 4, model_parallel_size=1)

cpu = torch.device("cpu")
cuda = torch.device("cuda")
model = llama.model.to(cuda)


from typing import List
from tokenizer import Dialog

dialogs: List[Dialog] = [
        [{"role": "user", "content": "what is the recipe of mayonnaise?"}],
        [
            {"role": "user", "content": "I am going to Paris, what should I see?"},
            {
                "role": "assistant",
                "content": """\
Paris, the capital of France, is known for its stunning architecture, art museums, historical landmarks, and romantic atmosphere. Here are some of the top attractions to see in Paris:

1. The Eiffel Tower: The iconic Eiffel Tower is one of the most recognizable landmarks in the world and offers breathtaking views of the city.
2. The Louvre Museum: The Louvre is one of the world's largest and most famous museums, housing an impressive collection of art and artifacts, including the Mona Lisa.
3. Notre-Dame Cathedral: This beautiful cathedral is one of the most famous landmarks in Paris and is known for its Gothic architecture and stunning stained glass windows.

These are just a few of the many attractions that Paris has to offer. With so much to see and do, it's no wonder that Paris is one of the most popular tourist destinations in the world.""",
            },
            {"role": "user", "content": "What is so great about #1?"},
        ],
        [
            {"role": "system", "content": "Always answer with Haiku"},
            {"role": "user", "content": "I am going to Paris, what should I see?"},
        ],
        [
            {
                "role": "system",
                "content": "Always answer with emojis",
            },
            {"role": "user", "content": "How to go from Beijing to NY?"},
        ],
    ]
results = llama.chat_completion(
    dialogs,
    max_gen_len=None,
    temperature=0.6,
    top_p=0.9,
)

for dialog, result in zip(dialogs, results):
    for msg in dialog:
        print(f"{msg['role'].capitalize()}: {msg['content']}\n")
    print(
        f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
    )
    print("\n==================================\n")
