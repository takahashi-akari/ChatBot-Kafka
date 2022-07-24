# @title model.py
# @author: Takahashi Akari <akaritakahashioss@gmail.com>
# @date: 2022/07/23
# @version: 1.0.6
# @description: This application is a chatbot that uses Kafka as a message broker.
# @license: MIT License Copyright (c) 2022 Takahashi Akari <akaritakahashioss@gmail.com>

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
nb_sentences = 1

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")

chat_history_ids = None

def chatbot(msg):
    global chat_history_ids
    # TODO: add chat history
    chat_history_ids = None
    # encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode(
        msg + tokenizer.eos_token, return_tensors="pt"
    )
    # append the new user input tokens to the chat history
    bot_input_ids = (
        torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
        if chat_history_ids is not None
        else new_user_input_ids
    )
    # generated a response while limiting the total chat history to 1000 tokens,
    chat_history_ids = model.generate(
        bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id
    )
    # pretty print last ouput tokens from bot
    response = tokenizer.decode(
        chat_history_ids[:, bot_input_ids.shape[-1] :][0], skip_special_tokens=True
    )

    return response