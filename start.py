#! /usr/bin/env python3
import asyncio
import os
from subprocess import run
from watchgod import awatch

base = os.getcwd()

def run_build():
  run(f"{base}/build.py")

async def watch_and_build():
  async for _ in awatch(f"{base}/src"):
    print("[watcher] Changes detected, reloading!")
    run_build()

async def serve_dist():
  proc = await asyncio.create_subprocess_exec(*["npx", "serve", "dist"])
  await proc.wait()

async def main():
  run_build()
  watcher_task = asyncio.create_task(watch_and_build())
  server_task = asyncio.create_task(serve_dist())

  _, pending = await asyncio.wait(
    [watcher_task, server_task],
    return_when=asyncio.FIRST_COMPLETED
  )

  for task in pending:
    task.cancel()

try:
  asyncio.run(main())
except KeyboardInterrupt:
  print("\n[devserver] Caught Ctrl+C, exiting.")