import logging
import os
import sqlite3
import json
import base64
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from ontology_dc8f06af066e4a7880a5938933236037.config import ConfigClass
from ontology_dc8f06af066e4a7880a5938933236037.input import InputClass
from ontology_dc8f06af066e4a7880a5938933236037.output import OutputClass
from openfabric_pysdk.context import AppModel, State
from core.stub import Stub
from local_llm import LocalLLM
from memory_manager import MemoryManager
configurations: Dict[str, ConfigClass] = dict()
memory_manager = MemoryManager()
local_llm = LocalLLM()
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)
(OUTPUT_DIR / "images").mkdir(exist_ok=True)
(OUTPUT_DIR / "models").mkdir(exist_ok=True)
def config(configuration: Dict[str, ConfigClass], state: State) -> None:
    for uid, conf in configuration.items():
        logging.info(f"Saving new config for user with id:'{uid}'")
        configurations[uid] = conf
def execute(model: AppModel) -> None:
    request: InputClass = model.request
    user_prompt = request.prompt
    user_config: ConfigClass = configurations.get('super-user', None)
    logging.info(f"User config: {user_config}")
    app_ids = user_config.app_ids if user_config else []
    stub = Stub(app_ids)
    try:
        logging.info("Step 1: Processing user prompt with local LLM...")
        enhanced_prompt = local_llm.enhance_prompt(user_prompt)
        logging.info(f"Enhanced prompt: {enhanced_prompt}")
        logging.info("Step 2: Generating image from text...")
        text_to_image_app_id = "f0997a01-d6d3-a5fe-53d8-561300318557.node3.openfabric.network"
        image_result = stub.call(text_to_image_app_id, {
            'prompt': enhanced_prompt
        }, 'super-user')
        image_data = image_result.get('result')
        if image_data:
            image_filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            image_path = OUTPUT_DIR / "images" / image_filename
            if isinstance(image_data, str):
                image_bytes = base64.b64decode(image_data)
            else:
                image_bytes = image_data
            with open(image_path, 'wb') as f:
                f.write(image_bytes)
            logging.info(f"Image saved to: {image_path}")
        else:
            raise Exception("Failed to generate image")
        logging.info("Step 3: Converting image to 3D model...")
        image_to_3d_app_id = "69543f29-4d41-4afc-7f29-3d51591f11eb.node3.openfabric.network"
        model_result = stub.call(image_to_3d_app_id, {
            'image': image_data
        }, 'super-user')
        model_data = model_result.get('result')
        if model_data:
            model_filename = f"model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.glb"
            model_path = OUTPUT_DIR / "models" / model_filename
            if isinstance(model_data, str):
                model_bytes = base64.b64decode(model_data)
            else:
                model_bytes = model_data
            with open(model_path, 'wb') as f:
                f.write(model_bytes)
            logging.info(f"3D model saved to: {model_path}")
        else:
            raise Exception("Failed to generate 3D model")
        logging.info("Step 4: Storing in memory...")
        memory_entry = {
            'timestamp': datetime.now().isoformat(),
            'original_prompt': user_prompt,
            'enhanced_prompt': enhanced_prompt,
            'image_path': str(image_path),
            'model_path': str(model_path),
            'session_id': 'super-user'
        }
        memory_manager.store_memory(memory_entry)
        response: OutputClass = model.response
        response.message = (
            f"✅ Success! Generated 3D model from prompt: '{user_prompt}'\\n"
            f"📁 Image saved: {image_path}\\n"
            f"📁 3D Model saved: {model_path}\\n"
            f"🧠 Stored in memory for future reference."
        )
    except Exception as e:
        logging.error(f"Error in execution: {e}")
        response: OutputClass = model.response
        response.message = f"❌ Error: {str(e)}"