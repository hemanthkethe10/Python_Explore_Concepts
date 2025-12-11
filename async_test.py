import aiohttp
import asyncio

async def fetch(url):
    try:
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url) as response:
                return await response.json()
    except aiohttp.ClientError as e:
        print(f"Request failed for {url}: {e}")
        return None

async def main():
    urls = [
        'https://679b423633d3168463233736.mockapi.io/api/v1/users/1',
        'https://679b423633d3168463233736.mockapi.io/api/v1/users/2',
        'https://679b423633d3168463233736.mockapi.io/api/v1/users/3',
    ]

    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
        
    for result in results:
        print(result)

# Run the async main function
asyncio.run(main())