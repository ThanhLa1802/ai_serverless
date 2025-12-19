# Sử dụng Base Image chính thức từ AWS cho Python 3.9
FROM public.ecr.aws/lambda/python:3.11

# Cài đặt các công cụ hệ thống cần thiết (nếu có thư viện nào cần compile)
RUN yum install -y gcc-c++

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào thư mục root của Lambda (${LAMBDA_TASK_ROOT})
COPY src/ ${LAMBDA_TASK_ROOT}/src/

# Thiết lập biến môi trường PYTHONPATH để Python có thể import từ thư mục /src
ENV PYTHONPATH=${LAMBDA_TASK_ROOT}

CMD [ "src.retrieval.handler.handler" ]