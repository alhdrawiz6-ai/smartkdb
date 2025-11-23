import os
import json
import struct
from typing import Dict, Any, Optional

class BlockStorage:
    """
    Append-only block storage for database records.
    
    Each record is stored as:
    - 1 byte status (0=Active, 1=Deleted)
    - 4 bytes length (unsigned long, little-endian)
    - N bytes JSON data
    
    Format: "<BL" = little-endian, 1 byte + 4 bytes unsigned long
    """
    
    def __init__(self, path: str):
        """
        Initialize block storage.
        
        Args:
            path: Path to the storage file
        """
        self.path = path
        if not os.path.exists(path):
            with open(path, "wb") as f:
                pass

    def write_record(self, data: Dict[str, Any]) -> int:
        """
        Write a record to the end of the file.
        
        Args:
            data: Record data as dictionary
            
        Returns:
            Offset (address) of the written record
        """
        serialized = json.dumps(data).encode("utf-8")
        length = len(serialized)
        
        with open(self.path, "ab") as f:
            offset = f.tell()
            # Header: 1 byte status + 4 bytes length
            # Format: <BL = little-endian, unsigned char (1) + unsigned long (4)
            header = struct.pack("<BL", 0, length)
            f.write(header)
            f.write(serialized)
            
        return offset

    def read_record(self, offset: int) -> Optional[Dict[str, Any]]:
        """
        Read a record at the given offset.
        
        Args:
            offset: Byte offset in the file
            
        Returns:
            Record data as dictionary, or None if not found/deleted
        """
        if offset < 0:
            return None

        try:
            with open(self.path, "rb") as f:
                f.seek(offset)
                header = f.read(5)
                
                # Check if we read enough bytes
                if len(header) < 5:
                    return None
                
                # Unpack: 1 byte status + 4 bytes length
                status, length = struct.unpack("<BL", header)
                
                if status == 1:  # Deleted
                    return None
                
                data_bytes = f.read(length)
                
                # Check if we read the complete data
                if len(data_bytes) < length:
                    return None
                    
                return json.loads(data_bytes.decode("utf-8"))
                
        except (IOError, json.JSONDecodeError, struct.error):
            return None

    def mark_deleted(self, offset: int) -> None:
        """
        Mark a record as deleted.
        
        Args:
            offset: Byte offset of the record to delete
        """
        try:
            with open(self.path, "r+b") as f:
                f.seek(offset)
                # Status 1 = Deleted (only first byte)
                f.write(struct.pack("B", 1))
        except IOError:
            pass  # File might not exist or be accessible


