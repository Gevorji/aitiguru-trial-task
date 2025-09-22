import asyncio

from sqlalchemy import text

from task3.create_db_tables import engine


async def exec_commands(commands):
    async with engine.begin() as conn:
        for command in commands:
            await conn.execute(command)


if __name__ == '__main__':
    import sys

    script_name = sys.argv[1]

    commands = [text(stmt) for stmt in open(script_name).read().split(';')]

    asyncio.run(exec_commands(commands))
