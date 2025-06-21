#!/usr/bin/env python3
"""
Create Demo Outputs - Generate sample images and 3D models for web display
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def create_demo_image(prompt, filename):
    """Create a demo image with the given prompt"""
    try:
        # Create a 512x512 image
        img = Image.new('RGB', (512, 512), color='#2E3440')
        draw = ImageDraw.Draw(img)
        
        # Try to use a default font
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Add title
        draw.text((20, 20), "AI Generated Image", fill='#88C0D0', font=font)
        
        # Add prompt (wrapped)
        words = prompt.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > 40:
                lines.append(' '.join(current_line[:-1]))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        y_position = 60
        for line in lines[:8]:
            draw.text((20, y_position), line, fill='#ECEFF4', font=font)
            y_position += 25
        
        # Add footer
        draw.text((20, 480), "Demo Image - AI Creative Pipeline", fill='#88C0D0', font=font)
        
        # Save the image
        img_path = Path("outputs/images") / filename
        img_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(img_path)
        
        print(f"✅ Created demo image: {img_path}")
        return img_path
        
    except Exception as e:
        print(f"❌ Error creating demo image: {e}")
        return None

def create_demo_3d_model(filename):
    """Create a demo 3D model file"""
    try:
        # Create a simple GLB file header (this is just for demo purposes)
        glb_header = b'glTF'  # GLB magic
        glb_version = b'\x02\x00\x00\x00'  # Version 2
        glb_length = b'\x20\x00\x00\x00'  # Length
        glb_json_length = b'\x0c\x00\x00\x00'  # JSON length
        glb_json_format = b'\x00\x00\x00\x00'  # JSON format
        
        # Simple JSON content
        json_content = b'{"asset":{"version":"2.0"},"scene":0,"scenes":[{"nodes":[]}],"nodes":[],"meshes":[]}'
        
        # Pad JSON to 4-byte boundary
        while len(json_content) % 4 != 0:
            json_content += b' '
        
        # Update JSON length
        glb_json_length = len(json_content).to_bytes(4, 'little')
        
        # Binary data (empty for demo)
        binary_data = b''
        binary_length = len(binary_data).to_bytes(4, 'little')
        
        # Combine all parts
        glb_content = glb_header + glb_version + glb_length + glb_json_length + glb_json_format + json_content + binary_length + binary_data
        
        # Save the file
        model_path = Path("outputs/models") / filename
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(model_path, 'wb') as f:
            f.write(glb_content)
        
        print(f"✅ Created demo 3D model: {model_path}")
        return model_path
        
    except Exception as e:
        print(f"❌ Error creating demo 3D model: {e}")
        return None

def main():
    print("🎨 Creating Demo Outputs for Web Display")
    print("=" * 50)
    
    # Create output directories
    Path("outputs/images").mkdir(parents=True, exist_ok=True)
    Path("outputs/models").mkdir(parents=True, exist_ok=True)
    
    # Demo prompts and their corresponding files
    demos = [
        {
            "prompt": "A glowing dragon standing on a cliff at sunset",
            "image_file": "dragon_sunset.png",
            "model_file": "dragon_sunset.glb"
        },
        {
            "prompt": "A futuristic robot in a cyberpunk city",
            "image_file": "cyberpunk_robot.png",
            "model_file": "cyberpunk_robot.glb"
        },
        {
            "prompt": "A magical forest with floating islands",
            "image_file": "magical_forest.png",
            "model_file": "magical_forest.glb"
        },
        {
            "prompt": "A steampunk airship flying through clouds",
            "image_file": "steampunk_airship.png",
            "model_file": "steampunk_airship.glb"
        }
    ]
    
    created_files = []
    
    for demo in demos:
        print(f"\n🎨 Creating demo for: {demo['prompt']}")
        
        # Create demo image
        image_path = create_demo_image(demo['prompt'], demo['image_file'])
        if image_path:
            created_files.append(str(image_path))
        
        # Create demo 3D model
        model_path = create_demo_3d_model(demo['model_file'])
        if model_path:
            created_files.append(str(model_path))
    
    print("\n" + "=" * 50)
    print("✅ Demo outputs created successfully!")
    print(f"📁 Created {len(created_files)} files")
    
    print("\n🎯 Next Steps:")
    print("1. Run the web output viewer: ./run_output_viewer.sh")
    print("2. Visit: http://localhost:8502")
    print("3. View all generated images and 3D models")
    
    print("\n📁 Created files:")
    for file_path in created_files:
        print(f"   - {file_path}")

if __name__ == "__main__":
    main() 