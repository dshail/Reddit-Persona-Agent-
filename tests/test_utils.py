import os
import pytest
from utils import clean_text, chunk_text, save_persona_to_file

def test_clean_text_removes_newlines_and_extra_spaces():
    raw_text = "This is a sample text.\nIt has line breaks.   And   extra spaces."
    cleaned = clean_text(raw_text)
    assert "\n" not in cleaned
    assert "  " not in cleaned
    assert cleaned == "This is a sample text. It has line breaks. And extra spaces."

def test_chunk_text_creates_chunks_correctly():
    texts = ["word " * 50, "word " * 50, "word " * 50]  # 3 texts with 50 words each
    chunks = chunk_text(texts, chunk_size=100)
    assert isinstance(chunks, list)
    assert len(chunks) >= 1
    for chunk in chunks:
        assert len(chunk) <= 3000  # Default chunk size

def test_save_persona_to_file_creates_output_file(tmp_path):
    username = "testuser"
    persona = "This is a test persona."
    
    # Temporarily change to tmp directory
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    
    try:
        file_path = save_persona_to_file(username, persona)
        assert os.path.exists(file_path)
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert persona in content
    finally:
        os.chdir(original_cwd)
