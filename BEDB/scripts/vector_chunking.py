#!/usr/bin/env python3
"""
Vector Chunking and Embedding System for AI Learning Platform
Xử lý văn bản thành chunks và tạo embeddings cho vector search
"""

import asyncio
import sys
import os
from typing import List, Dict, Any, Optional
import re
from datetime import datetime
import hashlib

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motor.motor_asyncio import AsyncIOMotorClient
import google.generativeai as genai
from app.config import settings

class TextChunker:
    """Class để chia văn bản thành chunks tối ưu"""
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap
        
    def clean_text(self, text: str) -> str:
        """Làm sạch văn bản"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.,!?;:()\-\'""]', ' ', text)
        return text.strip()
        
    def split_by_sentences(self, text: str) -> List[str]:
        """Chia văn bản theo câu"""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
        
    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Chia văn bản thành chunks với metadata"""
        if not text or len(text.strip()) == 0:
            return []
            
        text = self.clean_text(text)
        chunks = []
        
        # Nếu text ngắn hơn chunk_size, trả về toàn bộ
        if len(text) <= self.chunk_size:
            chunks.append({
                'text': text,
                'chunk_index': 0,
                'start_pos': 0,
                'end_pos': len(text),
                'word_count': len(text.split()),
                'metadata': metadata or {}
            })
            return chunks
            
        # Chia theo câu để tránh cắt giữa câu
        sentences = self.split_by_sentences(text)
        
        current_chunk = ""
        current_start = 0
        chunk_index = 0
        
        for sentence in sentences:
            # Nếu thêm câu này vào chunk hiện tại vẫn < chunk_size
            if len(current_chunk + sentence) <= self.chunk_size:
                current_chunk += sentence + ". "
            else:
                # Lưu chunk hiện tại
                if current_chunk:
                    chunks.append({
                        'text': current_chunk.strip(),
                        'chunk_index': chunk_index,
                        'start_pos': current_start,
                        'end_pos': current_start + len(current_chunk),
                        'word_count': len(current_chunk.split()),
                        'metadata': metadata or {}
                    })
                    
                    # Tạo overlap với chunk trước
                    if self.overlap > 0 and chunk_index > 0:
                        overlap_text = current_chunk[-self.overlap:] if len(current_chunk) > self.overlap else current_chunk
                        current_chunk = overlap_text + sentence + ". "
                    else:
                        current_chunk = sentence + ". "
                        
                    current_start += len(current_chunk) - self.overlap if chunk_index > 0 else 0
                    chunk_index += 1
                else:
                    current_chunk = sentence + ". "
                    
        # Thêm chunk cuối cùng
        if current_chunk:
            chunks.append({
                'text': current_chunk.strip(),
                'chunk_index': chunk_index,
                'start_pos': current_start,
                'end_pos': current_start + len(current_chunk),
                'word_count': len(current_chunk.split()),
                'metadata': metadata or {}
            })
            
        return chunks

class EmbeddingGenerator:
    """Class để tạo embeddings từ text chunks"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.google_api_key
        if self.api_key:
            genai.configure(api_key=self.api_key)
            
    async def generate_embedding(self, text: str) -> List[float]:
        """Tạo embedding vector từ text"""
        try:
            if not self.api_key:
                # Return dummy embedding for testing
                return [0.1] * 768
                
            # Use Google's embedding model
            model = 'models/embedding-001'
            result = genai.embed_content(
                model=model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
            
        except Exception as e:
            print(f"⚠️  Error generating embedding: {e}")
            # Return dummy embedding as fallback
            return [0.1] * 768
            
    async def batch_generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Tạo embeddings cho nhiều texts cùng lúc"""
        embeddings = []
        for text in texts:
            embedding = await self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings

class VectorProcessor:
    """Main class để xử lý vector cho toàn hệ thống"""
    
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or settings.mongodb_url
        self.database_name = settings.database_name
        self.client = None
        self.db = None
        self.chunker = TextChunker()
        self.embedding_generator = EmbeddingGenerator()
        
    async def connect(self):
        """Kết nối database"""
        self.client = AsyncIOMotorClient(self.connection_string)
        self.db = self.client[self.database_name]
        
    async def process_course_content(self, course_id: str) -> int:
        """Xử lý nội dung course thành vectors"""
        print(f"📚 Processing course: {course_id}")
        
        # Get course data
        course = await self.db.courses.find_one({"_id": course_id})
        if not course:
            print(f"❌ Course not found: {course_id}")
            return 0
            
        # Combine course content
        content_parts = []
        if course.get('title'):
            content_parts.append(f"Title: {course['title']}")
        if course.get('description'):
            content_parts.append(f"Description: {course['description']}")
        if course.get('outline'):
            content_parts.append(f"Outline: {course['outline']}")
            
        full_content = "\n\n".join(content_parts)
        
        if not full_content:
            print("⚠️  No content to process")
            return 0
            
        # Create chunks
        metadata = {
            'course_id': str(course_id),
            'title': course.get('title', ''),
            'level': course.get('level', ''),
            'tags': course.get('tags', [])
        }
        
        chunks = self.chunker.chunk_text(full_content, metadata)
        print(f"✂️  Created {len(chunks)} chunks")
        
        # Generate embeddings
        processed_count = 0
        for chunk in chunks:
            embedding = await self.embedding_generator.generate_embedding(chunk['text'])
            
            # Create embedding document
            embedding_doc = {
                'source_id': str(course_id),
                'source_type': 'course',
                'chunk_index': chunk['chunk_index'],
                'text': chunk['text'],
                'embedding': embedding,
                'metadata': {
                    **chunk['metadata'],
                    'word_count': chunk['word_count'],
                    'start_pos': chunk['start_pos'],
                    'end_pos': chunk['end_pos']
                },
                'created_at': datetime.utcnow()
            }
            
            # Remove existing embeddings for this source
            if chunk['chunk_index'] == 0:
                await self.db.embeddings.delete_many({
                    'source_id': str(course_id),
                    'source_type': 'course'
                })
                
            # Insert new embedding
            await self.db.embeddings.insert_one(embedding_doc)
            processed_count += 1
            
        print(f"✅ Processed {processed_count} chunks for course")
        return processed_count
        
    async def process_upload_content(self, upload_id: str) -> int:
        """Xử lý nội dung upload thành vectors"""
        print(f"📄 Processing upload: {upload_id}")
        
        # Get upload data
        upload = await self.db.uploads.find_one({"_id": upload_id})
        if not upload:
            print(f"❌ Upload not found: {upload_id}")
            return 0
            
        content = upload.get('extracted_text', '')
        if not content:
            print("⚠️  No extracted text found")
            return 0
            
        # Create chunks
        metadata = {
            'upload_id': str(upload_id),
            'filename': upload.get('filename', ''),
            'file_type': upload.get('file_type', ''),
            'user_id': str(upload.get('user_id', ''))
        }
        
        chunks = self.chunker.chunk_text(content, metadata)
        print(f"✂️  Created {len(chunks)} chunks")
        
        # Generate embeddings
        processed_count = 0
        for chunk in chunks:
            embedding = await self.embedding_generator.generate_embedding(chunk['text'])
            
            embedding_doc = {
                'source_id': str(upload_id),
                'source_type': 'upload',
                'chunk_index': chunk['chunk_index'],
                'text': chunk['text'],
                'embedding': embedding,
                'metadata': {
                    **chunk['metadata'],
                    'word_count': chunk['word_count'],
                    'start_pos': chunk['start_pos'],
                    'end_pos': chunk['end_pos']
                },
                'created_at': datetime.utcnow()
            }
            
            # Remove existing embeddings
            if chunk['chunk_index'] == 0:
                await self.db.embeddings.delete_many({
                    'source_id': str(upload_id),
                    'source_type': 'upload'
                })
                
            await self.db.embeddings.insert_one(embedding_doc)
            processed_count += 1
            
        print(f"✅ Processed {processed_count} chunks for upload")
        return processed_count
        
    async def reindex_all_content(self):
        """Reindex tất cả content trong hệ thống"""
        print("🔄 Reindexing all content...")
        
        total_processed = 0
        
        # Process all courses
        courses = await self.db.courses.find({}).to_list(None)
        print(f"📚 Found {len(courses)} courses to process")
        
        for course in courses:
            count = await self.process_course_content(course['_id'])
            total_processed += count
            
        # Process all uploads
        uploads = await self.db.uploads.find({'status': 'completed'}).to_list(None)
        print(f"📄 Found {len(uploads)} uploads to process")
        
        for upload in uploads:
            count = await self.process_upload_content(upload['_id'])
            total_processed += count
            
        print(f"🎉 Reindexing completed! Total chunks processed: {total_processed}")
        return total_processed
        
    async def search_similar_content(self, query: str, limit: int = 10, source_types: List[str] = None) -> List[Dict]:
        """Tìm kiếm content tương tự bằng vector search"""
        print(f"🔍 Searching for: {query}")
        
        # Generate query embedding
        query_embedding = await self.embedding_generator.generate_embedding(query)
        
        # Build aggregation pipeline
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": limit * 10,
                    "limit": limit
                }
            }
        ]
        
        # Add source type filter if specified
        if source_types:
            pipeline.append({
                "$match": {"source_type": {"$in": source_types}}
            })
            
        # Add metadata projection
        pipeline.append({
            "$project": {
                "text": 1,
                "source_id": 1,
                "source_type": 1,
                "chunk_index": 1,
                "metadata": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        })
        
        try:
            results = await self.db.embeddings.aggregate(pipeline).to_list(length=limit)
            print(f"✅ Found {len(results)} similar chunks")
            return results
        except Exception as e:
            print(f"⚠️  Vector search error: {e}")
            print("💡 Make sure vector search index is created in MongoDB Atlas")
            return []
            
    async def get_embedding_stats(self) -> Dict[str, Any]:
        """Lấy thống kê về embeddings"""
        stats = {}
        
        # Total embeddings
        stats['total_embeddings'] = await self.db.embeddings.count_documents({})
        
        # By source type
        pipeline = [
            {"$group": {"_id": "$source_type", "count": {"$sum": 1}}}
        ]
        source_stats = await self.db.embeddings.aggregate(pipeline).to_list(None)
        stats['by_source_type'] = {item['_id']: item['count'] for item in source_stats}
        
        # Average chunks per source
        pipeline = [
            {"$group": {"_id": "$source_id", "chunk_count": {"$sum": 1}}},
            {"$group": {"_id": None, "avg_chunks": {"$avg": "$chunk_count"}}}
        ]
        avg_result = await self.db.embeddings.aggregate(pipeline).to_list(None)
        stats['avg_chunks_per_source'] = avg_result[0]['avg_chunks'] if avg_result else 0
        
        return stats
        
    async def close(self):
        """Đóng kết nối"""
        if self.client:
            self.client.close()

async def main():
    """Main function"""
    print("🔮 AI Learning Platform Vector Processing System")
    print("=" * 50)
    
    processor = VectorProcessor()
    
    try:
        await processor.connect()
        
        # Show current stats
        stats = await processor.get_embedding_stats()
        print("📊 Current embedding stats:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        print()
        
        # Menu options
        while True:
            print("\n🔧 Choose an option:")
            print("1. Reindex all content")
            print("2. Process specific course")
            print("3. Process specific upload")
            print("4. Search similar content")
            print("5. Show embedding stats")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                await processor.reindex_all_content()
                
            elif choice == '2':
                course_id = input("Enter course ID: ").strip()
                if course_id:
                    await processor.process_course_content(course_id)
                    
            elif choice == '3':
                upload_id = input("Enter upload ID: ").strip()
                if upload_id:
                    await processor.process_upload_content(upload_id)
                    
            elif choice == '4':
                query = input("Enter search query: ").strip()
                if query:
                    results = await processor.search_similar_content(query)
                    for i, result in enumerate(results[:3], 1):
                        print(f"\n{i}. Score: {result.get('score', 0):.3f}")
                        print(f"   Source: {result['source_type']} ({result['source_id']})")
                        print(f"   Text: {result['text'][:200]}...")
                        
            elif choice == '5':
                stats = await processor.get_embedding_stats()
                print("\n📊 Embedding Statistics:")
                for key, value in stats.items():
                    print(f"   {key}: {value}")
                    
            elif choice == '6':
                break
                
            else:
                print("❌ Invalid choice. Please try again.")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
    finally:
        await processor.close()

if __name__ == "__main__":
    asyncio.run(main())
