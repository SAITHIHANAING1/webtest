#!/usr/bin/env python3
# deploy.py — zero-arg friendly generator for Docker deploy on Render.

from __future__ import annotations
import argparse, os, re, sys
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent

DOCKERFILE = dedent("""\
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
COPY ../requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
COPY . /app
ENV PORT=8080
CMD exec gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 3 --threads 8 --timeout 120
""")

RENDER_YAML = dedent("""\
services:
  - type: web
    name: safestep
    runtime: docker
    dockerfilePath: ./Dockerfile
    plan: free
    autoDeploy: true
    envVars:
      - key: SECRET_KEY
        sync: false
      - key: DATABASE_URL
        sync: false
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_ANON_KEY
        sync: false
      - key: SUPABASE_SERVICE_KEY
        sync: false
      - key: SESSION_COOKIE_SECURE
        value: "true"
      - key: GEMINI_API_KEY
        sync: false
""")

ENV_EXAMPLE = dedent("""\
SECRET_KEY=change_me
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DBNAME
SUPABASE_URL=https://YOUR_PROJECT.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_role_key
SESSION_COOKIE_SECURE=true
GEMINI_API_KEY=
""")

NEEDED = ["gunicorn", "psycopg2-binary"]

def read_reqs(p: Path) -> list[str]:
    if not p.exists():
        p.write_text("Flask\ngunicorn\npsycopg2-binary\n", encoding="utf-8")
    return [ln.rstrip("\n") for ln in p.read_text(encoding="utf-8").splitlines()]

def ensure(lines: list[str], pkgs: list[str]) -> list[str]:
    have = {re.split(r"[<>= ]", ln.strip(), 1)[0].lower()
            for ln in lines if ln.strip() and not ln.strip().startswith("#")}
    for pkg in pkgs:
        if pkg.lower() not in have:
            lines.append(pkg)
    return lines

def write(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force: return
    path.write_text(content, encoding="utf-8")

def make_files(fix_reqs: bool, force: bool):
    req = ROOT / "requirements.txt"
    lines = read_reqs(req)
    if fix_reqs:
        lines = ensure(lines, NEEDED)
        req.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # Docker + render.yaml + env example
    write(ROOT / "Dockerfile", DOCKERFILE, force)
    write(ROOT / "render.yaml", RENDER_YAML, force)
    write(ROOT / ".env.example", ENV_EXAMPLE, force)
    print("[ok] Wrote Dockerfile, render.yaml, .env.example")
    print("[ok] requirements.txt checked" + (" (updated)" if fix_reqs else ""))

def parse_args(argv):
    p = argparse.ArgumentParser(description="Prepare Flask app for Render (Docker)")
    sub = p.add_subparsers(dest="cmd")  # not required; we'll default to 'render'
    pr = sub.add_parser("render", help="Generate Dockerfile + render.yaml")
    pr.add_argument("--fix-reqs", action="store_true", help="Ensure gunicorn/psycopg2-binary in requirements.txt")
    pr.add_argument("--force", action="store_true", help="Overwrite existing files")
    pc = sub.add_parser("check", help="Print advice")
    return p.parse_args(argv)

def main():
    args = parse_args(sys.argv[1:])
    # Default to 'render' if no subcommand was given
    if not getattr(args, "cmd", None):
        print("[info] No subcommand provided; defaulting to 'render'.")
        args.cmd = "render"
        args.fix_reqs = True
        args.force = False
    if args.cmd == "render":
        make_files(fix_reqs=getattr(args, "fix_reqs", False), force=getattr(args, "force", False))
        print("\nNext steps:\n  git add Dockerfile render.yaml .env.example requirements.txt\n  git commit -m \"deploy: add Dockerfile + render.yaml\"\n  # Connect repo to Render → Web Service (runtime: docker) and set env vars.")
    elif args.cmd == "check":
        req = read_reqs(ROOT / "requirements.txt")
        print(f"scikit-learn present: {'yes' if any(ln.lower().startswith(('scikit-learn','sklearn')) for ln in req) else 'no'}")
        print("Recommended: gunicorn, psycopg2-binary")
    else:
        print("Unknown command")
        sys.exit(2)

if __name__ == "__main__":
    main()
