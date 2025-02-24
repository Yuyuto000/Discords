import asyncio
from yuyuka_bot.bot import run_cute_bot
from yuyuto_bot.bot import run_cool_bot

async def main():
    await asyncio.gather(
        run_cute_bot(),
        run_cool_bot()
    )

if __name__ == "__main__":
    asyncio.run(main())