# 🚀 AI Creative Pipeline - Text to 3D Model Generator

An intelligent, end-to-end pipeline that transforms simple text prompts into stunning 3D models using local LLM processing and Openfabric applications.

## 🌟 Features

- **🧠 Local LLM Integration**: Uses DeepSeek or Llama models to enhance user prompts (with intelligent fallback)
- **🎨 Text-to-Image Generation**: Converts enhanced prompts into high-quality images
- **🔮 Image-to-3D Conversion**: Transforms images into interactive 3D models
- **💾 Memory System**: Both short-term (session) and long-term (persistent) memory storage
- **🔍 Memory Search**: Find and recall previous generations
- **📊 Memory Analytics**: Track usage statistics and patterns

## 🛠 Architecture

```
User Prompt
    ↓
Local LLM Enhancement (DeepSeek/Llama/Fallback)
    ↓
Text-to-Image App (Openfabric)
    ↓
Generated Image
    ↓
Image-to-3D App (Openfabric)
    ↓
3D Model Output
    ↓
Memory Storage (SQLite + Session Cache)
```

## 📦 Installation

### Prerequisites

- Python 3.8+
- Poetry (for dependency management)
- Local LLM (optional - DeepSeek or Llama for enhanced prompt processing)

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-test/app
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Configure the application**
   - The app uses Openfabric apps with predefined IDs
   - Text-to-Image: `f0997a01-d6d3-a5fe-53d8-561300318557.node3.openfabric.network`
   - Image-to-3D: `69543f29-4d41-4afc-7f29-3d51591f11eb.node3.openfabric.network`

## 🚀 Usage

### Running the Application

#### Option 1: Local Development
```bash
./start.sh
```

#### Option 2: Docker
```bash
docker build -t ai-pipeline .
docker run -p 8888:8888 ai-pipeline
```

### API Endpoint

Once running, access the Swagger UI at:
```
http://localhost:8888/swagger-ui/#/App/post_execution
```

### Example Usage

**Request:**
```json
{
  "prompt": "Make me a glowing dragon standing on a cliff at sunset"
}
```

**Response:**
```json
{
  "message": "✅ Success! Generated 3D model from prompt: 'Make me a glowing dragon standing on a cliff at sunset'\n📁 Image saved: outputs/images/image_20231201_143022.png\n📁 3D Model saved: outputs/models/model_20231201_143022.glb\n🧠 Stored in memory for future reference."
}
```

## 🧠 Memory System

### Short-Term Memory (Session)
- Stored in memory during active sessions
- Automatically cleared when session ends
- Fast access for recent generations

### Long-Term Memory (Persistent)
- SQLite database storage
- Survives application restarts
- Searchable and queryable

### Memory Operations

```python
# Get session memory
session_memory = memory_manager.get_session_memory('super-user', limit=10)

# Get long-term memory
long_term_memory = memory_manager.get_long_term_memory(limit=20)

# Search memory
search_results = memory_manager.search_memory('dragon', limit=5)

# Get memory statistics
stats = memory_manager.get_memory_stats()
```

## 🎨 Local LLM Integration

### Supported Models

1. **DeepSeek**: Advanced prompt enhancement
2. **Llama**: Alternative local processing
3. **Fallback**: Intelligent keyword-based enhancement

### Model Detection

The system automatically detects available local LLM installations:
- Checks for `deepseek` command
- Checks for `llama` or `llama-cpp` commands
- Falls back to intelligent prompt enhancement

### Prompt Enhancement Examples

**Input:** "A robot"
**Enhanced:** "A robot, A futuristic robot with metallic surfaces, glowing components, and sci-fi aesthetics, high quality, detailed, professional photography, 8k resolution"

**Input:** "Cyberpunk city"
**Enhanced:** "Cyberpunk city, A cyberpunk scene with neon lighting, futuristic elements, and dystopian atmosphere, high quality, detailed, professional photography, 8k resolution"

## 📁 Output Structure

```
outputs/
├── images/
│   ├── image_20231201_143022.png
│   └── image_20231201_143045.png
└── models/
    ├── model_20231201_143022.glb
    └── model_20231201_143045.glb
```

## 🔧 Configuration

### Environment Variables

- `OUTPUT_DIR`: Directory for generated files (default: `outputs`)
- `MEMORY_DB_PATH`: SQLite database path (default: `memory.db`)

### App Configuration

The application expects configuration with Openfabric app IDs:
```python
config = ConfigClass(
    app_ids=[
        "f0997a01-d6d3-a5fe-53d8-561300318557.node3.openfabric.network",
        "69543f29-4d41-4afc-7f29-3d51591f11eb.node3.openfabric.network"
    ]
)
```

## 🧪 Testing

Run the test suite:
```bash
poetry run pytest
```

## 📊 Monitoring

### Logs
The application provides detailed logging for:
- LLM processing steps
- Openfabric API calls
- Memory operations
- Error handling

### Memory Statistics
Track usage patterns:
- Total entries stored
- Unique sessions
- Recent activity (24h)
- Active sessions

## 🚀 Advanced Features

### Memory Search
Find previous generations by content:
```python
# Search for dragon-related generations
results = memory_manager.search_memory('dragon')

# Search within specific session
session_results = memory_manager.search_memory('robot', session_id='user123')
```

### Memory Analytics
```python
stats = memory_manager.get_memory_stats()
print(f"Total entries: {stats['total_entries']}")
print(f"Unique sessions: {stats['unique_sessions']}")
print(f"Recent entries (24h): {stats['recent_entries_24h']}")
```

## 🔒 Security

- No external API calls (except Openfabric apps)
- Local LLM processing
- SQLite database with proper indexing
- Session-based memory isolation

## 🐛 Troubleshooting

### Common Issues

1. **Local LLM not found**
   - Install DeepSeek or Llama locally
   - System will fall back to intelligent enhancement

2. **Openfabric connection issues**
   - Verify app IDs are correct
   - Check network connectivity

3. **Memory database errors**
   - Ensure write permissions in app directory
   - Check SQLite installation

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Openfabric for the AI application platform
- DeepSeek and Llama for local LLM capabilities
- The AI development community for inspiration

---

**Built with ❤️ for the AI Developer Challenge** 