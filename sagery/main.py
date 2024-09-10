import argparse
import asyncio
import json
import logging


logging.basicConfig(level=logging.INFO)


async def worker():
    raise NotImplementedError


def create_job(job_name: str, kwargs: dict):
    raise NotImplementedError(job_name, kwargs)


def get_status(id_: str):
    raise NotImplementedError(id_)


def get_result(id_: str):
    raise NotImplementedError(id_)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', type=str)
    parser.add_argument('--args', type=str, default=None)
    parser.add_argument('--id', type=str, default=None)

    args = id_ = None
    arguments = parser.parse_args()
    if arguments.args is not None:
        args = json.loads(arguments.args)
    if arguments.id is not None:
        id_ = arguments.id

    match arguments.action:
        case 'worker':
            asyncio.run(worker())
        case 'create_job':
            if args is None:
                raise RuntimeError('No arguments')
            if 'job_name' not in args:
                raise RuntimeError('No job name in arguments')
            job_name = args.pop('job_name')
            create_job(job_name, args)
        case 'get_status':
            if id_ is None:
                raise RuntimeError('id must be specified')
            status = get_status(id_)
            print(status)
        case 'get_result':
            if id_ is None:
                raise RuntimeError('id must be specified')
            result = get_result(id_)
            print(result)
        case _:
            raise ValueError(f'Unknown action: {arguments.action}')
