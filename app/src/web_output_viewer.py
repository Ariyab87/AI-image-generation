#!/usr/bin/env python3
"""
Web Output Viewer - Display AI Creative Pipeline outputs in web interface
"""

import streamlit as st
import os
from pathlib import Path
from PIL import Image
from datetime import datetime
from memory_manager import MemoryManager

def main():
    st.set_page_config(
        page_title="AI Pipeline Outputs",
        page_icon="🖼️",
        layout="wide"
    )
    
    st.title("🖼️ AI Creative Pipeline - Output Viewer")
    st.markdown("View all generated images and 3D models")
    
    # Initialize memory manager
    memory = MemoryManager("demo_memory.db")
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["🖼️ Images", "🔮 3D Models", "📊 All Results"])
    
    with tab1:
        st.header("🖼️ Generated Images")
        
        output_dir = Path("outputs")
        images_dir = output_dir / "images"
        
        if images_dir.exists():
            image_files = list(images_dir.glob("*.png"))
            
            if image_files:
                st.success(f"Found {len(image_files)} generated images")
                
                # Display images in a grid
                cols = st.columns(min(3, len(image_files)))
                
                for i, img_path in enumerate(image_files):
                    with cols[i % 3]:
                        try:
                            image = Image.open(img_path)
                            st.image(image, caption=img_path.name, use_column_width=True)
                            
                            # File info
                            file_size = os.path.getsize(img_path)
                            created_time = datetime.fromtimestamp(os.path.getctime(img_path))
                            
                            st.caption(f"📁 Size: {file_size:,} bytes")
                            st.caption(f"📅 Created: {created_time.strftime('%Y-%m-%d %H:%M')}")
                            
                        except Exception as e:
                            st.error(f"Error loading {img_path.name}: {e}")
            else:
                st.info("No images found. Generate some images first!")
                st.info("💡 Images will appear here after running the AI pipeline")
        else:
            st.info("Images directory not found")
    
    with tab2:
        st.header("🔮 Generated 3D Models")
        
        models_dir = output_dir / "models"
        
        if models_dir.exists():
            model_files = list(models_dir.glob("*.glb"))
            
            if model_files:
                st.success(f"Found {len(model_files)} generated 3D models")
                
                for model_path in model_files:
                    with st.expander(f"3D Model: {model_path.name}"):
                        # File info
                        file_size = os.path.getsize(model_path)
                        created_time = datetime.fromtimestamp(os.path.getctime(model_path))
                        
                        st.info(f"📁 File: {model_path}")
                        st.info(f"💾 Size: {file_size:,} bytes")
                        st.info(f"📅 Created: {created_time.strftime('%Y-%m-%d %H:%M')}")
                        
                        # GLB file info
                        if model_path.endswith('.glb'):
                            st.success("🎮 GLB 3D Model File")
                            st.markdown("**Compatible with:**")
                            st.markdown("- 🌐 Web browsers (with 3D viewers)")
                            st.markdown("- 🎨 3D software (Blender, Maya, 3ds Max)")
                            st.markdown("- 🎮 Game engines (Unity, Unreal Engine)")
                            st.markdown("- 📱 Mobile apps (with 3D support)")
                            
                            # Download button
                            with open(model_path, "rb") as file:
                                st.download_button(
                                    label=f"📥 Download {model_path.name}",
                                    data=file.read(),
                                    file_name=model_path.name,
                                    mime="model/gltf-binary"
                                )
            else:
                st.info("No 3D models found. Generate some models first!")
                st.info("💡 3D models will appear here after running the AI pipeline")
        else:
            st.info("Models directory not found")
    
    with tab3:
        st.header("📊 All Results from Memory")
        
        # Get all memory entries
        all_memory = memory.get_long_term_memory(limit=50)
        
        if all_memory:
            st.success(f"Found {len(all_memory)} results in memory")
            
            for i, entry in enumerate(all_memory):
                with st.expander(f"Result {i+1}: {entry['original_prompt'][:50]}..."):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**🎨 Original Prompt:** {entry['original_prompt']}")
                        st.write(f"**🧠 Enhanced Prompt:** {entry['enhanced_prompt'][:100]}...")
                        st.write(f"**📅 Created:** {entry['created_at']}")
                        st.write(f"**👤 Session:** {entry['session_id']}")
                    
                    with col2:
                        # Show image if exists
                        if entry.get('image_path') and os.path.exists(entry['image_path']):
                            try:
                                image = Image.open(entry['image_path'])
                                st.image(image, caption="Generated Image", use_column_width=True)
                            except:
                                st.info("✅ Image file exists")
                        elif entry.get('image_path'):
                            st.info(f"❌ Image not found: {entry['image_path']}")
                        
                        # Show 3D model info
                        if entry.get('model_path') and os.path.exists(entry['model_path']):
                            st.success(f"✅ 3D Model: {Path(entry['model_path']).name}")
                        elif entry.get('model_path'):
                            st.info(f"❌ 3D Model not found: {entry['model_path']}")
        else:
            st.info("No results found in memory")
    
    # Sidebar with statistics
    st.sidebar.title("📈 Statistics")
    
    # File counts
    if output_dir.exists():
        images_dir = output_dir / "images"
        models_dir = output_dir / "models"
        
        image_count = len(list(images_dir.glob("*.png"))) if images_dir.exists() else 0
        model_count = len(list(models_dir.glob("*.glb"))) if models_dir.exists() else 0
        
        st.sidebar.metric("🖼️ Images", image_count)
        st.sidebar.metric("🔮 3D Models", model_count)
    
    # Memory stats
    stats = memory.get_memory_stats()
    st.sidebar.metric("📊 Memory Entries", stats.get('total_entries', 0))
    st.sidebar.metric("👥 Sessions", stats.get('unique_sessions', 0))
    
    # Instructions
    st.sidebar.title("💡 Instructions")
    st.sidebar.markdown("""
    1. **Generate Content**: Use the main app to create images and 3D models
    2. **View Results**: Check this page to see all generated outputs
    3. **Download**: Click download buttons to save 3D models
    4. **Memory**: View complete workflow history
    """)

if __name__ == "__main__":
    main() 