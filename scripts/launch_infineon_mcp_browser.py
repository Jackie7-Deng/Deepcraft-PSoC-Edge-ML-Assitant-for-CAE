from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_PROFILE_DIR = Path.home() / "AppData" / "Local" / "InfineonMCPBrowser"


def find_browser(explicit_path: str | None, browser: str) -> Path:
    if explicit_path:
        path = Path(explicit_path).expanduser()
        if path.is_file():
            return path
        raise FileNotFoundError(f"Browser executable not found: {path}")

    candidates: list[Path] = []
    program_files = [
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")),
        Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")),
        Path(os.environ.get("LocalAppData", str(Path.home() / "AppData" / "Local"))),
    ]

    if browser in ("chrome", "auto"):
        candidates.extend(
            [
                program_files[0] / "Google" / "Chrome" / "Application" / "chrome.exe",
                program_files[1] / "Google" / "Chrome" / "Application" / "chrome.exe",
                program_files[2] / "Google" / "Chrome" / "Application" / "chrome.exe",
            ]
        )

    if browser in ("edge", "auto"):
        candidates.extend(
            [
                program_files[0] / "Microsoft" / "Edge" / "Application" / "msedge.exe",
                program_files[1] / "Microsoft" / "Edge" / "Application" / "msedge.exe",
                program_files[2] / "Microsoft" / "Edge" / "Application" / "msedge.exe",
            ]
        )

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    raise FileNotFoundError(
        "No supported browser executable was found. "
        "Provide one with --browser-path or install Chrome/Edge."
    )


def build_command(
    browser_path: Path,
    profile_dir: Path,
    remote_debugging_port: int,
    start_url: str,
    headless: bool,
) -> list[str]:
    command = [
        str(browser_path),
        f"--user-data-dir={profile_dir}",
        f"--remote-debugging-port={remote_debugging_port}",
        "--no-first-run",
        "--no-default-browser-check",
    ]

    if headless:
        command.append("--headless=new")

    command.append(start_url)
    return command


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Launch a dedicated Chrome/Edge session for future MCP browser automation."
    )
    parser.add_argument(
        "--browser",
        choices=["auto", "chrome", "edge"],
        default="auto",
        help="Preferred browser family.",
    )
    parser.add_argument(
        "--browser-path",
        help="Explicit path to chrome.exe or msedge.exe.",
    )
    parser.add_argument(
        "--profile-dir",
        default=str(DEFAULT_PROFILE_DIR),
        help="Dedicated browser profile directory.",
    )
    parser.add_argument(
        "--remote-debugging-port",
        type=int,
        default=9222,
        help="Remote debugging port for later CDP/Playwright attachment.",
    )
    parser.add_argument(
        "--start-url",
        default="https://community.infineon.com",
        help="Initial page to open.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Launch in headless mode. Not recommended for first-time interactive login.",
    )
    args = parser.parse_args()

    profile_dir = Path(args.profile_dir).expanduser()
    profile_dir.mkdir(parents=True, exist_ok=True)

    try:
        browser_path = find_browser(args.browser_path, args.browser)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    command = build_command(
        browser_path=browser_path,
        profile_dir=profile_dir,
        remote_debugging_port=args.remote_debugging_port,
        start_url=args.start_url,
        headless=args.headless,
    )

    print("Launching browser:")
    print(f"  executable: {browser_path}")
    print(f"  profile:    {profile_dir}")
    print(f"  debug port: {args.remote_debugging_port}")
    print(f"  start url:  {args.start_url}")

    try:
        subprocess.Popen(command)
    except OSError as exc:
        print(f"Failed to launch browser: {exc}", file=sys.stderr)
        return 1

    print("\nNext steps:")
    print("1. Use this browser window for Community/Case login if needed.")
    print("2. Keep the browser session open.")
    print("3. Later let the MCP server attach to this profile or debug port.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
