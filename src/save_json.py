import json
import os
from src import config
from src.log_manager import log_info, log_error


def custom_json_serializer(obj):
    if hasattr(obj, 'raw'):
        return obj.raw
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def create_project_save_path():
    try:
        save_path = os.path.join(config.SAVE_PATH, "jira")
        os.makedirs(save_path, exist_ok=True)
        log_info(f"Diretório de salvamento criado: {save_path}")
        return save_path
    except Exception as e:
        log_error(f"Erro ao criar diretório de salvamento: {e}")
        raise


def save_data_to_json(data, project_id):
    try:
        save_path = create_project_save_path()
        full_path = os.path.join(save_path, f"{project_id}.json")
        with open(full_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, default=custom_json_serializer, ensure_ascii=False)
        log_info(f"Dados do projeto {project_id} salvos com sucesso em: {full_path}")
        return full_path
    except Exception as e:
        log_error(f"Erro ao salvar dados do projeto {project_id}: {e}")
        raise
