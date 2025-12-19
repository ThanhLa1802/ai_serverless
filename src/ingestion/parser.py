from langchain_community.document_loaders import PyPDFLoader
import tempfile
import os

class PDFParser:
    def __init__(self):
        pass

    def parse_from_bytes(self, file_bytes: bytes):
        """
        Lambda nhận file qua API thường ở dạng bytes. 
        Chúng ta cần lưu tạm vào /tmp (thư mục ghi được của Lambda) để Loader đọc.
        """
        # 1. Tạo file tạm trong môi trường Lambda
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file_bytes)
            temp_path = temp_file.name

        try:
            # 2. Sử dụng LangChain PyPDFLoader
            loader = PyPDFLoader(temp_path)
            
            # 3. Load nội dung thành danh sách các đối tượng Document
            # Mỗi trang PDF sẽ là một Document
            documents = loader.load()
            
            return documents
        finally:
            # 4. Dọn dẹp file tạm sau khi đã load xong
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def parse_from_path(self, file_path: str):
        """Dành cho việc chạy test local hoặc quét folder S3"""
        loader = PyPDFLoader(file_path)
        return loader.load()