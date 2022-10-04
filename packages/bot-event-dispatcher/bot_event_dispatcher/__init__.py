from asyncio import get_event_loop


async def main():
    pass


def start():
    loop = get_event_loop()
    loop.run_until_complete(main())


__all__ = ["start"]

if __name__ == "__main__":
    start()
