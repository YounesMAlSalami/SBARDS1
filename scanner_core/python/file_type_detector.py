import os
import magic
import mimetypes
import logging
import binascii
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("FileTypeDetector")

class FileTypeDetector:
    """
    Detects file types using multiple methods:
    1. File extension
    2. Magic numbers (file signatures)
    3. MIME type detection
    4. Content analysis
    """

    def __init__(self):
        """Initialize the file type detector"""
        try:
            self.mime = magic.Magic(mime=True)
            self.magic_available = True
        except Exception as e:
            logger.warning(f"Could not initialize python-magic: {e}")
            self.magic_available = False

        mimetypes.init()

        # Initialize common file signatures
        self.signatures = {
            b"\x4D\x5A": "application/x-dosexec",  # MZ header (Windows executable)
            b"\x7F\x45\x4C\x46": "application/x-elf",  # ELF header (Linux executable)
            b"\x50\x4B\x03\x04": "application/zip",  # ZIP archive
            b"\x25\x50\x44\x46": "application/pdf",  # PDF document
            b"\xFF\xD8\xFF": "image/jpeg",  # JPEG image
            b"\x89\x50\x4E\x47": "image/png",  # PNG image
            b"\x47\x49\x46\x38": "image/gif",  # GIF image
            b"\x52\x61\x72\x21": "application/x-rar-compressed",  # RAR archive
            b"\x1F\x8B\x08": "application/gzip",  # GZIP archive
            b"\x42\x5A\x68": "application/x-bzip2",  # BZIP2 archive
            b"\x37\x7A\xBC\xAF\x27\x1C": "application/x-7z-compressed",  # 7-Zip archive
            b"\xD0\xCF\x11\xE0": "application/msoffice",  # MS Office document
            b"\x75\x73\x74\x61\x72": "application/x-tar",  # TAR archive
            b"\x23\x21": "text/script",  # Shell script
            b"\x3C\x3F\x78\x6D\x6C": "application/xml",  # XML document
            b"\x3C\x68\x74\x6D\x6C": "text/html",  # HTML document
            b"\x3C\x21\x44\x4F\x43\x54\x59\x50\x45": "text/html",  # HTML document
            b"\x49\x44\x33": "audio/mpeg",  # MP3 audio
            b"\x66\x74\x79\x70": "video/mp4",  # MP4 video
            b"\x52\x49\x46\x46": "audio/wav",  # WAV audio
        }

        # Map file extensions to categories
        self.extension_categories = {
            # Executables
            ".exe": "executable",
            ".dll": "executable",
            ".sys": "executable",
            ".bat": "script",
            ".cmd": "script",
            ".ps1": "script",
            ".vbs": "script",
            ".js": "script",
            ".wsf": "script",
            ".hta": "script",
            ".msi": "installer",

            # Documents
            ".pdf": "document",
            ".doc": "document",
            ".docx": "document",
            ".xls": "document",
            ".xlsx": "document",
            ".ppt": "document",
            ".pptx": "document",
            ".txt": "document",
            ".rtf": "document",
            ".csv": "document",

            # Archives
            ".zip": "archive",
            ".rar": "archive",
            ".7z": "archive",
            ".tar": "archive",
            ".gz": "archive",
            ".bz2": "archive",
            ".iso": "archive",

            # Multimedia
            ".jpg": "image",
            ".jpeg": "image",
            ".png": "image",
            ".gif": "image",
            ".bmp": "image",
            ".mp3": "audio",
            ".wav": "audio",
            ".flac": "audio",
            ".mp4": "video",
            ".avi": "video",
            ".mkv": "video",

            # Programming
            ".py": "code",
            ".c": "code",
            ".cpp": "code",
            ".h": "code",
            ".java": "code",
            ".php": "code",
            ".html": "code",
            ".css": "code",
            ".sql": "code",

            # Certificates
            ".pem": "certificate",
            ".crt": "certificate",
            ".key": "certificate",
            ".p12": "certificate",
            ".pfx": "certificate",
        }

    def detect_file_type(self, file_path: str) -> Dict[str, Any]:
        """
        Detect the type of a file using multiple methods

        Args:
            file_path: Path to the file to analyze

        Returns:
            Dictionary with file type information
        """
        if not os.path.exists(file_path):
            logger.warning(f"File does not exist: {file_path}")
            return {
                "file_path": file_path,
                "exists": False,
                "mime_type": "unknown",
                "category": "unknown",
                "extension": "unknown",
                "is_binary": False,
                "is_executable": False,
                "is_archive": False,
                "is_document": False,
                "is_multimedia": False,
                "is_code": False,
                "is_certificate": False
            }

        # Get file extension
        _, extension = os.path.splitext(file_path)
        extension = extension.lower()

        # Get MIME type
        mime_type = "application/octet-stream"  # Default MIME type
        if self.magic_available:
            try:
                mime_type = self.mime.from_file(file_path)
            except Exception as e:
                logger.warning(f"Error detecting MIME type for {file_path}: {e}")
                # Try using mimetypes as fallback
                mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        else:
            # Use mimetypes as fallback if magic is not available
            mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
            logger.info(f"Using mimetypes fallback for {file_path}: {mime_type}")

        # Check file signature
        signature_type = self._check_file_signature(file_path)

        # Determine if file is binary
        is_binary = self._is_binary_file(file_path)

        # Get category from extension
        category = self.extension_categories.get(extension, "unknown")

        # If category is still unknown, try to determine from MIME type or signature
        if category == "unknown":
            # Try to determine category from signature
            if signature_type:
                if "executable" in signature_type:
                    category = "executable"
                elif "zip" in signature_type or "archive" in signature_type or "compressed" in signature_type:
                    category = "archive"
                elif "pdf" in signature_type or "msoffice" in signature_type:
                    category = "document"
                elif "image" in signature_type or "audio" in signature_type or "video" in signature_type:
                    category = "multimedia"
                elif "xml" in signature_type or "html" in signature_type:
                    category = "code"

            # If still unknown, try to determine from MIME type
            if category == "unknown" and mime_type != "application/octet-stream":
                mime_category = mime_type.split('/')[0]
                if mime_category == "application":
                    sub_type = mime_type.split('/')[1]
                    if "executable" in sub_type or sub_type in ["x-dosexec", "x-msdownload", "x-elf"]:
                        category = "executable"
                    elif "archive" in sub_type or "zip" in sub_type or "compressed" in sub_type or sub_type in ["x-tar", "x-gzip", "x-bzip2", "x-7z-compressed", "x-rar-compressed"]:
                        category = "archive"
                    elif "document" in sub_type or sub_type in ["pdf", "msword", "vnd.ms-excel", "vnd.ms-powerpoint", "rtf", "vnd.openxmlformats-officedocument"]:
                        category = "document"
                    elif "script" in sub_type or "code" in sub_type or sub_type in ["javascript", "json", "xml", "html"]:
                        category = "code"
                elif mime_category in ["image", "audio", "video"]:
                    category = "multimedia"
                elif mime_category == "text":
                    if mime_type in ["text/html", "text/xml", "text/css", "text/javascript"]:
                        category = "code"
                    else:
                        category = "document"

            # If still unknown but is a text file, categorize as document
            if category == "unknown" and not is_binary:
                category = "document"

            # Last resort: use file extension to guess category
            if category == "unknown" and extension:
                # Common text file extensions
                if extension in [".txt", ".log", ".md", ".csv", ".ini", ".conf", ".cfg"]:
                    category = "document"
                # Common code file extensions not already covered
                elif extension in [".py", ".java", ".c", ".cpp", ".h", ".cs", ".php", ".rb", ".go", ".swift", ".kt", ".ts"]:
                    category = "code"

        # Determine specific file types
        is_executable = category == "executable" or category == "script" or "executable" in mime_type
        is_archive = category == "archive" or "archive" in mime_type or "compressed" in mime_type
        is_document = category == "document" or "document" in mime_type or "text" in mime_type
        is_multimedia = category == "image" or category == "audio" or category == "video" or "image" in mime_type or "audio" in mime_type or "video" in mime_type
        is_code = category == "code" or "code" in mime_type or mime_type in ["text/html", "text/xml", "text/css", "text/javascript", "application/javascript", "application/json"]
        is_certificate = category == "certificate" or "certificate" in mime_type

        # Get file size
        try:
            file_size = os.path.getsize(file_path)
        except Exception as e:
            logger.warning(f"Error getting file size for {file_path}: {e}")
            file_size = 0

        # Calculate file hash (first 4KB only for performance)
        file_hash = ""
        try:
            with open(file_path, "rb") as f:
                content = f.read(4096)
                import hashlib
                file_hash = hashlib.md5(content).hexdigest()
        except Exception as e:
            logger.warning(f"Error calculating hash for {file_path}: {e}")

        # Create comprehensive result
        result = {
            "file_path": file_path,
            "exists": True,
            "mime_type": mime_type,
            "signature_type": signature_type,
            "category": category,
            "extension": extension,
            "file_size": file_size,
            "partial_hash": file_hash,
            "is_binary": is_binary,
            "is_executable": is_executable,
            "is_archive": is_archive,
            "is_document": is_document,
            "is_multimedia": is_multimedia,
            "is_code": is_code,
            "is_certificate": is_certificate
        }

        logger.debug(f"File type detection result for {file_path}: {category} ({mime_type})")
        return result

    def _check_file_signature(self, file_path: str) -> Optional[str]:
        """Check file signature (magic numbers) to determine file type"""
        try:
            with open(file_path, "rb") as f:
                file_start = f.read(16)  # Read first 16 bytes

                for signature, file_type in self.signatures.items():
                    if file_start.startswith(signature):
                        return file_type

                return None
        except Exception as e:
            logger.warning(f"Error checking file signature for {file_path}: {e}")
            return None

    def _is_binary_file(self, file_path: str) -> bool:
        """
        Determine if a file is binary by checking for null bytes and other binary indicators

        This is a more comprehensive check than just looking for null bytes.
        """
        try:
            # Check file size first - if it's too large, sample it
            file_size = os.path.getsize(file_path)

            # For very small files, read the whole thing
            if file_size < 1024:
                read_size = file_size
            else:
                # For larger files, read chunks from the beginning, middle, and end
                read_size = min(4096, file_size // 3)

            with open(file_path, "rb") as f:
                # Check beginning of file
                beginning = f.read(read_size)
                if b"\x00" in beginning:
                    return True

                # If file is large enough, check middle and end
                if file_size > read_size * 3:
                    f.seek(file_size // 2)
                    middle = f.read(read_size)
                    if b"\x00" in middle:
                        return True

                    f.seek(max(0, file_size - read_size))
                    end = f.read(read_size)
                    if b"\x00" in end:
                        return True

                # If no null bytes found, check for high concentration of non-printable characters
                # in the beginning of the file (which is most likely to contain headers)
                non_printable_count = sum(1 for b in beginning if b < 32 and b not in (9, 10, 13))  # Tab, LF, CR are printable
                if non_printable_count > len(beginning) * 0.3:  # If more than 30% is non-printable
                    return True

            return False
        except Exception as e:
            logger.warning(f"Error checking if file is binary for {file_path}: {e}")
            return False

    def get_detailed_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get detailed information about a file, including type detection and additional metadata

        Args:
            file_path: Path to the file to analyze

        Returns:
            Dictionary with detailed file information
        """
        # Get basic file type information
        file_info = self.detect_file_type(file_path)

        # Add additional file metadata
        try:
            stat_info = os.stat(file_path)
            file_info["created_time"] = stat_info.st_ctime
            file_info["modified_time"] = stat_info.st_mtime
            file_info["accessed_time"] = stat_info.st_atime
            file_info["permissions"] = stat_info.st_mode
            file_info["owner"] = stat_info.st_uid
            file_info["group"] = stat_info.st_gid
        except Exception as e:
            logger.warning(f"Error getting file metadata for {file_path}: {e}")

        return file_info
