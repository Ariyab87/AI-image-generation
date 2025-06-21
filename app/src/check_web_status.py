#!/usr/bin/env python3
"""
Check Web Status - Show status of web services and how to access outputs
"""

import requests
import subprocess
import time
from pathlib import Path

def check_port(port):
    """Check if a port is in use"""
    try:
        response = requests.get(f"http://localhost:{port}", timeout=2)
        return True
    except:
        return False

def main():
    print("🌐 AI Creative Pipeline - Web Services Status")
    print("=" * 60)
    
    # Check main GUI (port 8501)
    print("🎨 Main GUI (Streamlit):")
    if check_port(8501):
        print("   ✅ Running at: http://localhost:8501")
        print("   📝 Features: Generate content, view memory, analytics")
    else:
        print("   ❌ Not running")
        print("   💡 Start with: ./run_gui.sh")
    
    print()
    
    # Check output viewer (port 8502)
    print("🖼️ Output Viewer:")
    if check_port(8502):
        print("   ✅ Running at: http://localhost:8502")
        print("   📝 Features: View generated images and 3D models")
    else:
        print("   ❌ Not running")
        print("   💡 Start with: ./run_output_viewer.sh")
    
    print()
    
    # Check API (port 8888)
    print("🔌 API Server:")
    if check_port(8888):
        print("   ✅ Running at: http://localhost:8888")
        print("   📝 Features: REST API, Swagger UI")
    else:
        print("   ❌ Not running")
        print("   💡 Start with: ./start.sh")
    
    print()
    
    # Show output files
    print("📁 Generated Outputs:")
    output_dir = Path("outputs")
    
    if output_dir.exists():
        images_dir = output_dir / "images"
        models_dir = output_dir / "models"
        
        if images_dir.exists():
            image_files = list(images_dir.glob("*.png"))
            print(f"   🖼️  Images: {len(image_files)} files")
            for img in image_files:
                print(f"      - {img.name}")
        
        if models_dir.exists():
            model_files = list(models_dir.glob("*.glb"))
            print(f"   🔮 3D Models: {len(model_files)} files")
            for model in model_files:
                print(f"      - {model.name}")
    else:
        print("   ❌ No outputs directory found")
    
    print()
    print("🎯 How to View Outputs:")
    print("=" * 60)
    print("1. 🌐 Web Interface:")
    print("   - Main GUI: http://localhost:8501")
    print("   - Output Viewer: http://localhost:8502")
    print("   - API Docs: http://localhost:8888")
    
    print("\n2. 📁 File System:")
    print("   - Images: outputs/images/")
    print("   - 3D Models: outputs/models/")
    
    print("\n3. 💾 Database:")
    print("   - Memory: demo_memory.db")
    print("   - Query: sqlite3 demo_memory.db")
    
    print("\n4. 🧪 Command Line:")
    print("   - Show results: python show_results.py")
    print("   - Live demo: python demo.py")

if __name__ == "__main__":
    main() 