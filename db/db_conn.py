from psycopg_pool import AsyncConnectionPool

# todo: прописать в самой функции, или прокинуть через settings
DB_POOL = None
DB_POOL_OPEN = False

# todo: лучше разделить на получение pool и на генератор сессий
async def get_pool(
    conninfo,
    min_size=2,
    max_size=5,
    open_pool=False,
):
    global DB_POOL, DB_POOL_OPEN

    if DB_POOL is None:
        DB_POOL = AsyncConnectionPool(
            conninfo=conninfo,
            min_size=min_size,
            max_size=max_size,
        )

    if open_pool and not DB_POOL_OPEN:
        await DB_POOL.open()
        DB_POOL_OPEN = True

    return DB_POOL
