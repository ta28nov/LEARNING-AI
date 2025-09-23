# 🗄️ Database Scripts - AI Learning Platform

Tập hợp các script để setup, quản lý và tối ưu hóa MongoDB database cho AI Learning Platform.

## 📋 Tổng quan Scripts

| Script | Mục đích | Sử dụng khi |
|--------|----------|-------------|
| `run_all.sh` | **Setup hoàn chỉnh** | Lần đầu setup hệ thống |
| `init_database.py` | **Khởi tạo database** | Tạo collections, indexes, sample data |
| `vector_chunking.py` | **Xử lý vector embeddings** | Setup vector search, chunking content |
| `atlas_setup.py` | **MongoDB Atlas setup** | Deploy production lên Atlas |
| `optimize_database.py` | **Tối ưu hóa performance** | Maintenance định kỳ |

## 🚀 Quick Start

### 1. Setup hoàn chỉnh (Recommended)

```bash
# Cấp quyền thực thi
chmod +x scripts/run_all.sh

# Chạy setup hoàn chỉnh
./scripts/run_all.sh
```

### 2. Setup từng bước

```bash
# Bước 1: Khởi tạo database
python3 scripts/init_database.py

# Bước 2: Xử lý vector embeddings
python3 scripts/vector_chunking.py

# Bước 3: Tối ưu hóa (optional)
python3 scripts/optimize_database.py
```

## 🔧 Chi tiết từng Script

### 📜 `run_all.sh` - Complete Setup

**Mục đích:** Setup hoàn chỉnh database từ A-Z

**Tính năng:**
- ✅ Kiểm tra Python environment
- ✅ Tạo virtual environment
- ✅ Cài đặt dependencies
- ✅ Kiểm tra MongoDB connection
- ✅ Khởi tạo database
- ✅ Xử lý vector embeddings (optional)
- ✅ Hiển thị thông tin kết nối

**Sử dụng:**
```bash
./scripts/run_all.sh
```

**Environment Variables:**
```bash
export MONGODB_URL="mongodb://localhost:27017"
export GOOGLE_API_KEY="your_google_genai_api_key"
```

---

### 🏗️ `init_database.py` - Database Initialization

**Mục đích:** Tạo database structure và sample data

**Tính năng:**
- ✅ Tạo collections (users, courses, uploads, etc.)
- ✅ Tạo indexes tối ưu cho performance
- ✅ Setup vector search index structure
- ✅ Tạo admin user mẫu
- ✅ Tạo sample courses và quizzes
- ✅ Setup embedding system
- ✅ Health check

**Sử dụng:**
```bash
python3 scripts/init_database.py
```

**Kết quả:**
```
✅ Database: ai_learning_platform
✅ Admin user: admin@ailearning.com / admin123456
✅ Sample courses: 3 courses
✅ Collections: 11 collections với indexes
```

---

### 🔮 `vector_chunking.py` - Vector Processing

**Mục đích:** Xử lý text thành chunks và tạo embeddings

**Tính năng:**
- ✅ **Text Chunking**: Chia văn bản thành chunks 1000 ký tự
- ✅ **Smart Splitting**: Chia theo câu, tránh cắt giữa từ
- ✅ **Overlap Strategy**: 200 ký tự overlap giữa chunks
- ✅ **Embedding Generation**: Google GenAI embeddings (768 dimensions)
- ✅ **Metadata Preservation**: Lưu thông tin source, chapter, word count
- ✅ **Batch Processing**: Xử lý nhiều documents cùng lúc
- ✅ **Vector Search**: Tìm kiếm semantic với cosine similarity

**Sử dụng:**
```bash
python3 scripts/vector_chunking.py
```

**Menu Options:**
1. Reindex all content
2. Process specific course
3. Process specific upload
4. Search similar content
5. Show embedding stats

**Chunking Strategy:**
```python
chunk_size = 1000      # Kích thước chunk
overlap = 200          # Overlap giữa chunks
dimensions = 768       # Google GenAI embedding dimensions
similarity = "cosine"  # Cosine similarity
```

---

### ☁️ `atlas_setup.py` - MongoDB Atlas Setup

**Mục đích:** Hướng dẫn setup MongoDB Atlas cho production

**Tính năng:**
- ✅ Generate Atlas CLI commands
- ✅ Vector search index configuration
- ✅ Production environment template
- ✅ Docker production setup
- ✅ Nginx configuration
- ✅ Deployment scripts

**Sử dụng:**
```bash
python3 scripts/atlas_setup.py
```

**Generated Files:**
- `.env.production` - Environment template
- `vector_index.json` - Vector search config
- `Dockerfile.prod` - Production Docker
- `docker-compose.prod.yml` - Production compose
- `nginx.prod.conf` - Nginx config
- `deploy.sh` - Deployment script

**Atlas Requirements:**
- **Cluster:** M10+ (minimum for Vector Search)
- **MongoDB Version:** 7.0+
- **Regions:** US_EAST_1 (recommended)
- **Features:** Vector Search enabled

---

### ⚡ `optimize_database.py` - Performance Optimization

**Mục đích:** Tối ưu hóa database performance và maintenance

**Tính năng:**
- ✅ **Collection Analysis**: Thống kê size, document count
- ✅ **Index Usage Analysis**: Monitor index performance
- ✅ **Duplicate Cleanup**: Xóa duplicate embeddings
- ✅ **Old Data Cleanup**: Dọn dẹp data cũ (90 days)
- ✅ **System Stats Update**: Cập nhật thống kê hệ thống
- ✅ **Performance Indexes**: Tạo compound indexes
- ✅ **Slow Query Monitor**: Phát hiện slow queries
- ✅ **Critical Data Backup**: Backup admin users, system courses
- ✅ **Health Check**: Kiểm tra tình trạng database

**Sử dụng:**
```bash
python3 scripts/optimize_database.py
```

**Recommended Schedule:**
- **Daily**: Health check, system stats update
- **Weekly**: Duplicate cleanup, old data cleanup
- **Monthly**: Index analysis, performance review
- **Quarterly**: Full optimization run

---

## 📊 Database Schema

### Collections Structure

```
ai_learning_platform/
├── users                 # User accounts
├── courses               # Learning courses
├── uploads               # File uploads
├── quizzes               # Quiz definitions
├── quiz_history          # Quiz results
├── chat_sessions         # Chat sessions
├── chat_messages         # Chat messages
├── dashboard_progress    # User progress
├── embeddings           # Vector embeddings
├── chapters             # Course chapters
└── system_stats         # System statistics
```

### Key Indexes

```javascript
// Users
{ "email": 1 }              // Unique
{ "role": 1 }
{ "created_at": -1 }

// Courses
{ "title": "text", "description": "text" }
{ "owner_id": 1 }
{ "level": 1 }
{ "tags": 1 }
{ "is_public": 1 }

// Embeddings
{ "source_id": 1, "chunk_index": 1 }
{ "source_type": 1 }
{ "embedding": "vector" }   // Vector Search Index

// Performance Indexes
{ "user_id": 1, "last_accessed": -1 }
{ "user_id": 1, "score": -1, "completed_at": -1 }
{ "session_id": 1, "created_at": 1 }
```

## 🔍 Vector Search Setup

### MongoDB Atlas Vector Search

**Requirements:**
- MongoDB Atlas M10+ cluster
- MongoDB version 7.0+
- Vector Search feature enabled

**Index Configuration:**
```json
{
  "name": "vector_index",
  "definition": {
    "fields": [
      {
        "type": "vector",
        "path": "embedding",
        "numDimensions": 768,
        "similarity": "cosine"
      },
      {
        "type": "filter",
        "path": "source_type"
      }
    ]
  }
}
```

**Create Index:**
1. Atlas Dashboard → Database → Search
2. Create Search Index → Vector Search
3. Database: `ai_learning_platform`
4. Collection: `embeddings`
5. Paste configuration above

### Local Development

Cho development local, vector search sẽ sử dụng dummy data. Để test đầy đủ, cần:

1. **MongoDB Atlas account**
2. **M10+ cluster** 
3. **Vector Search index**
4. **Google GenAI API key**

## 🚨 Troubleshooting

### Common Issues

#### 1. Connection Error
```bash
❌ Error: ServerSelectionTimeoutError
```
**Solution:**
- Kiểm tra MongoDB đang chạy
- Kiểm tra connection string
- Kiểm tra network access (Atlas)

#### 2. Vector Search Error
```bash
⚠️ Vector search error: index not found
```
**Solution:**
- Tạo vector search index trong Atlas
- Đợi index build hoàn thành (5-10 phút)
- Kiểm tra index name: `vector_index`

#### 3. Google GenAI Error
```bash
⚠️ Error generating embedding
```
**Solution:**
- Set `GOOGLE_API_KEY` environment variable
- Kiểm tra API key còn valid
- Kiểm tra quota limits

#### 4. Permission Error
```bash
❌ Insufficient permissions
```
**Solution:**
- User cần `readWriteAnyDatabase` role
- Kiểm tra database user permissions
- Kiểm tra IP whitelist (Atlas)

### Debug Commands

```bash
# Test MongoDB connection
python3 -c "from motor.motor_asyncio import AsyncIOMotorClient; import asyncio; asyncio.run(AsyncIOMotorClient('mongodb://localhost:27017').admin.command('ping')); print('✅ Connected')"

# Check collections
python3 -c "from motor.motor_asyncio import AsyncIOMotorClient; import asyncio; print(asyncio.run(AsyncIOMotorClient('mongodb://localhost:27017')['ai_learning_platform'].list_collection_names()))"

# Test Google GenAI
python3 -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print('✅ GenAI OK')"
```

## 📈 Performance Tips

### Production Optimization

1. **Use MongoDB Atlas M10+**
   - Vector Search support
   - Better performance
   - Automatic scaling

2. **Enable Profiling**
   ```javascript
   db.runCommand({profile: 2, slowms: 100})
   ```

3. **Monitor Indexes**
   ```javascript
   db.collection.aggregate([{$indexStats: {}}])
   ```

4. **Optimize Chunks**
   - Chunk size: 1000 characters
   - Overlap: 200 characters
   - Max chunks per document: 100

5. **Regular Maintenance**
   - Run `optimize_database.py` weekly
   - Monitor slow queries
   - Clean old data monthly

### Memory Usage

```bash
# MongoDB memory usage
db.serverStatus().mem

# Index size
db.stats()

# Collection stats
db.collection.stats()
```

## 🎯 Production Checklist

- [ ] MongoDB Atlas M10+ cluster created
- [ ] Vector search index created and active
- [ ] Database user with proper permissions
- [ ] IP whitelist configured
- [ ] Google GenAI API key configured
- [ ] Environment variables set
- [ ] Database initialized with sample data
- [ ] Vector embeddings processed
- [ ] Health check passing
- [ ] Backup strategy implemented
- [ ] Monitoring setup
- [ ] Performance optimization completed

## 📞 Support

### Resources
- [MongoDB Atlas Docs](https://docs.atlas.mongodb.com/)
- [Vector Search Guide](https://docs.atlas.mongodb.com/atlas-vector-search/)
- [Google GenAI Docs](https://ai.google.dev/docs)

### Common Commands
```bash
# Full setup
./scripts/run_all.sh

# Production setup
python3 scripts/atlas_setup.py

# Maintenance
python3 scripts/optimize_database.py

# Vector processing
python3 scripts/vector_chunking.py
```

---

**🎉 Happy Learning with AI! 🤖✨**
