import argparse
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call the transformed orders endpoint and save CSV to Downloads."
    )
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
        help="Base URL where the Django app is running.",
    )
    parser.add_argument(
        "--output",
        default=str(Path.home() / "Downloads" / "transformed_order_data.csv"),
        help="Output CSV path.",
    )
    return parser.parse_args()


def fetch_csv(base_url: str) -> bytes:
    endpoint = f"{base_url.rstrip('/')}/get-all-transformed-orders"
    with urlopen(endpoint, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"Request failed with status {response.status}: {endpoint}")
        return response.read()


def write_csv(csv_bytes: bytes, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_bytes(csv_bytes)


def main() -> None:
    args = parse_args()
    output_file = Path(args.output)

    try:
        csv_bytes = fetch_csv(args.base_url)
        write_csv(csv_bytes, output_file)
    except (HTTPError, URLError, RuntimeError) as exc:
        raise SystemExit(f"CSV export failed: {exc}") from exc

    print(f"CSV saved to {output_file}")


if __name__ == "__main__":
    main()