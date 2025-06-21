#!/usr/bin/env python3
"""
Test script for the AI Creative Pipeline
Demonstrates the complete workflow from prompt to 3D model generation
"""

import logging
import json
from pathlib import Path
from local_llm import LocalLLM
from memory_manager import MemoryManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_local_llm():
    """Test the local LLM enhancement functionality"""
    print("🧠 Testing Local LLM Enhancement...")
    
    llm = LocalLLM()
    
    test_prompts = [
        "A glowing dragon standing on a cliff at sunset",
        "A futuristic robot in a cyberpunk city",
        "A magical forest with floating islands",
        "A steampunk airship flying through clouds"
    ]
    
    for prompt in test_prompts:
        enhanced = llm.enhance_prompt(prompt)
        print(f"\nOriginal: {prompt}")
        print(f"Enhanced: {enhanced}")
        print("-" * 80)

def test_memory_manager():
    """Test the memory management functionality"""
    print("\n💾 Testing Memory Management...")
    
    memory = MemoryManager("test_memory.db")
    
    # Test storing memory
    test_entries = [
        {
            'timestamp': '2023-12-01T14:30:22',
            'session_id': 'test-user-1',
            'original_prompt': 'A dragon',
            'enhanced_prompt': 'A majestic dragon with detailed scales',
            'image_path': 'outputs/images/test_image_1.png',
            'model_path': 'outputs/models/test_model_1.glb'
        },
        {
            'timestamp': '2023-12-01T14:35:15',
            'session_id': 'test-user-1',
            'original_prompt': 'A robot',
            'enhanced_prompt': 'A futuristic robot with metallic surfaces',
            'image_path': 'outputs/images/test_image_2.png',
            'model_path': 'outputs/models/test_model_2.glb'
        }
    ]
    
    for entry in test_entries:
        success = memory.store_memory(entry)
        print(f"Stored memory entry: {'✅' if success else '❌'}")
    
    # Test retrieving memory
    session_memory = memory.get_session_memory('test-user-1')
    print(f"\nSession memory entries: {len(session_memory)}")
    
    long_term_memory = memory.get_long_term_memory()
    print(f"Long-term memory entries: {len(long_term_memory)}")
    
    # Test memory search
    search_results = memory.search_memory('dragon')
    print(f"Search results for 'dragon': {len(search_results)}")
    
    # Test memory statistics
    stats = memory.get_memory_stats()
    print(f"\nMemory Statistics:")
    print(f"  Total entries: {stats.get('total_entries', 0)}")
    print(f"  Unique sessions: {stats.get('unique_sessions', 0)}")
    print(f"  Recent entries (24h): {stats.get('recent_entries_24h', 0)}")
    print(f"  Active sessions: {stats.get('active_sessions', 0)}")

def test_output_directory_creation():
    """Test output directory creation"""
    print("\n📁 Testing Output Directory Creation...")
    
    output_dir = Path("outputs")
    images_dir = output_dir / "images"
    models_dir = output_dir / "models"
    
    # Create directories
    output_dir.mkdir(exist_ok=True)
    images_dir.mkdir(exist_ok=True)
    models_dir.mkdir(exist_ok=True)
    
    print(f"✅ Output directory: {output_dir.absolute()}")
    print(f"✅ Images directory: {images_dir.absolute()}")
    print(f"✅ Models directory: {models_dir.absolute()}")

def test_configuration():
    """Test configuration structure"""
    print("\n⚙️ Testing Configuration...")
    
    # Simulate the configuration structure expected by the app
    config = {
        'app_ids': [
            'f0997a01-d6d3-a5fe-53d8-561300318557.node3.openfabric.network',
            '69543f29-4d41-4afc-7f29-3d51591f11eb.node3.openfabric.network'
        ]
    }
    
    print(f"✅ Text-to-Image App ID: {config['app_ids'][0]}")
    print(f"✅ Image-to-3D App ID: {config['app_ids'][1]}")

def main():
    """Run all tests"""
    print("🚀 AI Creative Pipeline - Test Suite")
    print("=" * 60)
    
    try:
        test_local_llm()
        test_memory_manager()
        test_output_directory_creation()
        test_configuration()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        print("\n🎯 Next Steps:")
        print("1. Start the application: ./start.sh")
        print("2. Access Swagger UI: http://localhost:8888/swagger-ui/#/App/post_execution")
        print("3. Test with a prompt like: 'Make me a glowing dragon standing on a cliff at sunset'")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        logging.error(f"Test error: {e}")

if __name__ == "__main__":
    main() 