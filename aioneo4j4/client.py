import asyncio
import collections

from yarl import URL

from .transport import Transport


class Client:

    def __init__(
        self,
        url='http://127.0.0.1:7474/',
        auth=None,
        transport=Transport,
        request_timeout=...,
        *, loop=None
    ):
        if loop is None:
            loop = asyncio.get_event_loop()

        self.loop = loop

        url = URL(url)

        if url.user and url.password:
            auth = url.user, url.password

            url = url.with_user(None)

            # TODO: not sure is it needed
            url = url.with_password(None)

        self.transport = transport(
            url=url,
            auth=auth,
            request_timeout=request_timeout,
            loop=self.loop,
        )


    async def begin_and_commit(
            self,
            cypher,
            db='neo4j',
            path='db/%s/tx/commit',
            request_timeout=...,
    ):

        _, data = await self.transport.perform_request(
            method='POST',
            path=path % db,
            data={
                "statements": [{
                    "statement": cypher,
                }]
            },
            request_timeout=request_timeout,
        )

        return data



    async def close(self):
        await self.transport.close()

    async def __aenter__(self):  # noqa
        return self

    async def __aexit__(self, *exc_info):  # noqa
        await self.close()
