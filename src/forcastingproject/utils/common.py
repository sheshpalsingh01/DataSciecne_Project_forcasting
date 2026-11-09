import yaml
import  os,sys
import json
import pickle, joblib
from pathlib import Path
try:
    from src.forcastingproject.logging.logger import logger
except ModuleNotFoundError:
    try:
        from forcastingproject.logging.logger import logger
    except ModuleNotFoundError:
        from ..logging.logger import logger

try:
    from src.forcastingproject.exception.exception import CustomException
except ModuleNotFoundError:
    try:
        from forcastingproject.exception.exception import CustomException
    except ModuleNotFoundError:
        from ..exception.exception import CustomException

from ensure import ensure_annotations
from typing_extensions import Any


@ensure_annotations
def read_yaml_file(file_path: Path) -> dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            content = yaml.safe_load(yaml_file)
            return content if content is not None else {}
    except Exception as e:
        raise CustomException(e, sys)


@ensure_annotations
def write_yaml_file(file_path:str,content:object,replace:bool=False):
    try:
        if replace:
            if os.path.exists(file_path):
                logger.info(f"file is already exists")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as yaml_file:
            yaml.dump(content,yaml_file)
    except Exception as e:
        raise CustomException(e,sys)


@ensure_annotations
def create_directories(path_to_dir:list,verbose:bool=True):
    try:
        for path in path_to_dir:
            os.makedirs(path,exist_ok=True)
            if verbose:
                logger.info(f"Created directory: {path}")
    except Exception as e:
        raise CustomException(e,sys)

@ensure_annotations
def save_json(path:Path,data:dict):
    try:
        with open(path,"w") as json_file:
            json.dump(data,json_file)
    except Exception as e:
        raise CustomException(e,sys)

@ensure_annotations
def load_json(path:Path)->dict:
    try:
        with open(path,"r") as json_file:
            return json.load(json_file)
    except Exception as e:
        raise CustomException(e,sys)

@ensure_annotations
def save_bin(data:Any,path:Path):
    try:
        data = joblib.dump(data,path)
        logger.info(f"saved data to {path}")
    except Exception as e:
        raise CustomException(e,sys)

@ensure_annotations
def load_bin(path:Path):
    try:
        data = joblib.load(path)
        logger.info(f"loaded data from {path}")
        return data
    except Exception as e:
        raise CustomException(e,sys)