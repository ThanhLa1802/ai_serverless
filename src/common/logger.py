import logging
import sys
import os

def get_logger(name: str):
    """
    Khởi tạo logger chuẩn cho toàn bộ dự án.
    :param name: Tên của module gọi logger (thường truyền __name__)
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        logger.setLevel(log_level)

        # Định dạng log: Thời gian - Tên Module - Mức độ - Nội dung
        # AWS Lambda sẽ tự thêm RequestID vào CloudWatch, nhưng ta có thể custom thêm
        formatter = logging.Formatter(
            '[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(name)s\t%(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S'
        )

        # Output ra stdout để CloudWatch Logs thu thập
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger