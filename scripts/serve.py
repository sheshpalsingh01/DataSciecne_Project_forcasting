import hashlib
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml


DAGSHUB_ENDPOINT = "https://dagshub.com/sheshpalsingh2024/DataSciecne_Project_forcasting.s3"


def fetch_object(storage, digest: str, destination: Path):
    key = f"files/md5/{digest[:2]}/{digest[2:]}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=destination.parent) as directory:
        temporary = Path(directory) / destination.name
        storage.download_file("dvc", key, str(temporary))
        with temporary.open("rb") as downloaded:
            actual = hashlib.file_digest(downloaded, "md5").hexdigest()
        if actual != digest.removesuffix(".dir"):
            raise ValueError(f"DVC checksum mismatch for {destination}")
        temporary.replace(destination)
        print(f"Verified {destination.name}.", flush=True)


def fetch_artifacts(root: Path):
    import boto3
    from botocore.config import Config

    stages = yaml.safe_load((root / "dvc.lock").read_text())["stages"]
    transformation = next(
        output for output in stages["data_transformation"]["outs"]
        if output["path"] == "artifacts/data_transformation"
    )
    model, = stages["model_training"]["outs"]
    storage = boto3.client(
        "s3",
        endpoint_url=DAGSHUB_ENDPOINT,
        region_name="us-east-1",
        config=Config(connect_timeout=10, read_timeout=30, retries={"total_max_attempts": 3}),
    )

    with TemporaryDirectory() as directory:
        manifest_path = Path(directory) / "transformation.json"
        fetch_object(storage, transformation["md5"], manifest_path)
        entries = json.loads(manifest_path.read_text())
    preprocessor = next(entry for entry in entries if entry["relpath"] == "preprocessor.joblib")
    fetch_object(
        storage, preprocessor["md5"], root / transformation["path"] / preprocessor["relpath"]
    )
    fetch_object(storage, model["md5"], root / model["path"])
    print("Loaded both serving artifacts from DagsHub DVC storage.", flush=True)


if __name__ == "__main__":
    if os.environ.get("FORECAST_FETCH_ARTIFACTS") == "1":
        fetch_artifacts(Path.cwd())

    port = os.environ.get("PORT", "5000")
    os.execlp(
        "gunicorn", "gunicorn", "--bind", f"0.0.0.0:{port}",
        "--no-control-socket", "--worker-class", "gthread", "--threads", "2", "--access-logfile", "-", "app:app",
    )
