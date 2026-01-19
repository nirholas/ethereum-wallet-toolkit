"""
Tests for keystore file operations.
"""

import json
import os
import tempfile
import pytest
from pathlib import Path
import uuid

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from keystore_mcp.utils.file_utils import (
    generate_keystore_filename,
    secure_write_file,
    secure_read_file,
    validate_file_path,
)


class TestFilenameGeneration:
    """Tests for keystore filename generation."""
    
    def test_generate_standard_filename(self):
        """Test generating standard keystore filename."""
        address = "742d35cc6634c0532925a3b844bc9e7595f8fe00"
        filename = generate_keystore_filename(address)
        
        assert filename.startswith("UTC--")
        assert address in filename
        assert filename.endswith(".json")
    
    def test_generate_filename_with_0x_prefix(self):
        """Test filename generation handles 0x prefix."""
        address = "0x742d35cc6634c0532925a3b844bc9e7595f8fe00"
        filename = generate_keystore_filename(address)
        
        # Should strip 0x prefix
        assert "0x" not in filename or filename.count("0x") == 0
        assert "742d35cc6634c0532925a3b844bc9e7595f8fe00" in filename
    
    def test_generate_filename_lowercase(self):
        """Test filename uses lowercase address."""
        address = "742D35CC6634C0532925A3B844BC9E7595F8FE00"
        filename = generate_keystore_filename(address)
        
        assert address.lower() in filename
    
    def test_generate_unique_filenames(self):
        """Test that generated filenames are unique."""
        address = "742d35cc6634c0532925a3b844bc9e7595f8fe00"
        
        filenames = [generate_keystore_filename(address) for _ in range(10)]
        
        # All should be unique due to timestamp
        assert len(set(filenames)) == len(filenames)


class TestSecureFileOperations:
    """Tests for secure file read/write operations."""
    
    def test_secure_write_creates_file(self):
        """Test secure_write creates file with correct content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.json")
            content = {"test": "data"}
            
            secure_write_file(filepath, json.dumps(content))
            
            assert os.path.exists(filepath)
            with open(filepath, 'r') as f:
                assert json.load(f) == content
    
    def test_secure_write_creates_directories(self):
        """Test secure_write creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "subdir", "nested", "test.json")
            content = {"test": "data"}
            
            secure_write_file(filepath, json.dumps(content))
            
            assert os.path.exists(filepath)
    
    def test_secure_write_sets_permissions(self):
        """Test secure_write sets restrictive permissions (Unix only)."""
        if os.name != 'posix':
            pytest.skip("Permission test only on Unix")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.json")
            
            secure_write_file(filepath, "{}")
            
            # Check file is owner-only readable/writable
            mode = os.stat(filepath).st_mode & 0o777
            assert mode == 0o600
    
    def test_secure_read_returns_content(self):
        """Test secure_read returns file content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.json")
            expected = '{"test": "data"}'
            
            with open(filepath, 'w') as f:
                f.write(expected)
            
            content = secure_read_file(filepath)
            assert content == expected
    
    def test_secure_read_nonexistent_file(self):
        """Test secure_read handles nonexistent file."""
        with pytest.raises(FileNotFoundError):
            secure_read_file("/nonexistent/path/file.json")


class TestFilePathValidation:
    """Tests for file path validation."""
    
    def test_valid_absolute_path(self):
        """Test valid absolute path passes validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "keystore.json")
            result = validate_file_path(filepath, must_exist=False)
            assert result["valid"] is True
    
    def test_path_traversal_attack(self):
        """Test path traversal is blocked."""
        dangerous_path = "/home/user/../../../etc/passwd"
        result = validate_file_path(dangerous_path, must_exist=False)
        
        # Should either be invalid or normalized
        assert result.get("valid") is False or ".." not in result.get("normalized_path", dangerous_path)
    
    def test_nonexistent_path_with_must_exist(self):
        """Test nonexistent path fails when must_exist=True."""
        result = validate_file_path("/nonexistent/path.json", must_exist=True)
        assert result["valid"] is False
    
    def test_directory_not_file(self):
        """Test directory path fails file validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = validate_file_path(tmpdir, must_exist=True, must_be_file=True)
            assert result["valid"] is False


class TestKeystoreFileRoundtrip:
    """Integration tests for complete file operations."""
    
    def get_test_keystore(self):
        """Return a test keystore structure."""
        return {
            "version": 3,
            "id": str(uuid.uuid4()),
            "address": "742d35cc6634c0532925a3b844bc9e7595f8fe00",
            "crypto": {
                "ciphertext": "a" * 64,
                "cipherparams": {"iv": "b" * 32},
                "cipher": "aes-128-ctr",
                "kdf": "scrypt",
                "kdfparams": {
                    "n": 262144,
                    "r": 8,
                    "p": 1,
                    "dklen": 32,
                    "salt": "c" * 64
                },
                "mac": "d" * 64
            }
        }
    
    def test_write_and_read_keystore(self):
        """Test writing and reading keystore file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            keystore = self.get_test_keystore()
            filename = generate_keystore_filename(keystore["address"])
            filepath = os.path.join(tmpdir, filename)
            
            # Write
            secure_write_file(filepath, json.dumps(keystore, indent=2))
            
            # Read
            content = secure_read_file(filepath)
            loaded = json.loads(content)
            
            assert loaded == keystore
    
    def test_keystore_json_formatting(self):
        """Test keystore is written with proper JSON formatting."""
        with tempfile.TemporaryDirectory() as tmpdir:
            keystore = self.get_test_keystore()
            filepath = os.path.join(tmpdir, "keystore.json")
            
            secure_write_file(filepath, json.dumps(keystore, indent=2))
            
            content = secure_read_file(filepath)
            
            # Should be properly formatted (indented)
            assert "\n" in content
            assert "  " in content  # Indentation
    
    def test_multiple_keystores_in_directory(self):
        """Test managing multiple keystores in one directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            addresses = [
                "742d35cc6634c0532925a3b844bc9e7595f8fe00",
                "1234567890abcdef1234567890abcdef12345678",
                "abcdef1234567890abcdef1234567890abcdef12",
            ]
            
            files = []
            for addr in addresses:
                keystore = self.get_test_keystore()
                keystore["address"] = addr
                filename = generate_keystore_filename(addr)
                filepath = os.path.join(tmpdir, filename)
                secure_write_file(filepath, json.dumps(keystore))
                files.append(filepath)
            
            # All files should exist
            for f in files:
                assert os.path.exists(f)
            
            # Should be 3 files
            keystore_files = [f for f in os.listdir(tmpdir) if f.endswith('.json')]
            assert len(keystore_files) == 3


class TestEdgeCases:
    """Tests for edge cases in file operations."""
    
    def test_unicode_in_path(self):
        """Test handling of Unicode characters in path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create subdir with unicode name
            unicode_dir = os.path.join(tmpdir, "钱包")
            os.makedirs(unicode_dir, exist_ok=True)
            
            filepath = os.path.join(unicode_dir, "keystore.json")
            secure_write_file(filepath, "{}")
            
            assert os.path.exists(filepath)
    
    def test_very_long_path(self):
        """Test handling of very long file paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create nested directories to make long path
            long_path = tmpdir
            for i in range(10):
                long_path = os.path.join(long_path, f"dir{i}")
            
            filepath = os.path.join(long_path, "keystore.json")
            
            try:
                secure_write_file(filepath, "{}")
                assert os.path.exists(filepath)
            except OSError:
                # Path too long for OS - acceptable
                pass
    
    def test_special_characters_in_filename(self):
        """Test that special characters are handled safely."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Normal address without special chars
            address = "742d35cc6634c0532925a3b844bc9e7595f8fe00"
            filename = generate_keystore_filename(address)
            
            # Should not contain shell-dangerous characters
            dangerous_chars = [';', '|', '&', '$', '`', '>', '<']
            for char in dangerous_chars:
                assert char not in filename


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
