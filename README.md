# 📖 Story Image Generator - Công cụ Tạo Ảnh Câu Chuyện Hàng Loạt

## 🎯 Mô tả
Tool tự động tạo một loạt hình ảnh câu chuyện từ ảnh bìa đơn giản. Chỉ cần upload ảnh bìa, hệ thống sẽ:
- 🤖 Phân tích ảnh bìa để hiểu yêu cầu câu chuyện
- 🎨 Tạo prompt câu chuyện chi tiết
- 🖼️ Sinh ra các ảnh liên tiếp theo hành trình câu chuyện
- 👥 Đồng bộ nhân vật qua tất cả các ảnh
- 📚 Tạo hoàn chỉnh từ đầu đến kết thúc

## 🚀 Tính năng Chính

### 1. **Upload & Phân tích Ảnh Bìa**
- Nhận dạng chủ đề, nhân vật, phong cách nghệ thuật
- Trích xuất thông tin màu sắc, môi trường, tâm trạng

### 2. **AI Story Generation**
- Tạo câu chuyện hoàn chỉnh (5-10 cảnh)
- Mỗi cảnh có mô tả chi tiết cho việc tạo ảnh
- Đảm bảo tính nhất quán trong câu chuyện

### 3. **Character Consistency Engine**
- Nhận dạng và mô tả nhân vật chính
- Duy trì đặc điểm nhân vật qua tất cả ảnh
- Sử dụng Face Encoding để đồng bộ hóa

### 4. **Batch Image Generation**
- Tạo tất cả ảnh song song
- Tối ưu hóa thời gian xử lý
- Quản lý queue tác vụ

### 5. **Quality & Export**
- Kiểm tra tính nhất quán giữa các ảnh
- Xuất video/slideshow hoàn chỉnh
- Lưu trữ metadata câu chuyện

## 📋 Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** - Web framework
- **Anthropic Claude API** - Story generation
- **OpenAI DALL-E 3** - Image generation
- **Google Vision API** - Image analysis
- **DeepFace/FaceNet** - Face consistency
- **Celery** - Async task queue
- **Redis** - Cache & queue backend
- **PostgreSQL** - Database

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **Shadcn/ui** - UI components
- **Zustand** - State management
- **React Query** - Data fetching

## 🔄 Quy Trình Hoạt Động

```
1. Upload Ảnh Bìa
        ↓
2. Phân Tích Ảnh (Vision AI)
        ↓
3. Tạo Mô Tả Nhân Vật & Thế Giới
        ↓
4. Sinh Câu Chuyện (Claude AI)
        ↓
5. Phân Chia thành Cảnh (Scenes)
        ↓
6. Tạo Prompt Chi Tiết cho Mỗi Ảnh
        ↓
7. Sinh Ảnh Batch (DALL-E 3)
        ↓
8. Kiểm Tra Tính Nhất Quán Nhân Vật
        ↓
9. Xuất Video/Slideshow
        ↓
10. Lưu Metadata & Lịch Sử
```

## 🛠️ Cài Đặt

### Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Node.js 18+
- API Keys: OpenAI, Anthropic, Google Cloud Vision

### Cài Đặt Nhanh

```bash
git clone https://github.com/phanquoctai/story-image-generator.git
cd story-image-generator
cp .env.example .env
docker-compose up -d
```

## 📝 License

MIT