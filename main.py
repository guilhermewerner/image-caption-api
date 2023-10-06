#!/usr/bin/env python3

from flask import Flask, request, jsonify
import requests
import torch
from PIL import Image
from transformers import *
from tqdm import tqdm
import urllib.parse as parse
import os

app = Flask(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)

# Carregar o modelo, tokenizer e processador de imagem
finetuned_model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning").to(device)
finetuned_tokenizer = GPT2TokenizerFast.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
finetuned_image_processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

# Função para carregar uma imagem
def load_image(image_path):
    return Image.open(requests.get(image_path, stream=True).raw)

# Função para obter a legenda de uma imagem
def get_caption(model, image_processor, tokenizer, image_path):
    image = load_image(image_path)
    img = image_processor(image, return_tensors="pt").to(device)
    output = model.generate(**img)
    caption = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
    return caption

# Rota da api para obter a caption da imagem
@app.route('/caption', methods=['POST'])
def caption_image():
    data = request.get_json()
    if 'image_url' in data:
        image_url = data['image_url']
        caption = get_caption(finetuned_model, finetuned_image_processor, finetuned_tokenizer, image_url)
        response = {"caption": caption}
        return jsonify(response)
    else:
        return jsonify({"error": "Missing 'image_url'"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5885)
