import os
from pathlib import Path
import logging

Project_name = "forcastingproject"

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"

)
logger = logging.getLogger(__name__)

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{Project_name}/__init__.py",
    f"src/{Project_name}/components/__init__.py",
    f"src/{Project_name}/utils/common.py",
    f"src/{Project_name}/utils/__init__.py",
    f"src/{Project_name}/config/__init__.py",
    f"src/{Project_name}/config/configuration.py",
    f"src/{Project_name}/entity/__init__.py",
    f"src/{Project_name}/pipeline/__init__py",
    f"src/{Project_name}/constants/__init__.py",
    f"src/{Project_name}/logging/__init__.py",
    # Monitoring
    f"src/{Project_name}/monitoring/__init__.py",
    f"src/{Project_name}/monitoring/model_monitoring.py",
    f"src/{Project_name}/monitoring/data_monitoring.py",
    "reports/file.txt",
    "data/raw.csv",
    "config/config.yaml",
    "params.yaml",
    "main.py",
    "templates/index.html",
    "Dockerfile",
    "requirements.txt",
    "research/exprements.ipynb",
    "app.py",
    "docker-compose.yaml",
    ".dockerignore",
    
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir,filename = os.path.split(filepath)

    if filedir!="":
        os.makedirs(filedir, exist_ok=True)

        logging.info(f"Directory Created : {filedir} for th file {filename}")

    if (not os.path.exists(filepath)) or( os.path.getsize(filepath)==0):
        with open(filepath,"w") as f:
            pass
        logging.info(f"Empty file created : {filepath}")
    else:
        logging.info(f"file already exists : {filepath}")


