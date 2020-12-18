import asyncio

from aioneo4j4 import Neo4j


async def go():
    async with Neo4j('http://neo4j:123456@127.0.0.1:7474/') as neo4j:
        data = await neo4j.begin_and_commit("match n return count(n)")

        assert bool(data)


loop = asyncio.get_event_loop()
loop.run_until_complete(go())
loop.close()