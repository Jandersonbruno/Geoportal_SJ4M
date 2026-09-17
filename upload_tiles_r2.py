"""
Sobe os tiles da ortofoto (guardados em Ortofoto_4M.mbtiles) para um bucket
Cloudflare R2, como objetos soltos {z}/{x}/{y}.jpg -- prontos para o Leaflet
consumir via L.tileLayer('https://<sua-url-publica>/{z}/{x}/{y}.jpg').

Requer as credenciais da API do R2 como variaveis de ambiente (nunca
digitadas no codigo nem compartilhadas no chat):

    $env:R2_ACCESS_KEY_ID = "..."
    $env:R2_SECRET_ACCESS_KEY = "..."
    python upload_tiles_r2.py

Ajuste ACCOUNT_ID e BUCKET_NAME abaixo se forem diferentes.
"""
import os
import sqlite3
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import boto3
from botocore.config import Config

ACCOUNT_ID = "8fd0fcb8080470ed7f8dce17bbc8b6f3"
BUCKET_NAME = "geoportal-sj4m-tiles"
MBTILES_PATH = r"E:\GEOPORTAL_SJ4M\IMG\Ortofoto_4M.mbtiles"
ENDPOINT_URL = f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com"
CONCURRENCY = 48

access_key = os.environ.get("R2_ACCESS_KEY_ID")
secret_key = os.environ.get("R2_SECRET_ACCESS_KEY")
if not access_key or not secret_key:
    print("ERRO: defina R2_ACCESS_KEY_ID e R2_SECRET_ACCESS_KEY como variaveis de ambiente antes de rodar.")
    sys.exit(1)

s3 = boto3.client(
    "s3",
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    config=Config(signature_version="s3v4", max_pool_connections=CONCURRENCY + 8),
    region_name="auto",
)


def load_tiles():
    conn = sqlite3.connect(MBTILES_PATH)
    cur = conn.cursor()
    cur.execute("SELECT zoom_level, tile_column, tile_row, tile_data FROM tiles")
    rows = cur.fetchall()
    conn.close()
    return rows


def upload_one(z, x, tms_row, data):
    xyz_y = (2 ** z) - 1 - tms_row  # mbtiles stores TMS row order; XYZ (Leaflet) wants it flipped back
    key = f"{z}/{x}/{xyz_y}.jpg"
    s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=data, ContentType="image/jpeg", CacheControl="public, max-age=31536000, immutable")
    return key


def main():
    print("Lendo tiles do mbtiles...", flush=True)
    rows = load_tiles()
    total = len(rows)
    print(f"{total} tiles para enviar. Iniciando upload com {CONCURRENCY} conexoes simultaneas...", flush=True)

    done = 0
    errors = 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        futures = [pool.submit(upload_one, z, x, tms_row, data) for (z, x, tms_row, data) in rows]
        for fut in as_completed(futures):
            try:
                fut.result()
            except Exception as e:
                errors += 1
                if errors <= 20:
                    print(f"ERRO num upload: {e}", flush=True)
            done += 1
            if done % 2000 == 0:
                elapsed = time.time() - t0
                rate = done / elapsed if elapsed > 0 else 0
                eta = (total - done) / rate if rate > 0 else 0
                print(f"{done}/{total} enviados ({elapsed:.0f}s, {rate:.0f}/s, ETA {eta/60:.1f} min, {errors} erros)", flush=True)

    elapsed = time.time() - t0
    print(f"CONCLUIDO: {done}/{total} tiles em {elapsed/60:.1f} min, {errors} erros.", flush=True)


if __name__ == "__main__":
    main()
