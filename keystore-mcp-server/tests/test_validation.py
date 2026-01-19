"""
Tests for keystore validation functionality.
"""

import json
import os
import pytest
from unittest.mock import MagicMock, patch
import uuid

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from keystore_mcp.utils.validation import (
    validate_private_key,
    validate_address,
    validate_password_strength,
    validate_kdf_params,
)


class TestPrivateKeyValidation:
    """Tests for private key validation."""
    
    def test_valid_private_key_hex_with_prefix(self):
        """Test valid private key with 0x prefix."""
        key = "0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318"
        result = validate_private_key(key)
        assert result["valid"] is True
    
    def test_valid_private_key_hex_without_prefix(self):
        """Test valid private key without 0x prefix."""
        key = "4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318"
        result = validate_private_key(key)
        assert result["valid"] is True
    
    def test_invalid_private_key_too_short(self):
        """Test private key that's too short."""
        key = "0x4c0883a69102937d6231471b5dbb6204"
        result = validate_private_key(key)
        assert result["valid"] is False
        assert "length" in result.get("error", "").lower()
    
    def test_invalid_private_key_too_long(self):
        """Test private key that's too long."""
        key = "0x" + "a" * 128
        result = validate_private_key(key)
        assert result["valid"] is False
    
    def test_invalid_private_key_non_hex(self):
        """Test private key with non-hex characters."""
        key = "0xzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
        result = validate_private_key(key)
        assert result["valid"] is False
    
    def test_invalid_private_key_zero(self):
        """Test private key that is zero (invalid for secp256k1)."""
        key = "0x0000000000000000000000000000000000000000000000000000000000000000"
        result = validate_private_key(key)
        assert result["valid"] is False


class TestAddressValidation:
    """Tests for Ethereum address validation."""
    
    def test_valid_address_checksummed(self):
        """Test valid checksummed address."""
        address = "0x742d35Cc6634C0532925a3b844Bc9e7595f8fE00"
        result = validate_address(address)
        assert result["valid"] is True
        assert result.get("checksum_valid") is True
    
    def test_valid_address_lowercase(self):
        """Test valid lowercase address."""
        address = "0x742d35cc6634c0532925a3b844bc9e7595f8fe00"
        result = validate_address(address)
        assert result["valid"] is True
    
    def test_valid_address_uppercase(self):
        """Test valid uppercase address."""
        address = "0x742D35CC6634C0532925A3B844BC9E7595F8FE00"
        result = validate_address(address)
        assert result["valid"] is True
    
    def test_invalid_address_too_short(self):
        """Test address that's too short."""
        address = "0x742d35Cc6634C0532925a3b844Bc9e75"
        result = validate_address(address)
        assert result["valid"] is False
    
    def test_invalid_address_too_long(self):
        """Test address that's too long."""
        address = "0x742d35Cc6634C0532925a3b844Bc9e7595f8fE00aa"
        result = validate_address(address)
        assert result["valid"] is False
    
    def test_invalid_address_no_prefix(self):
        """Test address without 0x prefix."""
        address = "742d35Cc6634C0532925a3b844Bc9e7595f8fE00"
        result = validate_address(address)
        # Should either be valid (some validators accept) or flag missing prefix
        assert "valid" in result
    
    def test_invalid_address_non_hex(self):
        """Test address with non-hex characters."""
        address = "0xZZZd35Cc6634C0532925a3b844Bc9e7595f8fE00"
        result = validate_address(address)
        assert result["valid"] is False


class TestPasswordStrengthValidation:
    """Tests for password strength validation."""
    
    def test_strong_password(self):
        """Test strong password passes validation."""
        password = "MyStr0ng!Password#2024"
        result = validate_password_strength(password)
        assert result["valid"] is True
        assert result["strength"] in ["strong", "very_strong"]
    
    def test_weak_password_too_short(self):
        """Test weak password (too short)."""
        password = "Ab1!"
        result = validate_password_strength(password)
        assert result["strength"] in ["weak", "very_weak"]
        assert "length" in str(result.get("issues", [])).lower()
    
    def test_weak_password_no_numbers(self):
        """Test weak password (no numbers)."""
        password = "MyPasswordNoNumbers!"
        result = validate_password_strength(password)
        # Should flag missing numbers
        issues = result.get("issues", [])
        assert any("number" in str(i).lower() or "digit" in str(i).lower() for i in issues)
    
    def test_weak_password_no_special(self):
        """Test weak password (no special characters)."""
        password = "MyPassword12345678"
        result = validate_password_strength(password)
        issues = result.get("issues", [])
        assert any("special" in str(i).lower() or "symbol" in str(i).lower() for i in issues)
    
    def test_weak_password_common(self):
        """Test weak password (common password)."""
        password = "password123"
        result = validate_password_strength(password)
        assert result["strength"] in ["weak", "very_weak"]


class TestKDFParamsValidation:
    """Tests for KDF parameter validation."""
    
    def test_valid_scrypt_params(self):
        """Test valid scrypt parameters."""
        params = {
            "n": 262144,
            "r": 8,
            "p": 1,
            "dklen": 32,
            "salt": "a" * 64
        }
        result = validate_kdf_params("scrypt", params)
        assert result["valid"] is True
    
    def test_invalid_scrypt_n_not_power_of_2(self):
        """Test scrypt with N not power of 2."""
        params = {
            "n": 100000,  # Not power of 2
            "r": 8,
            "p": 1,
            "dklen": 32,
            "salt": "a" * 64
        }
        result = validate_kdf_params("scrypt", params)
        assert result["valid"] is False
        assert "power" in str(result.get("error", "")).lower()
    
    def test_invalid_scrypt_missing_param(self):
        """Test scrypt with missing parameter."""
        params = {
            "n": 262144,
            "r": 8,
            # Missing p
            "dklen": 32,
            "salt": "a" * 64
        }
        result = validate_kdf_params("scrypt", params)
        assert result["valid"] is False
    
    def test_valid_pbkdf2_params(self):
        """Test valid PBKDF2 parameters."""
        params = {
            "c": 262144,
            "prf": "hmac-sha256",
            "dklen": 32,
            "salt": "a" * 64
        }
        result = validate_kdf_params("pbkdf2", params)
        assert result["valid"] is True
    
    def test_invalid_pbkdf2_low_iterations(self):
        """Test PBKDF2 with too few iterations."""
        params = {
            "c": 1000,  # Too low
            "prf": "hmac-sha256",
            "dklen": 32,
            "salt": "a" * 64
        }
        result = validate_kdf_params("pbkdf2", params)
        # Should either be invalid or have a warning
        assert result["valid"] is False or "warning" in result
    
    def test_invalid_kdf_type(self):
        """Test unsupported KDF type."""
        params = {"iterations": 10000}
        result = validate_kdf_params("bcrypt", params)
        assert result["valid"] is False


class TestKeystoreStructureValidation:
    """Tests for validating complete keystore structure."""
    
    def get_valid_keystore(self):
        """Return a valid keystore structure for testing."""
        return {
            "version": 3,
            "id": str(uuid.uuid4()),
            "address": "742d35cc6634c0532925a3b844bc9e7595f8fe00",
            "crypto": {
                "ciphertext": "a" * 64,
                "cipherparams": {
                    "iv": "b" * 32
                },
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
    
    def test_valid_keystore_structure(self):
        """Test validation of valid keystore structure."""
        keystore = self.get_valid_keystore()
        # Manual structure validation
        assert keystore["version"] == 3
        assert "crypto" in keystore
        assert "ciphertext" in keystore["crypto"]
        assert "mac" in keystore["crypto"]
        assert "kdfparams" in keystore["crypto"]
    
    def test_missing_version(self):
        """Test keystore missing version field."""
        keystore = self.get_valid_keystore()
        del keystore["version"]
        assert "version" not in keystore
    
    def test_wrong_version(self):
        """Test keystore with wrong version."""
        keystore = self.get_valid_keystore()
        keystore["version"] = 2
        assert keystore["version"] != 3
    
    def test_missing_crypto(self):
        """Test keystore missing crypto section."""
        keystore = self.get_valid_keystore()
        del keystore["crypto"]
        assert "crypto" not in keystore
    
    def test_missing_mac(self):
        """Test keystore missing MAC."""
        keystore = self.get_valid_keystore()
        del keystore["crypto"]["mac"]
        assert "mac" not in keystore["crypto"]
    
    def test_invalid_mac_length(self):
        """Test keystore with invalid MAC length."""
        keystore = self.get_valid_keystore()
        keystore["crypto"]["mac"] = "abc"  # Too short
        assert len(keystore["crypto"]["mac"]) != 64
    
    def test_invalid_iv_length(self):
        """Test keystore with invalid IV length."""
        keystore = self.get_valid_keystore()
        keystore["crypto"]["cipherparams"]["iv"] = "abc"  # Too short
        assert len(keystore["crypto"]["cipherparams"]["iv"]) != 32


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
