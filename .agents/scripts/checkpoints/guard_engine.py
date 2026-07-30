import hashlib
import os
import shutil

def compute_scoped_hash(target_files: list[str]) -> str:
    """Computes a SHA-256 hash strictly over the specified target files."""
    hasher = hashlib.sha256()
    for file_path in sorted(target_files):
        if os.path.exists(file_path):
            hasher.update(file_path.encode('utf-8'))
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
        else:
            hasher.update(f"MISSING:{file_path}".encode('utf-8'))
    return hasher.hexdigest()

def create_snapshot(target_files: list[str], snapshot_dir: str) -> None:
    """Creates a backup snapshot of specified target files into snapshot_dir."""
    if os.path.exists(snapshot_dir):
        shutil.rmtree(snapshot_dir)
    os.makedirs(snapshot_dir, exist_ok=True)
    
    for file_path in target_files:
        if os.path.exists(file_path):
            rel_name = os.path.basename(file_path)
            dest_path = os.path.join(snapshot_dir, rel_name)
            shutil.copy2(file_path, dest_path)

def verify_staleness(target_files: list[str], expected_hash: str) -> bool:
    """Returns True if current hash matches expected_hash (no drift). Returns False if drifted."""
    current_hash = compute_scoped_hash(target_files)
    return current_hash == expected_hash

def rollback_snapshot(snapshot_dir: str, target_files: list[str]) -> None:
    """Restores target_files from snapshot_dir."""
    for file_path in target_files:
        rel_name = os.path.basename(file_path)
        dest_path = os.path.join(snapshot_dir, rel_name)
        if os.path.exists(dest_path):
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            shutil.copy2(dest_path, file_path)
