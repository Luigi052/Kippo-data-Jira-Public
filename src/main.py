from data_collector import DataCollector
from Datalake import save_data
from log_manager import setup_logging, log_info, log_error

def main():
    setup_logging()
    log_info("Iniciando o processo de coleta de dados.")

    try:
        collector = DataCollector()
        projects = collector.collect_projects_modified_today()
        log_info(f"{len(projects)} projetos modificados ou criados no último dia foram coletados.")

        for project in projects:
            project_id = project.id
            project_data = {
                "project_info": {
                    "id": project.id,
                    "key": project.key,
                    "name": project.name
                },
                "roles": collector.collect_project_roles(project_id),
                "versions": collector.collect_project_versions(project_id),
                "issues": [],
                "audit_logs": None,
                "boards": collector.collect_boards(project_id),
                "policies": collector.collect_policies(project_id),
                "dashboards": collector.collect_dashboards(),
                "custom_fields": collector.collect_custom_fields(),
                "users": collector.collect_users()
            }

            issues = collector.collect_modified_issues(project_id)
            for issue in issues:
                issue_id = issue.id
                issue_data = {
                    "issue_info": collector.collect_issue_details(issue_id),
                    "comments": collector.collect_issue_comments(issue_id),
                    "worklogs": collector.collect_issue_worklogs(issue_id),
                    "changelog": collector.collect_issue_changelog(issue_id),
                    "attachments": collector.collect_issue_attachments(issue_id)
                }
                project_data["issues"].append(issue_data)

            save_data(project_data, project_id)
            log_info(f"Dados do projeto {project_id} processados com sucesso.")

        log_info("Coleta de dados concluída com sucesso.")

    except Exception as e:
        log_error(f"Erro durante o processo de coleta de dados: {e}")

if __name__ == "__main__":
    main()
