"""Temporary WSL-to-Windows TCP bridge for Brave CDP.

Run this script with Windows Python. Bind only to the WSL virtual-interface
address, never 0.0.0.0, so the debugging endpoint is not exposed to the LAN.
"""

from __future__ import annotations

import argparse
import socket
import threading


BUFFER_SIZE = 64 * 1024


def copy_stream(source: socket.socket, target: socket.socket) -> None:
    try:
        while data := source.recv(BUFFER_SIZE):
            target.sendall(data)
    except OSError:
        pass
    finally:
        try:
            target.shutdown(socket.SHUT_WR)
        except OSError:
            pass


def handle_client(client: socket.socket, target_host: str, target_port: int) -> None:
    upstream: socket.socket | None = None
    try:
        upstream = socket.create_connection((target_host, target_port), timeout=10)
        left = threading.Thread(target=copy_stream, args=(client, upstream), daemon=True)
        right = threading.Thread(target=copy_stream, args=(upstream, client), daemon=True)
        left.start()
        right.start()
        left.join()
        right.join()
    finally:
        client.close()
        if upstream is not None:
            upstream.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--listen-address", required=True)
    parser.add_argument("--listen-port", type=int, default=9223)
    parser.add_argument("--target-address", default="127.0.0.1")
    parser.add_argument("--target-port", type=int, default=9222)
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((args.listen_address, args.listen_port))
        listener.listen(16)
        print(
            f"CDP proxy listening on {args.listen_address}:{args.listen_port} "
            f"-> {args.target_address}:{args.target_port}",
            flush=True,
        )
        while True:
            client, _ = listener.accept()
            threading.Thread(
                target=handle_client,
                args=(client, args.target_address, args.target_port),
                daemon=True,
            ).start()


if __name__ == "__main__":
    main()
