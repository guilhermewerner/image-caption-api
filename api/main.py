#!/usr/bin/env python3

from flask import Flask, request, jsonify
import requests
import torch
from PIL import Image
from transformers import *
from tqdm import tqdm
import urllib.parse as parse
import os
import base64
from io import BytesIO
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)

# Carregar o modelo, tokenizer e processador de imagem
finetuned_model = VisionEncoderDecoderModel.from_pretrained("Trabalho/vit-swin-base-224-gpt2-image-captioning").to(device)
finetuned_tokenizer = GPT2TokenizerFast.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
finetuned_image_processor = ViTImageProcessor.from_pretrained("Trabalho/vit-swin-base-224-gpt2-image-captioning")

# Função para carregar uma imagem
def load_image(image_path):
    return Image.open(requests.get(image_path, stream=True).raw)

# Função para obter a legenda de uma imagem
def get_caption(model, image_processor, tokenizer, image):
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
        caption = get_caption(finetuned_model, finetuned_image_processor, finetuned_tokenizer, load_image(image_path))
        response = {"caption": caption}
        return jsonify(response)
    else:
        return jsonify({"error": "Missing 'image_url'"}), 400

# Rota da api para obter a caption da imagem
@app.route('/caption-base64', methods=['POST'])
def caption_image_base64():
    data = request.get_json()

    print(data)

    if 'image_base64' in data:
        image_base64 = re.sub('^data:image/.+;base64,', '', data['image_base64'])
        image_data = base64.b64decode(image_base64)
        image_stream = BytesIO(image_data)
        image = Image.open(image_stream)
        caption = get_caption(finetuned_model, finetuned_image_processor, finetuned_tokenizer, image)
        response = {"caption": caption}
        return jsonify(response)
    else:
        return jsonify({"error": "Missing 'image_base64'"}), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5885, debug=True)
