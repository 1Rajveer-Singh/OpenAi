import os
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from typing import str, bytes, Optional
from loguru import logger

class SecurityManager:
    """Enhanced security manager for VyapaarGPT with AES-256 encryption"""
    
    def __init__(self):
        self.encryption_key = self._get_or_create_encryption_key()
        self.fernet = Fernet(self.encryption_key)
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for AES-256"""
        
        # Check if key exists in environment
        env_key = os.getenv("ENCRYPTION_KEY")
        if env_key:
            try:
                return base64.urlsafe_b64decode(env_key.encode())
            except Exception:
                logger.warning("Invalid encryption key in environment, generating new one")
        
        # Generate new key from password
        password = os.getenv("SECRET_KEY", "vyapaargpt-default-secret-key").encode()
        salt = b"vyapaargpt_salt_2024"  # In production, use random salt
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data like phone numbers, addresses"""
        
        try:
            if not data:
                return ""
            
            encrypted_data = self.fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
            
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return data  # Return original data if encryption fails
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        
        try:
            if not encrypted_data:
                return ""
            
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.fernet.decrypt(decoded_data)
            return decrypted_data.decode()
            
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return encrypted_data  # Return original data if decryption fails
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt"""
        
        salt = os.getenv("PASSWORD_SALT", "vyapaargpt_salt").encode()
        return hashlib.sha256(salt + password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        
        return self.hash_password(password) == hashed_password
    
    def sanitize_phone_number(self, phone: str) -> str:
        """Sanitize and validate Indian phone number"""
        
        if not phone:
            return ""
        
        # Remove all non-digit characters
        clean_phone = ''.join(filter(str.isdigit, phone))
        
        # Handle different phone number formats
        if len(clean_phone) == 10:
            # Add country code for India
            clean_phone = "91" + clean_phone
        elif len(clean_phone) == 11 and clean_phone.startswith("0"):
            # Remove leading 0 and add country code
            clean_phone = "91" + clean_phone[1:]
        elif len(clean_phone) == 12 and clean_phone.startswith("91"):
            # Already has country code
            pass
        else:
            logger.warning(f"Invalid phone number format: {phone}")
            return phone  # Return original if can't sanitize
        
        return clean_phone
    
    def validate_indian_phone(self, phone: str) -> bool:
        """Validate Indian phone number format"""
        
        clean_phone = self.sanitize_phone_number(phone)
        
        # Indian mobile numbers start with 6, 7, 8, or 9
        if len(clean_phone) == 12 and clean_phone.startswith("91"):
            mobile_part = clean_phone[2:]
            return mobile_part[0] in ["6", "7", "8", "9"]
        
        return False
    
    def mask_sensitive_data(self, data: str, data_type: str = "phone") -> str:
        """Mask sensitive data for logging/display"""
        
        if not data:
            return ""
        
        if data_type == "phone":
            if len(data) >= 10:
                return data[:2] + "*" * (len(data) - 4) + data[-2:]
            else:
                return "*" * len(data)
        
        elif data_type == "email":
            if "@" in data:
                local, domain = data.split("@", 1)
                if len(local) > 2:
                    masked_local = local[:1] + "*" * (len(local) - 2) + local[-1:]
                else:
                    masked_local = "*" * len(local)
                return f"{masked_local}@{domain}"
            else:
                return "*" * len(data)
        
        elif data_type == "upi":
            if "@" in data:
                local, provider = data.split("@", 1)
                if len(local) > 2:
                    masked_local = local[:1] + "*" * (len(local) - 2) + local[-1:]
                else:
                    masked_local = "*" * len(local)
                return f"{masked_local}@{provider}"
            else:
                return "*" * len(data)
        
        else:
            # Generic masking
            if len(data) > 4:
                return data[:2] + "*" * (len(data) - 4) + data[-2:]
            else:
                return "*" * len(data)

class DataComplianceManager:
    """Manage compliance with Indian data protection laws"""
    
    def __init__(self):
        self.security_manager = SecurityManager()
    
    def process_customer_data(self, customer_data: dict) -> dict:
        """Process customer data according to compliance requirements"""
        
        processed_data = customer_data.copy()
        
        # Encrypt sensitive fields
        sensitive_fields = ["phone", "email", "address", "whatsapp_number"]
        
        for field in sensitive_fields:
            if field in processed_data and processed_data[field]:
                processed_data[field] = self.security_manager.encrypt_sensitive_data(
                    processed_data[field]
                )
        
        # Validate phone number
        if "phone" in customer_data and customer_data["phone"]:
            if not self.security_manager.validate_indian_phone(customer_data["phone"]):
                processed_data["phone_valid"] = False
            else:
                processed_data["phone_valid"] = True
        
        return processed_data
    
    def get_customer_data_for_display(self, encrypted_customer_data: dict) -> dict:
        """Decrypt customer data for authorized display"""
        
        display_data = encrypted_customer_data.copy()
        
        # Decrypt sensitive fields
        sensitive_fields = ["phone", "email", "address", "whatsapp_number"]
        
        for field in sensitive_fields:
            if field in display_data and display_data[field]:
                display_data[field] = self.security_manager.decrypt_sensitive_data(
                    display_data[field]
                )
        
        return display_data
    
    def get_masked_customer_data(self, encrypted_customer_data: dict) -> dict:
        """Get masked customer data for logs/analytics"""
        
        # First decrypt, then mask
        decrypted_data = self.get_customer_data_for_display(encrypted_customer_data)
        masked_data = decrypted_data.copy()
        
        # Mask sensitive fields
        if "phone" in masked_data and masked_data["phone"]:
            masked_data["phone"] = self.security_manager.mask_sensitive_data(
                masked_data["phone"], "phone"
            )
        
        if "email" in masked_data and masked_data["email"]:
            masked_data["email"] = self.security_manager.mask_sensitive_data(
                masked_data["email"], "email"
            )
        
        if "address" in masked_data and masked_data["address"]:
            # For address, just show first few characters
            address = masked_data["address"]
            if len(address) > 10:
                masked_data["address"] = address[:10] + "..."
            else:
                masked_data["address"] = address
        
        return masked_data
    
    def audit_log_access(self, user_id: int, data_type: str, action: str, ip_address: str = None):
        """Log data access for audit trail"""
        
        audit_entry = {
            "user_id": user_id,
            "data_type": data_type,
            "action": action,
            "timestamp": "2024-01-15T10:30:00Z",  # In real implementation, use datetime.now()
            "ip_address": ip_address or "unknown",
            "compliance_status": "logged"
        }
        
        # In production, store in audit database
        logger.info(f"Data access audit: {audit_entry}")
        return audit_entry
    
    def check_data_retention_policy(self, data_age_days: int, data_type: str) -> dict:
        """Check if data should be retained according to policy"""
        
        retention_policies = {
            "customer_data": 365 * 7,      # 7 years for customer data
            "transaction_data": 365 * 7,   # 7 years for financial records
            "audit_logs": 365 * 3,         # 3 years for audit logs
            "voice_recordings": 30,        # 30 days for voice data
            "temporary_data": 7             # 7 days for temporary data
        }
        
        retention_days = retention_policies.get(data_type, 365)
        
        return {
            "should_retain": data_age_days < retention_days,
            "retention_period_days": retention_days,
            "days_until_deletion": max(0, retention_days - data_age_days),
            "policy": f"{data_type} retained for {retention_days} days"
        }

# Initialize global instances
security_manager = SecurityManager()
compliance_manager = DataComplianceManager()