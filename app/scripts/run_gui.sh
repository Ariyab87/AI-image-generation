#!/bin/bash
echo "🚀 Starting AI Creative Pipeline GUI..."
echo "Access the interface at: http://localhost:8501"
echo ""
cd "$(dirname "$0")/.." && pwd
streamlit run src/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 