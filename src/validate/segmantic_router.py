import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pypdf import PdfReader

app = FastAPI(title="Semantic Router cho RAG Pipeline")

# Khởi tạo LLM gác cổng (dùng model nhỏ, rẻ, chạy nhanh)
# Đặt temperature = 0 để model trả lời dứt khoát, không sáng tạo
llm_router = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Xây dựng Prompt phân loại
# Nhấn mạnh chuyên môn hệ thống để mô hình nhận diện chính xác
router_prompt = ChatPromptTemplate.from_messages([
    ("system", """Bạn là một chuyên gia kiểm duyệt tài liệu tự động. 
Hệ thống AI Chatbot này CHỈ phục vụ mảng Công nghệ thông tin, Software Engineering, Data Engineering, Cloud (AWS) và AI.
Nhiệm vụ của bạn là đọc đoạn trích tài liệu dưới đây và xác định xem tài liệu có đúng chuyên môn hay không.
- Nếu CÓ liên quan đến chuyên môn hệ thống: Trả lời 'YES'
- Nếu KHÔNG liên quan (ví dụ: thực đơn, tiểu thuyết tình cảm, hóa đơn mua hàng...): Trả lời 'NO'
Chỉ trả về ĐÚNG MỘT TỪ 'YES' hoặc 'NO', tuyệt đối không giải thích thêm."""),
    ("human", "Đoạn trích tài liệu:\n{snippet}")
])

# Tạo chuỗi thực thi
router_chain = router_prompt | llm_router

def extract_text_snippet(file_bytes: bytes, max_chars: int = 1500) -> str:
    """Hàm phụ trợ trích xuất một đoạn text ngắn từ file PDF để LLM đánh giá"""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
            if len(text) > max_chars:
                break
        return text[:max_chars]
    except Exception as e:
        raise ValueError(f"Không thể đọc nội dung file PDF: {str(e)}")

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    # 1. Kiểm tra định dạng thô (Lớp 1)
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Hệ thống hiện chỉ hỗ trợ file PDF.")
    
    # Đọc file vào bộ nhớ
    file_bytes = await file.read()
    
    try:
        # 2. Trích xuất khoảng 1500 ký tự đầu tiên
        snippet = extract_text_snippet(file_bytes)
        
        if len(snippet.strip()) < 50:
             raise HTTPException(status_code=400, detail="File PDF quá ngắn hoặc chứa toàn hình ảnh.")
             
        # 3. GỌI LLM ROUTER ĐỂ KIỂM DUYỆT (Lớp 3)
        print("Đang nhờ LLM kiểm duyệt nội dung...")
        response = await router_chain.ainvoke({"snippet": snippet})
        decision = response.content.strip().upper()
        
        # 4. Ra quyết định
        if "YES" not in decision:
            raise HTTPException(
                status_code=406, 
                detail="Từ chối: Tài liệu không thuộc chuyên môn IT, Data hoặc Cloud."
            )
            
        
        return {
            "status": "success", 
            "message": "Tài liệu hợp lệ. Đã đưa vào hàng đợi xử lý RAG.",
            "file_name": file.filename
        }
        
    except ValueError as ve:
         raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý hệ thống: {str(e)}")