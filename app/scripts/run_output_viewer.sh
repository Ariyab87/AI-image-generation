#!/bin/bash
echo "🖼️ Starting AI Creative Pipeline Output Viewer..."
echo "Access the output viewer at: http://localhost:8502"
echo ""
cd "$(dirname "$0")/.." && pwd
streamlit run src/web_output_viewer.py --server.port 8502 --server.address 0.0.0.0 