#!/usr/bin/env python3
"""
Database Optimization Script for AI Learning Platform
Tối ưu hóa performance và monitoring cho production
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class DatabaseOptimizer:
    """Class để tối ưu hóa database performance"""
    
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or settings.mongodb_url
        self.database_name = settings.database_name
        self.client = None
        self.db = None
        
    async def connect(self):
        """Kết nối database"""
        self.client = AsyncIOMotorClient(self.connection_string)
        self.db = self.client[self.database_name]
        
    async def analyze_collection_stats(self) -> Dict[str, Any]:
        """Phân tích thống kê collections"""
        print("📊 Analyzing collection statistics...")
        
        stats = {}
        collections = await self.db.list_collection_names()
        
        for collection_name in collections:
            collection = self.db[collection_name]
            
            # Basic stats
            count = await collection.count_documents({})
            
            # Collection stats from MongoDB
            try:
                db_stats = await self.db.command("collStats", collection_name)
                size_mb = db_stats.get('size', 0) / (1024 * 1024)
                avg_obj_size = db_stats.get('avgObjSize', 0)
                index_size_mb = db_stats.get('totalIndexSize', 0) / (1024 * 1024)
            except:
                size_mb = 0
                avg_obj_size = 0
                index_size_mb = 0
            
            stats[collection_name] = {
                'document_count': count,
                'size_mb': round(size_mb, 2),
                'avg_obj_size_bytes': round(avg_obj_size, 2),
                'index_size_mb': round(index_size_mb, 2)
            }
            
        return stats
        
    async def analyze_index_usage(self) -> Dict[str, Any]:
        """Phân tích usage của indexes"""
        print("🔍 Analyzing index usage...")
        
        index_stats = {}
        collections = ['users', 'courses', 'uploads', 'embeddings', 'quiz_history']
        
        for collection_name in collections:
            try:
                # Get index stats
                stats = await self.db[collection_name].aggregate([
                    {"$indexStats": {}}
                ]).to_list(None)
                
                index_stats[collection_name] = {}
                for stat in stats:
                    index_name = stat['name']
                    usage_count = stat['accesses']['ops']
                    since = stat['accesses'].get('since', datetime.utcnow())
                    
                    index_stats[collection_name][index_name] = {
                        'usage_count': usage_count,
                        'since': since,
                        'usage_per_day': usage_count / max(1, (datetime.utcnow() - since).days or 1)
                    }
                    
            except Exception as e:
                print(f"⚠️  Could not get index stats for {collection_name}: {e}")
                
        return index_stats
        
    async def optimize_embeddings_collection(self):
        """Tối ưu hóa collection embeddings"""
        print("🔮 Optimizing embeddings collection...")
        
        # Check for duplicate embeddings
        pipeline = [
            {
                "$group": {
                    "_id": {"source_id": "$source_id", "chunk_index": "$chunk_index"},
                    "count": {"$sum": 1},
                    "ids": {"$push": "$_id"}
                }
            },
            {"$match": {"count": {"$gt": 1}}}
        ]
        
        duplicates = await self.db.embeddings.aggregate(pipeline).to_list(None)
        
        if duplicates:
            print(f"🔍 Found {len(duplicates)} duplicate embedding groups")
            
            removed_count = 0
            for dup in duplicates:
                # Keep first, remove others
                ids_to_remove = dup['ids'][1:]
                result = await self.db.embeddings.delete_many(
                    {"_id": {"$in": ids_to_remove}}
                )
                removed_count += result.deleted_count
                
            print(f"✅ Removed {removed_count} duplicate embeddings")
        else:
            print("✅ No duplicate embeddings found")
            
    async def cleanup_old_data(self, days: int = 90):
        """Dọn dẹp data cũ"""
        print(f"🧹 Cleaning up data older than {days} days...")
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Clean old chat messages (keep sessions)
        result = await self.db.chat_messages.delete_many({
            "created_at": {"$lt": cutoff_date}
        })
        print(f"🗑️  Removed {result.deleted_count} old chat messages")
        
        # Clean old quiz history (keep recent results)
        result = await self.db.quiz_history.delete_many({
            "completed_at": {"$lt": cutoff_date},
            "score": {"$lt": 50}  # Only remove low scores
        })
        print(f"🗑️  Removed {result.deleted_count} old low-score quiz results")
        
    async def update_system_stats(self):
        """Cập nhật system statistics"""
        print("📊 Updating system statistics...")
        
        stats = {
            'total_users': await self.db.users.count_documents({}),
            'active_users': await self.db.users.count_documents({'is_active': True}),
            'total_courses': await self.db.courses.count_documents({}),
            'public_courses': await self.db.courses.count_documents({'is_public': True}),
            'total_uploads': await self.db.uploads.count_documents({}),
            'completed_uploads': await self.db.uploads.count_documents({'status': 'completed'}),
            'total_quizzes': await self.db.quizzes.count_documents({}),
            'total_quiz_attempts': await self.db.quiz_history.count_documents({}),
            'total_chat_sessions': await self.db.chat_sessions.count_documents({}),
            'active_chat_sessions': await self.db.chat_sessions.count_documents({'status': 'active'}),
            'total_embeddings': await self.db.embeddings.count_documents({}),
            'last_updated': datetime.utcnow()
        }
        
        # Calculate average scores
        pipeline = [
            {"$group": {"_id": None, "avg_score": {"$avg": "$score"}}}
        ]
        avg_result = await self.db.quiz_history.aggregate(pipeline).to_list(None)
        stats['average_quiz_score'] = round(avg_result[0]['avg_score'], 2) if avg_result else 0
        
        # Update or insert stats
        await self.db.system_stats.replace_one(
            {},
            stats,
            upsert=True
        )
        
        print("✅ System statistics updated")
        return stats
        
    async def create_performance_indexes(self):
        """Tạo indexes bổ sung cho performance"""
        print("⚡ Creating performance indexes...")
        
        # Compound indexes for common queries
        performance_indexes = [
            # User activity tracking
            {
                'collection': 'dashboard_progress',
                'index': [('user_id', 1), ('last_accessed', -1)],
                'name': 'user_activity_idx'
            },
            # Quiz performance queries
            {
                'collection': 'quiz_history',
                'index': [('user_id', 1), ('score', -1), ('completed_at', -1)],
                'name': 'user_quiz_performance_idx'
            },
            # Chat session queries
            {
                'collection': 'chat_messages',
                'index': [('session_id', 1), ('created_at', 1)],
                'name': 'session_timeline_idx'
            },
            # Embedding search optimization
            {
                'collection': 'embeddings',
                'index': [('source_type', 1), ('source_id', 1), ('chunk_index', 1)],
                'name': 'embedding_lookup_idx'
            }
        ]
        
        for idx_config in performance_indexes:
            try:
                await self.db[idx_config['collection']].create_index(
                    idx_config['index'],
                    name=idx_config['name'],
                    background=True
                )
                print(f"✅ Created index: {idx_config['name']}")
            except Exception as e:
                if 'already exists' in str(e):
                    print(f"ℹ️  Index exists: {idx_config['name']}")
                else:
                    print(f"⚠️  Error creating {idx_config['name']}: {e}")
                    
    async def monitor_slow_queries(self, duration_seconds: int = 60):
        """Monitor slow queries"""
        print(f"🐌 Monitoring slow queries for {duration_seconds} seconds...")
        
        # Enable profiling for slow operations (>100ms)
        await self.db.command('profile', 2, slowms=100)
        
        print("⏳ Profiling enabled. Generating some sample queries...")
        
        # Run some sample queries to generate profile data
        await self.db.users.find({'role': 'student'}).limit(10).to_list(None)
        await self.db.courses.find({'level': 'beginner'}).limit(10).to_list(None)
        await self.db.embeddings.find({'source_type': 'course'}).limit(5).to_list(None)
        
        await asyncio.sleep(duration_seconds)
        
        # Get profile data
        profile_data = await self.db.system.profile.find().sort('ts', -1).limit(10).to_list(None)
        
        # Disable profiling
        await self.db.command('profile', 0)
        
        print(f"🔍 Found {len(profile_data)} profiled operations:")
        for op in profile_data:
            duration_ms = op.get('durationMillis', 0)
            command = op.get('command', {})
            collection = command.get('find') or command.get('aggregate') or 'unknown'
            print(f"   {collection}: {duration_ms}ms")
            
    async def backup_critical_data(self):
        """Backup critical system data"""
        print("💾 Creating backup of critical data...")
        
        backup_data = {
            'timestamp': datetime.utcnow(),
            'admin_users': [],
            'system_courses': [],
            'system_stats': None
        }
        
        # Backup admin users
        admin_users = await self.db.users.find({'role': 'admin'}).to_list(None)
        for user in admin_users:
            backup_data['admin_users'].append({
                'email': user['email'],
                'name': user['name'],
                'created_at': user['created_at']
            })
            
        # Backup system courses
        system_courses = await self.db.courses.find({'source': 'system'}).to_list(None)
        for course in system_courses:
            backup_data['system_courses'].append({
                'title': course['title'],
                'description': course['description'],
                'level': course['level'],
                'tags': course['tags']
            })
            
        # Backup system stats
        stats = await self.db.system_stats.find_one({})
        backup_data['system_stats'] = stats
        
        # Save backup
        backup_filename = f"backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        import json
        with open(backup_filename, 'w') as f:
            json.dump(backup_data, f, indent=2, default=str)
            
        print(f"✅ Backup saved to: {backup_filename}")
        
    async def run_health_check(self) -> Dict[str, Any]:
        """Chạy health check toàn diện"""
        print("🏥 Running comprehensive health check...")
        
        health_status = {
            'timestamp': datetime.utcnow(),
            'database_connection': False,
            'collections_status': {},
            'index_health': {},
            'data_integrity': {},
            'performance_metrics': {}
        }
        
        try:
            # Test connection
            await self.client.admin.command('ping')
            health_status['database_connection'] = True
            
            # Check collections
            collections = await self.db.list_collection_names()
            required_collections = ['users', 'courses', 'uploads', 'embeddings']
            
            for collection in required_collections:
                if collection in collections:
                    count = await self.db[collection].count_documents({})
                    health_status['collections_status'][collection] = {
                        'exists': True,
                        'document_count': count
                    }
                else:
                    health_status['collections_status'][collection] = {
                        'exists': False,
                        'document_count': 0
                    }
                    
            # Check data integrity
            admin_count = await self.db.users.count_documents({'role': 'admin'})
            health_status['data_integrity']['admin_users'] = admin_count > 0
            
            embedding_count = await self.db.embeddings.count_documents({})
            health_status['data_integrity']['embeddings_available'] = embedding_count > 0
            
            print("✅ Health check completed")
            
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            health_status['error'] = str(e)
            
        return health_status
        
    async def close(self):
        """Đóng kết nối"""
        if self.client:
            self.client.close()

async def main():
    """Main function"""
    print("⚡ AI Learning Platform Database Optimizer")
    print("=" * 50)
    
    optimizer = DatabaseOptimizer()
    
    try:
        await optimizer.connect()
        
        while True:
            print("\n🔧 Choose optimization task:")
            print("1. Analyze collection statistics")
            print("2. Analyze index usage")
            print("3. Optimize embeddings collection")
            print("4. Clean up old data")
            print("5. Update system statistics")
            print("6. Create performance indexes")
            print("7. Monitor slow queries")
            print("8. Backup critical data")
            print("9. Run health check")
            print("10. Run all optimizations")
            print("11. Exit")
            
            choice = input("\nEnter your choice (1-11): ").strip()
            
            if choice == '1':
                stats = await optimizer.analyze_collection_stats()
                print("\n📊 Collection Statistics:")
                for collection, data in stats.items():
                    print(f"  {collection}:")
                    print(f"    Documents: {data['document_count']:,}")
                    print(f"    Size: {data['size_mb']} MB")
                    print(f"    Index Size: {data['index_size_mb']} MB")
                    
            elif choice == '2':
                index_stats = await optimizer.analyze_index_usage()
                print("\n🔍 Index Usage Statistics:")
                for collection, indexes in index_stats.items():
                    print(f"  {collection}:")
                    for index_name, data in indexes.items():
                        print(f"    {index_name}: {data['usage_count']} uses")
                        
            elif choice == '3':
                await optimizer.optimize_embeddings_collection()
                
            elif choice == '4':
                days = input("Enter days to keep (default 90): ").strip()
                days = int(days) if days else 90
                await optimizer.cleanup_old_data(days)
                
            elif choice == '5':
                stats = await optimizer.update_system_stats()
                print("\n📊 Updated System Stats:")
                for key, value in stats.items():
                    if key != 'last_updated':
                        print(f"  {key}: {value}")
                        
            elif choice == '6':
                await optimizer.create_performance_indexes()
                
            elif choice == '7':
                duration = input("Monitor duration in seconds (default 60): ").strip()
                duration = int(duration) if duration else 60
                await optimizer.monitor_slow_queries(duration)
                
            elif choice == '8':
                await optimizer.backup_critical_data()
                
            elif choice == '9':
                health = await optimizer.run_health_check()
                print("\n🏥 Health Check Results:")
                print(f"  Database Connection: {'✅' if health['database_connection'] else '❌'}")
                for collection, status in health['collections_status'].items():
                    print(f"  {collection}: {'✅' if status['exists'] else '❌'} ({status['document_count']} docs)")
                    
            elif choice == '10':
                print("🚀 Running all optimizations...")
                await optimizer.create_performance_indexes()
                await optimizer.optimize_embeddings_collection()
                await optimizer.cleanup_old_data(90)
                await optimizer.update_system_stats()
                await optimizer.backup_critical_data()
                health = await optimizer.run_health_check()
                print("✅ All optimizations completed!")
                
            elif choice == '11':
                break
                
            else:
                print("❌ Invalid choice. Please try again.")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
    finally:
        await optimizer.close()

if __name__ == "__main__":
    asyncio.run(main())
