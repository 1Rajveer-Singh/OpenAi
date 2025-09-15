"""
Database configuration and connection management for VyapaarGPT
"""

import os
import asyncio
from typing import AsyncGenerator, Optional
from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import asyncpg
from loguru import logger

from app.models.schemas import Base

class DatabaseConfig:
    """Database configuration and connection management"""
    
    def __init__(self):
        self.database_url = self._get_database_url()
        self.async_database_url = self._get_async_database_url()
        
        # Create engines
        self.engine = create_engine(
            self.database_url,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=os.getenv("DEBUG", "false").lower() == "true"
        )
        
        self.async_engine = create_async_engine(
            self.async_database_url,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=os.getenv("DEBUG", "false").lower() == "true"
        )
        
        # Create session makers
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.async_engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )
    
    def _get_database_url(self) -> str:
        """Get database URL for synchronous connections"""
        
        # Check for full database URL first
        if db_url := os.getenv("DATABASE_URL"):
            return db_url
        
        # Default to SQLite for demo
        return "sqlite:///./vyapaargpt_demo.db"
    
    def _get_async_database_url(self) -> str:
        """Get database URL for async connections"""
        
        # Check for async database URL first
        if async_db_url := os.getenv("ASYNC_DATABASE_URL"):
            return async_db_url
        
        # Default to SQLite for demo
        return "sqlite+aiosqlite:///./vyapaargpt_demo.db"
    
    async def create_database_if_not_exists(self):
        """Create database if it doesn't exist (SQLite auto-creates)"""
        
        try:
            # For SQLite, database is created automatically
            logger.info("Using SQLite database - auto-created if needed")
            
        except Exception as e:
            logger.error(f"Error with database: {e}")
            # Continue anyway, maybe database already exists
    
    async def create_tables(self):
        """Create all database tables"""
        
        try:
            async with self.async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
            
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise
    
    async def drop_tables(self):
        """Drop all database tables (for testing/development)"""
        
        try:
            async with self.async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
            logger.info("Database tables dropped successfully")
            
        except Exception as e:
            logger.error(f"Error dropping tables: {e}")
            raise
    
    def get_db(self) -> Session:
        """Get synchronous database session"""
        
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    async def get_async_db(self) -> AsyncGenerator[AsyncSession, None]:
        """Get asynchronous database session"""
        
        async with self.AsyncSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()
    
    async def check_connection(self) -> bool:
        """Check if database connection is working"""
        
        try:
            async with self.async_engine.begin() as conn:
                result = await conn.execute("SELECT 1")
                return True
                
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    async def get_database_stats(self) -> dict:
        """Get database statistics"""
        
        try:
            async with self.AsyncSessionLocal() as session:
                # Get table sizes
                result = await session.execute("""
                    SELECT 
                        schemaname,
                        tablename,
                        attname,
                        n_distinct,
                        correlation
                    FROM pg_stats 
                    WHERE schemaname = 'public'
                    ORDER BY tablename, attname;
                """)
                
                stats = {
                    "connection_status": "connected",
                    "database_url": self.database_url.split("@")[1] if "@" in self.database_url else "hidden",
                    "engine_info": str(self.async_engine.url),
                    "table_stats": [dict(row) for row in result.fetchall()]
                }
                
                return stats
                
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {
                "connection_status": "error",
                "error": str(e)
            }

class DatabaseManager:
    """High-level database management operations"""
    
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
    
    async def initialize_database(self, reset: bool = False):
        """Initialize database with tables and initial data"""
        
        logger.info("Initializing database...")
        
        # Create database if needed
        await self.db_config.create_database_if_not_exists()
        
        # Reset if requested
        if reset:
            logger.warning("Resetting database (dropping all tables)")
            await self.db_config.drop_tables()
        
        # Create tables
        await self.db_config.create_tables()
        
        # Add initial data
        await self._add_initial_data()
        
        logger.info("Database initialization completed")
    
    async def _add_initial_data(self):
        """Add initial/seed data to database"""
        
        try:
            async with self.db_config.AsyncSessionLocal() as session:
                # Check if we already have data
                from app.models.schemas import User
                result = await session.execute("SELECT COUNT(*) FROM users")
                user_count = result.scalar()
                
                if user_count > 0:
                    logger.info("Database already has data, skipping seed data")
                    return
                
                # Add default admin user
                from app.services.security import security_manager
                
                admin_user_data = {
                    "username": "admin",
                    "email": "admin@vyapaargpt.com",
                    "full_name": "VyapaarGPT Admin",
                    "business_name": "VyapaarGPT",
                    "phone": "919876543210",
                    "language_preference": "english",
                    "business_type": "technology",
                    "is_active": True,
                    "is_admin": True
                }
                
                # Encrypt sensitive data
                from app.services.security import compliance_manager
                processed_data = compliance_manager.process_customer_data(admin_user_data)
                
                admin_user = User(**processed_data)
                admin_user.hashed_password = security_manager.hash_password("admin123")
                
                session.add(admin_user)
                await session.commit()
                
                logger.info("Added default admin user")
                
        except Exception as e:
            logger.error(f"Error adding initial data: {e}")
    
    async def backup_database(self, backup_path: str = None) -> str:
        """Create database backup"""
        
        import subprocess
        from datetime import datetime
        
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backup_vyapaargpt_{timestamp}.sql"
        
        try:
            # Get database connection details
            db_user = os.getenv("DB_USER", "postgres")
            db_host = os.getenv("DB_HOST", "localhost")
            db_port = os.getenv("DB_PORT", "5432")
            db_name = os.getenv("DB_NAME", "vyapaargpt")
            
            # Create pg_dump command
            cmd = [
                "pg_dump",
                f"--host={db_host}",
                f"--port={db_port}",
                f"--username={db_user}",
                f"--dbname={db_name}",
                "--verbose",
                "--clean",
                "--no-owner",
                "--no-privileges",
                f"--file={backup_path}"
            ]
            
            # Set password environment variable
            env = os.environ.copy()
            env["PGPASSWORD"] = os.getenv("DB_PASSWORD", "password")
            
            # Run backup
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Database backup created: {backup_path}")
                return backup_path
            else:
                logger.error(f"Backup failed: {result.stderr}")
                raise Exception(f"Backup failed: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            raise
    
    async def restore_database(self, backup_path: str):
        """Restore database from backup"""
        
        import subprocess
        
        try:
            # Get database connection details
            db_user = os.getenv("DB_USER", "postgres")
            db_host = os.getenv("DB_HOST", "localhost")
            db_port = os.getenv("DB_PORT", "5432")
            db_name = os.getenv("DB_NAME", "vyapaargpt")
            
            # Create psql command
            cmd = [
                "psql",
                f"--host={db_host}",
                f"--port={db_port}",
                f"--username={db_user}",
                f"--dbname={db_name}",
                f"--file={backup_path}"
            ]
            
            # Set password environment variable
            env = os.environ.copy()
            env["PGPASSWORD"] = os.getenv("DB_PASSWORD", "password")
            
            # Run restore
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Database restored from: {backup_path}")
            else:
                logger.error(f"Restore failed: {result.stderr}")
                raise Exception(f"Restore failed: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Error restoring database: {e}")
            raise

# Global instances
db_config = DatabaseConfig()
db_manager = DatabaseManager(db_config)

# Dependency functions for FastAPI
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for async database sessions"""
    async with db_config.AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def get_db() -> Session:
    """FastAPI dependency for sync database sessions"""
    db = db_config.SessionLocal()
    try:
        yield db
    finally:
        db.close()