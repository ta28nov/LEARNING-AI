#!/usr/bin/env python3
"""
Migration Script: Add Visibility Fields to Existing Courses
Migrates existing courses to include visibility, is_approved, and enrollment_count fields
"""

import asyncio
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class CourseMigration:
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or settings.mongodb_url
        self.database_name = settings.database_name
        self.client = None
        self.db = None
        
    async def connect(self):
        """Kết nối đến MongoDB"""
        print(f"🔗 Connecting to MongoDB: {self.database_name}")
        self.client = AsyncIOMotorClient(self.connection_string)
        self.db = self.client[self.database_name]
        
        # Test connection
        await self.client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!")
        
    async def backup_courses(self):
        """Tạo backup collection trước khi migrate"""
        print("💾 Creating backup collection...")
        
        # Copy courses to backup collection
        courses = await self.db.courses.find({}).to_list(None)
        
        if courses:
            backup_name = f"courses_backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            await self.db[backup_name].insert_many(courses)
            print(f"✅ Backup created: {backup_name} ({len(courses)} documents)")
            return backup_name
        else:
            print("ℹ️  No courses to backup")
            return None
            
    async def analyze_courses(self):
        """Phân tích courses hiện có"""
        print("🔍 Analyzing existing courses...")
        
        total_courses = await self.db.courses.count_documents({})
        
        # Check for courses with old structure
        without_visibility = await self.db.courses.count_documents({
            "visibility": {"$exists": False}
        })
        
        without_approval = await self.db.courses.count_documents({
            "is_approved": {"$exists": False}
        })
        
        without_enrollment_count = await self.db.courses.count_documents({
            "enrollment_count": {"$exists": False}
        })
        
        print(f"📊 Analysis Results:")
        print(f"   Total courses: {total_courses}")
        print(f"   Missing visibility field: {without_visibility}")
        print(f"   Missing is_approved field: {without_approval}")
        print(f"   Missing enrollment_count field: {without_enrollment_count}")
        
        return {
            "total": total_courses,
            "needs_migration": max(without_visibility, without_approval, without_enrollment_count)
        }
        
    async def migrate_visibility_field(self):
        """Migrate visibility field based on is_public"""
        print("🔄 Migrating visibility field...")
        
        # Courses with is_public=True → visibility=public
        result1 = await self.db.courses.update_many(
            {
                "is_public": True,
                "visibility": {"$exists": False}
            },
            {
                "$set": {
                    "visibility": "public"
                }
            }
        )
        
        # Courses with is_public=False → visibility=private
        result2 = await self.db.courses.update_many(
            {
                "is_public": False,
                "visibility": {"$exists": False}
            },
            {
                "$set": {
                    "visibility": "private"
                }
            }
        )
        
        # Courses without is_public → visibility=draft
        result3 = await self.db.courses.update_many(
            {
                "is_public": {"$exists": False},
                "visibility": {"$exists": False}
            },
            {
                "$set": {
                    "visibility": "draft"
                }
            }
        )
        
        total_updated = result1.modified_count + result2.modified_count + result3.modified_count
        print(f"✅ Updated visibility for {total_updated} courses")
        print(f"   - Public: {result1.modified_count}")
        print(f"   - Private: {result2.modified_count}")
        print(f"   - Draft: {result3.modified_count}")
        
        return total_updated
        
    async def migrate_approval_field(self):
        """Migrate is_approved field"""
        print("🔄 Migrating is_approved field...")
        
        # All existing courses are approved by default
        result = await self.db.courses.update_many(
            {
                "is_approved": {"$exists": False}
            },
            {
                "$set": {
                    "is_approved": True,
                    "approved_at": datetime.utcnow()
                }
            }
        )
        
        print(f"✅ Set is_approved=True for {result.modified_count} courses")
        return result.modified_count
        
    async def migrate_enrollment_count(self):
        """Migrate enrollment_count field and calculate actual enrollments"""
        print("🔄 Migrating enrollment_count field...")
        
        # Get all courses
        courses = await self.db.courses.find(
            {"enrollment_count": {"$exists": False}}
        ).to_list(None)
        
        updated_count = 0
        
        for course in courses:
            # Count actual enrollments for this course
            enrollment_count = await self.db.course_enrollments.count_documents({
                "course_id": course["_id"]
            })
            
            # Update course with actual count
            await self.db.courses.update_one(
                {"_id": course["_id"]},
                {
                    "$set": {
                        "enrollment_count": enrollment_count
                    }
                }
            )
            
            updated_count += 1
            
        print(f"✅ Set enrollment_count for {updated_count} courses")
        return updated_count
        
    async def verify_migration(self):
        """Verify migration results"""
        print("✅ Verifying migration...")
        
        # Check all courses have required fields
        total = await self.db.courses.count_documents({})
        
        with_visibility = await self.db.courses.count_documents({
            "visibility": {"$exists": True}
        })
        
        with_approval = await self.db.courses.count_documents({
            "is_approved": {"$exists": True}
        })
        
        with_enrollment_count = await self.db.courses.count_documents({
            "enrollment_count": {"$exists": True}
        })
        
        print(f"📊 Verification Results:")
        print(f"   Total courses: {total}")
        print(f"   With visibility: {with_visibility} ({with_visibility == total and '✓' or '✗'})")
        print(f"   With is_approved: {with_approval} ({with_approval == total and '✓' or '✗'})")
        print(f"   With enrollment_count: {with_enrollment_count} ({with_enrollment_count == total and '✓' or '✗'})")
        
        # Sample courses
        sample_courses = await self.db.courses.find().limit(3).to_list(3)
        
        if sample_courses:
            print(f"\n📋 Sample courses after migration:")
            for course in sample_courses:
                print(f"   - {course.get('title', 'Untitled')}")
                print(f"     visibility: {course.get('visibility', 'N/A')}")
                print(f"     is_approved: {course.get('is_approved', 'N/A')}")
                print(f"     enrollment_count: {course.get('enrollment_count', 'N/A')}")
                
        return with_visibility == total and with_approval == total and with_enrollment_count == total
        
    async def close(self):
        """Đóng kết nối database"""
        if self.client:
            self.client.close()
            print("🔒 Database connection closed")

async def main():
    """Main function để chạy migration"""
    print("🚀 Course Visibility Migration Script")
    print("=" * 50)
    
    migration = CourseMigration()
    
    try:
        # Connect
        await migration.connect()
        
        # Analyze
        analysis = await migration.analyze_courses()
        
        if analysis["needs_migration"] == 0:
            print("\n✅ No migration needed - all courses already have required fields!")
            return
            
        print(f"\n⚠️  {analysis['needs_migration']} courses need migration")
        print("📝 Starting migration process...\n")
        
        # Backup
        backup_name = await migration.backup_courses()
        
        # Migrate
        await migration.migrate_visibility_field()
        await migration.migrate_approval_field()
        await migration.migrate_enrollment_count()
        
        # Verify
        success = await migration.verify_migration()
        
        if success:
            print("\n🎉 Migration completed successfully!")
            if backup_name:
                print(f"💾 Backup saved as: {backup_name}")
        else:
            print("\n⚠️  Migration completed with warnings - please check verification results")
            
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        raise
    finally:
        await migration.close()

if __name__ == "__main__":
    asyncio.run(main())
