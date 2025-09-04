# from .latergate import app
# import .latergate as latergate
import uvicorn
import argparse
from dotenv import load_dotenv
import os
import tomllib

def get_args():
    parser = argparse.ArgumentParser(description='latergate')
    parser.add_argument('-p', '--port', type=int, default=int(os.getenv('LG_PORT', '8901')), help='port')
    parser.add_argument('--host', default=os.getenv('LG_HOST', '0.0.0.0'), help='port')
    parser.add_argument('-c', '--config', default=os.getenv('LG_CONFIG','latergate.toml'), help='Path to latergate.toml')

    args = parser.parse_args()
    return args


def main():
    load_dotenv()
    args = get_args()

    os.environ["LG_CONFIG"] = args.config

    print(f"Running LaterGate on {args.host}:{args.port}")
    uvicorn.run(
        "latergate.latergate:app",
        host=args.host,
        port=args.port,
        reload=True
    )
