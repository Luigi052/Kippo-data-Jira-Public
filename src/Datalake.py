import pandas as pd
from azure.storage.blob import BlockBlobService
from datetime import datetime
import config
from log_manager import log_info, log_error


def load_project_data(project_data):
    project_info = project_data['project_info']
    roles = project_data.get('roles', {})
    versions = project_data.get('versions', [])
    issues = project_data.get('issues', [])

    df_project_info = pd.DataFrame([project_info])
    df_roles = pd.DataFrame([roles])
    df_versions = pd.DataFrame(versions)
    df_issues = pd.DataFrame(issues)

    df_combined = pd.concat([df_project_info, df_roles, df_versions, df_issues], axis=1)

#    print(df_combined)

    return df_combined


def upload_to_datalake(df, project_id):
    try:
        now = datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%m')
        day = now.strftime('%d')

        file_path = f"jira/{year}/{month}/{day}/{project_id}/data.json"

        block_blob_service = BlockBlobService(
            account_name=config.AZURE_STORAGE_ACCOUNT_NAME,
            account_key=config.AZURE_STORAGE_ACCOUNT_KEY
        )
        container_name = config.AZURE_CONTAINER_NAME

        blob_content = df.to_json(orient='records', lines=False)
        block_blob_service.create_blob_from_text(container_name, file_path, blob_content)

        log_info(f"Dados enviados ao Azure DataLake como {file_path}")

    except Exception as e:
        log_error(f"Erro ao enviar dados ao Azure DataLake: {e}")


def save_data(data, project_id):
    try:
        df_combined = load_project_data(data)

        if config.LOCAL_SAVE:
            from save_json import save_data_to_json
            save_data_to_json(data, project_id)

        if config.CLOUD_SAVE:
            upload_to_datalake(df_combined, project_id)

    except Exception as e:
        log_error(f"Erro ao processar dados do projeto {project_id}: {e}")
