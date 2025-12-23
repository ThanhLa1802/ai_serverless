# Sử dụng Python 3.12 - Image này có môi trường hiện đại hơn và GCC mới hơn
FROM public.ecr.aws/lambda/python:3.12

# Cài đặt công cụ hệ thống cần thiết
RUN dnf install -y gcc-c++

COPY requirements.txt .

# Nâng cấp pip và cài đặt wheel trước để ưu tiên cài bản binary
RUN pip install --upgrade pip setuptools wheel

# Cài đặt requirements
RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

COPY src/ ${LAMBDA_TASK_ROOT}/src/
# Optional: embed version for debug
ARG IMAGE_TAG=dev
ENV IMAGE_TAG=${IMAGE_TAG}

ENV PYTHONPATH=${LAMBDA_TASK_ROOT}

CMD [ "src.retrieval.handler.handler" ]