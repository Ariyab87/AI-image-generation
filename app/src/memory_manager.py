import logging
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class MemoryManager:
    def __init__(self, db_path: str = "memory.db"):
        self.db_path = db_path
        self.short_term_memory = {}
        self._init_database()

    def _init_database(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS memory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        session_id TEXT NOT NULL,
                        original_prompt TEXT NOT NULL,
                        enhanced_prompt TEXT NOT NULL,
                        image_path TEXT,
                        model_path TEXT,
                        metadata TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_session_id ON memory(session_id)
                ''')
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_timestamp ON memory(timestamp)
                ''')
                conn.commit()
                logging.info("Memory database initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing database: {e}")

    def store_memory(self, memory_entry: Dict) -> bool:
        try:
            session_id = memory_entry.get('session_id', 'default')
            if session_id not in self.short_term_memory:
                self.short_term_memory[session_id] = []
            self.short_term_memory[session_id].append(memory_entry)
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO memory 
                    (timestamp, session_id, original_prompt, enhanced_prompt, image_path, model_path, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    memory_entry.get('timestamp'),
                    memory_entry.get('session_id'),
                    memory_entry.get('original_prompt'),
                    memory_entry.get('enhanced_prompt'),
                    memory_entry.get('image_path'),
                    memory_entry.get('model_path'),
                    json.dumps(memory_entry.get('metadata', {}))
                ))
                conn.commit()
            logging.info(f"Memory stored successfully for session: {session_id}")
            return True
        except Exception as e:
            logging.error(f"Error storing memory: {e}")
            return False

    def get_session_memory(self, session_id: str, limit: int = 10) -> List[Dict]:
        session_memory = self.short_term_memory.get(session_id, [])
        return session_memory[-limit:] if limit > 0 else session_memory

    def get_long_term_memory(self, session_id: Optional[str] = None, limit: int = 20) -> List[Dict]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if session_id:
                    cursor.execute('''
                        SELECT timestamp, session_id, original_prompt, enhanced_prompt, 
                               image_path, model_path, metadata, created_at
                        FROM memory 
                        WHERE session_id = ?
                        ORDER BY created_at DESC
                        LIMIT ?
                    ''', (session_id, limit))
                else:
                    cursor.execute('''
                        SELECT timestamp, session_id, original_prompt, enhanced_prompt, 
                               image_path, model_path, metadata, created_at
                        FROM memory 
                        ORDER BY created_at DESC
                        LIMIT ?
                    ''', (limit,))
                rows = cursor.fetchall()
                memory_entries = []
                for row in rows:
                    memory_entries.append({
                        'timestamp': row[0],
                        'session_id': row[1],
                        'original_prompt': row[2],
                        'enhanced_prompt': row[3],
                        'image_path': row[4],
                        'model_path': row[5],
                        'metadata': json.loads(row[6]) if row[6] else {},
                        'created_at': row[7]
                    })
                return memory_entries
        except Exception as e:
            logging.error(f"Error retrieving long-term memory: {e}")
            return []

    def search_memory(self, query: str, session_id: Optional[str] = None, limit: int = 10) -> List[Dict]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if session_id:
                    cursor.execute('''
                        SELECT timestamp, session_id, original_prompt, enhanced_prompt, 
                               image_path, model_path, metadata, created_at
                        FROM memory 
                        WHERE session_id = ? AND (original_prompt LIKE ? OR enhanced_prompt LIKE ?)
                        ORDER BY created_at DESC
                        LIMIT ?
                    ''', (session_id, f'%{query}%', f'%{query}%', limit))
                else:
                    cursor.execute('''
                        SELECT timestamp, session_id, original_prompt, enhanced_prompt, 
                               image_path, model_path, metadata, created_at
                        FROM memory 
                        WHERE original_prompt LIKE ? OR enhanced_prompt LIKE ?
                        ORDER BY created_at DESC
                        LIMIT ?
                    ''', (f'%{query}%', f'%{query}%', limit))
                rows = cursor.fetchall()
                memory_entries = []
                for row in rows:
                    memory_entries.append({
                        'timestamp': row[0],
                        'session_id': row[1],
                        'original_prompt': row[2],
                        'enhanced_prompt': row[3],
                        'image_path': row[4],
                        'model_path': row[5],
                        'metadata': json.loads(row[6]) if row[6] else {},
                        'created_at': row[7]
                    })
                return memory_entries
        except Exception as e:
            logging.error(f"Error searching memory: {e}")
            return []

    def get_memory_stats(self) -> Dict:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM memory')
                total_entries = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(DISTINCT session_id) FROM memory')
                unique_sessions = cursor.fetchone()[0]
                cursor.execute('''
                    SELECT COUNT(*) FROM memory 
                    WHERE created_at >= datetime('now', '-1 day')
                ''')
                recent_entries = cursor.fetchone()[0]
                return {
                    'total_entries': total_entries,
                    'unique_sessions': unique_sessions,
                    'recent_entries_24h': recent_entries,
                    'active_sessions': len(self.short_term_memory)
                }
        except Exception as e:
            logging.error(f"Error getting memory stats: {e}")
            return {}

    def clear_session_memory(self, session_id: str) -> bool:
        if session_id in self.short_term_memory:
            del self.short_term_memory[session_id]
            logging.info(f"Cleared short-term memory for session: {session_id}")
            return True
        return False

    def clear_all_memory(self) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM memory')
                conn.commit()
            self.short_term_memory.clear()
            logging.info("Cleared all long-term and short-term memory")
            return True
        except Exception as e:
            logging.error(f"Error clearing all memory: {e}")
            return False