import os
import tempfile
import platform # Thêm thư viện này để kiểm tra OS
from langchain_community.document_loaders import PyPDFLoader
from src.common.logger import get_logger

_logger = get_logger(__name__)

class PDFParser:
    def parse_from_bytes(self, file_bytes: bytes):
        temp_path = None
        try:
            # Tự động xác định thư mục tạm: 
            # Trên Lambda sẽ là /tmp, trên Windows sẽ là thư mục Temp của hệ thống
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(file_bytes)
                temp_path = temp_file.name
            
            _logger.info(f"Đã tạo file tạm tại: {temp_path}")
            
            # Kiểm tra file có tồn tại và có dữ liệu không
            if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
                raise FileNotFoundError(f"Không thể tạo file tạm hoặc file rỗng: {temp_path}")

            loader = PyPDFLoader(temp_path)
            documents = loader.load()
            
            _logger.info(f"PyPDFLoader hoàn tất. Số trang trích xuất: {len(documents)}")
            return documents
            
        except Exception as e:
            _logger.error(f"Lỗi trong PDFParser: {str(e)}", exc_info=True)
            raise e
        finally:
            # Quan trọng: Trên Windows, đôi khi PyPDFLoader vẫn giữ file (lock) 
            # nên cần đặt trong try-except khi xóa
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                    _logger.info("Đã xóa file tạm.")
                except Exception as del_e:
                    _logger.warning(f"Không thể xóa file tạm: {del_e}")