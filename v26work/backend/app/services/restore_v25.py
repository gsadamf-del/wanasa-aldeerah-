import os, subprocess, tempfile
from datetime import datetime

def run_restore_drill(source_backup: str, target_database: str, timeout: int = 300) -> dict:
    """Runs pg_restore against an isolated target. Intended for scheduled non-production drills."""
    if not source_backup or not target_database: raise ValueError('backup and target database are required')
    started=datetime.utcnow()
    cmd=['pg_restore','--exit-on-error','--no-owner','--dbname',target_database,source_backup]
    try:
        proc=subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
    except FileNotFoundError:
        return {'status':'NOT_RUN','verified':False,'reason':'pg_restore not installed','started_at':started.isoformat()}
    return {'status':'PASSED' if proc.returncode==0 else 'FAILED','verified':proc.returncode==0,'returncode':proc.returncode,'stderr':proc.stderr[-2000:],'started_at':started.isoformat()}
