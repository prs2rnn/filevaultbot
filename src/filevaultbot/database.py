import asyncio

import aiosqlite


class FileDatabase:
    def __init__(self, db_path='files.db'):
        self.db_path = db_path
        self.lock = asyncio.Lock()

    async def _ensure_tables_exist(self):
        async with self.lock:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    '''
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    unique_id TEXT UNIQUE NOT NULL,
                    original_id TEXT UNIQUE NOT NULL,
                    type TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    created_at REAL DEFAULT (strftime('%s', 'now'))
                )
                '''
                )
                await db.commit()

    async def add_file(self, unique_id: str, original_id: str, type: str, user_id: int):
        await self._ensure_tables_exist()
        async with self.lock:
            async with aiosqlite.connect(self.db_path) as db:
                try:
                    await db.execute(
                        'INSERT INTO files (unique_id, original_id, type, user_id) VALUES (?, ?, ?, ?)',
                        (unique_id, original_id, type, user_id),
                    )
                    await db.commit()
                    return True
                except aiosqlite.IntegrityError:
                    return False

    async def get_user_files(self, user_id: int):
        await self._ensure_tables_exist()
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                'SELECT original_id, type FROM files WHERE user_id = ? ORDER BY created_at DESC',
                (user_id,),
            )
            rows = await cursor.fetchall()
            return [{'original_id': row[0], 'type': row[1]} for row in rows]

    async def get_file_by_unique_id(self, unique_id: str):
        await self._ensure_tables_exist()
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                'SELECT original_id, type FROM files WHERE unique_id = ?', (unique_id,)
            )
            row = await cursor.fetchone()
            if row:
                return {'original_id': row[0], 'type': row[1]}


async def main():
    file_db = FileDatabase()
    success = await file_db.add_file(
        'asf24r23', '12afdf3e21', 'document', '1239210413u41'
    )
    print(success)
    files = await file_db.get_user_files('1239210413u41')
    print(files)


if __name__ == '__main__':
    asyncio.run(main())
