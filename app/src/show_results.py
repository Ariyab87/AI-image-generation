#!/usr/bin/env python3
"""
Show Results - Display all AI Creative Pipeline results
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime

def show_memory_results():
    """Show all results stored in memory"""
    print("🧠 AI CREATIVE PIPELINE - ALL RESULTS")
    print("=" * 80)
    
    try:
        # Connect to the demo memory database
        conn = sqlite3.connect('demo_memory.db')
        cursor = conn.cursor()
        
        # Get all memory entries
        cursor.execute('''
            SELECT original_prompt, enhanced_prompt, image_path, model_path, created_at, session_id
            FROM memory 
            ORDER BY created_at DESC
        ''')
        
        rows = cursor.fetchall()
        
        if not rows:
            print("❌ No results found in memory database")
            return
        
        print(f"📊 Found {len(rows)} results in memory database\n")
        
        for i, row in enumerate(rows, 1):
            original_prompt, enhanced_prompt, image_path, model_path, created_at, session_id = row
            
            print(f"🎯 RESULT #{i}")
            print(f"   📅 Created: {created_at}")
            print(f"   👤 Session: {session_id}")
            print(f"   🎨 Original Prompt: {original_prompt}")
            print(f"   🧠 Enhanced Prompt: {enhanced_prompt[:100]}...")
            print(f"   🖼️  Image: {image_path}")
            print(f"   🔮 3D Model: {model_path}")
            
            # Check if files exist
            image_exists = os.path.exists(image_path)
            model_exists = os.path.exists(model_path)
            
            print(f"   📁 Image exists: {'✅' if image_exists else '❌'}")
            print(f"   📁 3D Model exists: {'✅' if model_exists else '❌'}")
            print("-" * 80)
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading memory database: {e}")

def show_file_structure():
    """Show the file structure of generated outputs"""
    print("\n📁 OUTPUT FILE STRUCTURE")
    print("=" * 80)
    
    output_dir = Path("outputs")
    
    if not output_dir.exists():
        print("❌ Outputs directory not found")
        return
    
    print(f"📂 Root directory: {output_dir.absolute()}")
    
    # Check images directory
    images_dir = output_dir / "images"
    if images_dir.exists():
        image_files = list(images_dir.glob("*.png"))
        print(f"🖼️  Images directory: {images_dir}")
        print(f"   📄 Found {len(image_files)} image files")
        for img in image_files:
            print(f"      - {img.name}")
    else:
        print("❌ Images directory not found")
    
    # Check models directory
    models_dir = output_dir / "models"
    if models_dir.exists():
        model_files = list(models_dir.glob("*.glb"))
        print(f"🔮 Models directory: {models_dir}")
        print(f"   📄 Found {len(model_files)} 3D model files")
        for model in model_files:
            print(f"      - {model.name}")
    else:
        print("❌ Models directory not found")

def show_database_info():
    """Show information about the memory databases"""
    print("\n💾 MEMORY DATABASE INFORMATION")
    print("=" * 80)
    
    databases = ['demo_memory.db', 'test_memory.db', 'memory.db']
    
    for db_name in databases:
        if os.path.exists(db_name):
            try:
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()
                
                # Get table info
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                # Get row count
                cursor.execute("SELECT COUNT(*) FROM memory")
                count = cursor.fetchone()[0]
                
                # Get file size
                file_size = os.path.getsize(db_name)
                
                print(f"📊 Database: {db_name}")
                print(f"   📄 Tables: {[table[0] for table in tables]}")
                print(f"   📊 Entries: {count}")
                print(f"   💾 Size: {file_size} bytes")
                print()
                
                conn.close()
                
            except Exception as e:
                print(f"❌ Error reading {db_name}: {e}")
        else:
            print(f"❌ Database {db_name} not found")

def show_summary():
    """Show a summary of all results"""
    print("\n📈 RESULTS SUMMARY")
    print("=" * 80)
    
    try:
        conn = sqlite3.connect('demo_memory.db')
        cursor = conn.cursor()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM memory")
        total_count = cursor.fetchone()[0]
        
        # Get unique sessions
        cursor.execute("SELECT COUNT(DISTINCT session_id) FROM memory")
        unique_sessions = cursor.fetchone()[0]
        
        # Get recent entries (last 24 hours)
        cursor.execute('''
            SELECT COUNT(*) FROM memory 
            WHERE created_at >= datetime('now', '-1 day')
        ''')
        recent_count = cursor.fetchone()[0]
        
        # Get most common keywords
        cursor.execute('''
            SELECT original_prompt FROM memory
        ''')
        prompts = cursor.fetchall()
        
        keywords = {}
        for prompt in prompts:
            words = prompt[0].lower().split()
            for word in words:
                if len(word) > 3:  # Only count words longer than 3 characters
                    keywords[word] = keywords.get(word, 0) + 1
        
        # Get top keywords
        top_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:5]
        
        print(f"📊 Total Results: {total_count}")
        print(f"👥 Unique Sessions: {unique_sessions}")
        print(f"🕐 Recent (24h): {recent_count}")
        print(f"🔍 Top Keywords: {[f'{word}({count})' for word, count in top_keywords]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error generating summary: {e}")

def main():
    """Show all results"""
    print("🚀 AI CREATIVE PIPELINE - RESULTS VIEWER")
    print("=" * 80)
    
    # Show memory results
    show_memory_results()
    
    # Show file structure
    show_file_structure()
    
    # Show database info
    show_database_info()
    
    # Show summary
    show_summary()
    
    print("\n" + "=" * 80)
    print("🎯 HOW TO VIEW RESULTS:")
    print("=" * 80)
    print("1. 📁 Generated Files: Check outputs/images/ and outputs/models/")
    print("2. 💾 Memory Database: Query demo_memory.db with SQLite")
    print("3. 🌐 Web Interface: Run ./run_gui.sh and visit http://localhost:8501")
    print("4. 📊 API Results: Run ./start.sh and use Swagger UI")
    print("5. 🧪 Live Demo: Run python demo.py for real-time results")
    print("=" * 80)

if __name__ == "__main__":
    main() 