import os
import logging
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from flask import Flask
from flask_talisman import Talisman
import dash_auth

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def setup_authentication(app):
    """
    Set up basic authentication for the dashboard.
    
    For demonstration, we're using a simple username/password pair.
    In production, integrate with an enterprise identity provider (e.g., OIDC, SAML)
    and securely manage credentials using environment variables.
    """
    # Retrieve credentials from environment variables (with defaults for demo purposes)
    USERNAME = os.getenv("DASHBOARD_USER", "admin")
    PASSWORD = os.getenv("DASHBOARD_PASSWORD", "supersecret")
    
    VALID_USERNAME_PASSWORD_PAIRS = {USERNAME: PASSWORD}
    auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
    logging.info("Basic Authentication has been configured for the dashboard.")
    return auth

def enforce_https(app):
    """
    Enforce HTTPS for the app using Flask-Talisman.
    
    Flask-Talisman sets security headers (e.g., HSTS) and forces HTTPS.
    This is critical when deploying web applications in production.
    
    Args:
        app: The Dash/Flask application instance.
    
    Returns:
        The Talisman instance wrapping the app.
    """
    talisman = Talisman(app, force_https=True)
    logging.info("HTTPS enforcement via Flask-Talisman has been applied.")
    return talisman

def generate_encryption_key():
    """
    Generate a new AES-256-GCM key (32 bytes).
    
    IMPORTANT:
        The generated key must be stored securely (e.g., in an environment variable,
        a secure key management system, or a hardware security module).
    
    Returns:
        bytes: A 32-byte key for AES-256-GCM.
    """
    key = os.urandom(32)  # 32 bytes = 256 bits for AES-256
    logging.info("New AES-256-GCM key generated. Store this key securely!")
    return key

def encrypt_data(data, key):
    """
    Encrypt sensitive data using AES-256-GCM.
    
    Args:
        data (bytes): The plaintext data to encrypt.
        key (bytes): A 32-byte AES-256-GCM key.
    
    Returns:
        tuple: A tuple containing (nonce, ciphertext).
            - nonce (bytes): A 12-byte nonce generated for this encryption.
            - ciphertext (bytes): The encrypted data including the authentication tag.
    
    Note:
        - AES-GCM requires a unique nonce for each encryption operation.
        - The nonce must be stored alongside the ciphertext for decryption.
    """
    # Initialize AESGCM with the provided key
    aesgcm = AESGCM(key)
    # Generate a 12-byte nonce (96 bits) for AES-GCM, which is the recommended size
    nonce = os.urandom(12)
    # Encrypt the data; additional authenticated data (AAD) is set to None
    ciphertext = aesgcm.encrypt(nonce, data, None)
    logging.info("Data encryption completed using AES-256-GCM.")
    return nonce, ciphertext

def decrypt_data(nonce, ciphertext, key):
    """
    Decrypt data that was encrypted using AES-256-GCM.
    
    Args:
        nonce (bytes): The nonce used during encryption.
        ciphertext (bytes): The encrypted data including the authentication tag.
        key (bytes): The 32-byte AES-256-GCM key.
    
    Returns:
        bytes: The decrypted (plaintext) data.
    
    Raises:
        Exception: If decryption fails (e.g., due to an invalid key or corrupted data).
    """
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    logging.info("Data decryption completed using AES-256-GCM.")
    return plaintext

def apply_security_measures(app=None):
    """
    Apply multiple security measures.
    
    Args:
        app: Optional Dash/Flask application instance. If provided, 
             it will be wrapped with HTTPS enforcement and basic authentication.
             
    Returns:
        dict: A dictionary containing security configurations such as the app's auth settings and encryption key.
    
    Notes:
        In production, further measures should be applied:
            • Encrypting data at rest (handled by the storage system).
            • Regular vulnerability scanning and patch management.
            • Secure logging practices (avoid logging sensitive information).
            • Implementing robust access controls, RBAC, and MFA for administrative interfaces.
    """
    security_config = {}

    if app:
        # Enforce HTTPS and set security headers
        security_config["talisman"] = enforce_https(app)
        # Set up basic authentication for the dashboard
        security_config["auth"] = setup_authentication(app)
        logging.info("Security measures applied to the app.")
    else:
        logging.info("No app instance provided; ensure you apply HTTPS, authentication, and other security measures at deployment.")

    # Manage the encryption key securely:
    # Try to load the key from an environment variable. If not found, generate a new key.
    key = os.getenv("ENCRYPTION_KEY")
    if key:
        # Convert from string (if stored as hex/base64) to bytes if necessary.
        key = key.encode() if isinstance(key, str) else key
    else:
        key = generate_encryption_key()
        # WARNING: In production, do not log sensitive keys.
        logging.info("Generated encryption key: %s", key.hex())
    security_config["encryption_key"] = key

    return security_config

# Example usage of the security functions
if __name__ == "__main__":
    # For demonstration, create a dummy Dash app instance
    from dash import Dash
    app = Dash(__name__)
    
    # Apply security measures (authentication, HTTPS, encryption key generation)
    security_settings = apply_security_measures(app)
    
    # Demonstrate encryption and decryption using AES-256-GCM
    sample_data = b"Sensitive cybersecurity data"
    key = security_settings["encryption_key"]
    nonce, encrypted = encrypt_data(sample_data, key)
    logging.info("Encrypted Data (nonce + ciphertext): %s, %s", nonce.hex(), encrypted.hex())
    
    # Decrypt the data back to plaintext
    decrypted = decrypt_data(nonce, encrypted, key)
    logging.info("Decrypted Data: %s", decrypted)
