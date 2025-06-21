import logging
import subprocess
import json
from typing import Optional

class LocalLLM:
    def __init__(self):
        self.model_type = self._detect_available_model()
        logging.info(f"Initialized LocalLLM with model type: {self.model_type}")

    def _detect_available_model(self) -> str:
        try:
            result = subprocess.run(['which', 'deepseek'], capture_output=True, text=True)
            if result.returncode == 0:
                return 'deepseek'
            result = subprocess.run(['which', 'llama'], capture_output=True, text=True)
            if result.returncode == 0:
                return 'llama'
            result = subprocess.run(['which', 'llama-cpp'], capture_output=True, text=True)
            if result.returncode == 0:
                return 'llama'
        except Exception as e:
            logging.warning(f"Error detecting local models: {e}")
        return 'fallback'

    def enhance_prompt(self, user_prompt: str) -> str:
        if self.model_type == 'deepseek':
            return self._enhance_with_deepseek(user_prompt)
        elif self.model_type == 'llama':
            return self._enhance_with_llama(user_prompt)
        else:
            return self._enhance_fallback(user_prompt)

    def _enhance_with_deepseek(self, user_prompt: str) -> str:
        try:
            system_prompt = """You are an expert at creating detailed, artistic descriptions for image generation. 
            Take the user's simple idea and expand it into a rich, vivid description that includes:
            - Visual details (colors, lighting, composition)
            - Artistic style suggestions
            - Atmospheric elements
            - Technical details for high-quality image generation
            Keep the enhanced description under 200 words but make it highly detailed and artistic."""
            full_prompt = f"{system_prompt}\\n\\nUser request: {user_prompt}\\n\\nEnhanced description:"
            result = subprocess.run([
                'deepseek', 'generate', 
                '--prompt', full_prompt,
                '--max-tokens', '300'
            ], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                enhanced = result.stdout.strip()
                return enhanced if enhanced else self._enhance_fallback(user_prompt)
            else:
                logging.warning(f"DeepSeek failed: {result.stderr}")
                return self._enhance_fallback(user_prompt)
        except Exception as e:
            logging.error(f"Error with DeepSeek: {e}")
            return self._enhance_fallback(user_prompt)

    def _enhance_with_llama(self, user_prompt: str) -> str:
        try:
            system_prompt = """You are an expert at creating detailed, artistic descriptions for image generation. 
            Take the user's simple idea and expand it into a rich, vivid description that includes:
            - Visual details (colors, lighting, composition)
            - Artistic style suggestions
            - Atmospheric elements
            - Technical details for high-quality image generation
            Keep the enhanced description under 200 words but make it highly detailed and artistic."""
            full_prompt = f"{system_prompt}\\n\\nUser request: {user_prompt}\\n\\nEnhanced description:"
            result = subprocess.run([
                'llama', 'generate', 
                '--prompt', full_prompt,
                '--max-tokens', '300'
            ], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                enhanced = result.stdout.strip()
                return enhanced if enhanced else self._enhance_fallback(user_prompt)
            else:
                logging.warning(f"Llama failed: {result.stderr}")
                return self._enhance_fallback(user_prompt)
        except Exception as e:
            logging.error(f"Error with Llama: {e}")
            return self._enhance_fallback(user_prompt)

    def _enhance_fallback(self, user_prompt: str) -> str:
        enhancements = {
            'dragon': 'A majestic dragon with detailed scales, glowing eyes, and dramatic lighting',
            'robot': 'A futuristic robot with metallic surfaces, glowing components, and sci-fi aesthetics',
            'city': 'A detailed cityscape with architectural elements, atmospheric lighting, and urban textures',
            'landscape': 'A breathtaking landscape with natural elements, atmospheric perspective, and rich colors',
            'portrait': 'A detailed portrait with expressive features, professional lighting, and artistic composition',
            'animal': 'A detailed animal with realistic fur/textures, natural lighting, and dynamic pose',
            'fantasy': 'A magical fantasy scene with ethereal lighting, mystical elements, and artistic style',
            'cyberpunk': 'A cyberpunk scene with neon lighting, futuristic elements, and dystopian atmosphere'
        }
        user_prompt_lower = user_prompt.lower()
        for keyword, enhancement in enhancements.items():
            if keyword in user_prompt_lower:
                return f"{user_prompt}, {enhancement}, high quality, detailed, professional photography, 8k resolution"
        return f"{user_prompt}, highly detailed, professional quality, artistic composition, dramatic lighting, 8k resolution, photorealistic" 