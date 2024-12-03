from jira import JIRA, JIRAError
from log_manager import log_info, log_error
import config
from typing import List


class DataCollector:
    def __init__(self):
        try:
            options = {
                "headers": {
                    "User-Agent": "meu_pacote/1.0.0"
                }
            }
            self.jira = JIRA(
                server=config.JIRA_BASE_URL,
                basic_auth=(config.USER_EMAIL, config.JIRA_API_TOKEN),
                options=options
            )
            log_info("Autenticação no Jira realizada com sucesso.")
        except JIRAError as e:
            log_error(f"Erro ao autenticar no Jira: {e}")

    def collect_projects_modified_today(self) -> List:
        try:
            projects = self.jira.projects()
            modified_projects = []

            log_info(f"Projetos obtidos: {[project.key for project in projects]}")

            for project in projects:
                try:
                    # Usando project.key ao invés de project.id para a consulta JQL
                    jql_query = f'project="{project.key}" AND (created >= -1d OR updated >= -1d)'
                    log_info(f"Executando JQL para o projeto: {project.key}")

                    issues = self.jira.search_issues(jql_query, maxResults=1)

                    if issues:
                        modified_projects.append(project)

                except JIRAError as e:
                    log_error(f"Erro ao executar JQL para o projeto {project.key}: {e}")
                    continue

            log_info(f"{len(modified_projects)} projetos com modificações nas últimas 24 horas.")
            return modified_projects
        except JIRAError as e:
            log_error(f"Erro ao coletar projetos modificados no último dia: {e}")
            return []

    def collect_modified_issues(self, project_id):
        try:
            jql_query = f'project={project_id} AND (created >= -1d OR updated >= -1d)'
            issues = self.jira.search_issues(jql_query)
            log_info(f"Issues modificadas do projeto {project_id} coletadas.")
            return issues
        except JIRAError as e:
            log_error(f"Erro ao coletar issues modificadas do projeto {project_id}: {e}")
            return []

    def collect_project_roles(self, project_id):
        try:
            roles = self.jira.project_roles(project_id)
            log_info(f"Funções do projeto {project_id} coletadas.")
            return roles
        except JIRAError as e:
            log_error(f"Erro ao coletar funções do projeto {project_id}: {e}")
            return []

    def collect_project_versions(self, project_id):
        try:
            versions = self.jira.project_versions(project_id)
            log_info(f"Versões do projeto {project_id} coletadas.")
            return versions
        except JIRAError as e:
            log_error(f"Erro ao coletar versões do projeto {project_id}: {e}")
            return []

    def collect_policies(self, project_id):
        try:
            project = self.jira.project(project_id)
            policies = getattr(project, 'projectCategory', None)
            log_info(f"Políticas do projeto {project_id} coletadas.")
            return policies
        except JIRAError as e:
            log_error(f"Erro ao coletar políticas do projeto {project_id}: {e}")
            return []

    def collect_issue_details(self, issue_id):
        try:
            issue = self.jira.issue(issue_id)
            log_info(f"Detalhes da issue {issue_id} coletados.")
            return {
                "id": issue.id,
                "key": issue.key,
                "summary": issue.fields.summary,
                "status": issue.fields.status.name,
                "priority": issue.fields.priority.name if issue.fields.priority else None,
                "reporter": issue.fields.reporter.displayName if issue.fields.reporter else None,
                "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None
            }
        except JIRAError as e:
            log_error(f"Erro ao coletar detalhes da issue {issue_id}: {e}")
            return None

    def collect_issue_comments(self, issue_id):
        try:
            comments = self.jira.comments(issue_id)
            log_info(f"Comentários da issue {issue_id} coletados.")
            return [{"author": comment.author.displayName, "body": comment.body} for comment in comments]
        except JIRAError as e:
            log_error(f"Erro ao coletar comentários da issue {issue_id}: {e}")
            return []

    def collect_issue_worklogs(self, issue_id):
        try:
            worklogs = self.jira.worklogs(issue_id)
            log_info(f"Worklogs da issue {issue_id} coletados.")
            return [{"author": worklog.author.displayName, "timeSpent": worklog.timeSpent} for worklog in worklogs]
        except JIRAError as e:
            log_error(f"Erro ao coletar worklogs da issue {issue_id}: {e}")
            return []

    def collect_issue_changelog(self, issue_id):
        try:
            changelog = self.jira.issue(issue_id, expand='changelog').changelog
            log_info(f"Changelog da issue {issue_id} coletado.")
            return [{
                "author": history.author.displayName,
                "items": [{"field": item.field, "fromString": item.fromString, "toString": item.toString}
                          for item in history.items]
            } for history in changelog.histories]
        except JIRAError as e:
            log_error(f"Erro ao coletar changelog da issue {issue_id}: {e}")
            return []

    def collect_issue_attachments(self, issue_id):
        try:
            issue = self.jira.issue(issue_id)
            attachments = issue.fields.attachment
            log_info(f"Anexos da issue {issue_id} coletados.")
            return [{"filename": attachment.filename, "size": attachment.size, "author": attachment.author.displayName}
                    for attachment in attachments]
        except JIRAError as e:
            log_error(f"Erro ao coletar anexos da issue {issue_id}: {e}")
            return []

    def collect_boards(self, project_id):
        try:
            boards = self.jira.boards()
            log_info(f"Boards coletados.")
            return boards
        except JIRAError as e:
            log_error(f"Erro ao coletar boards: {e}")
            return []

    def collect_dashboards(self):
        try:
            dashboards = self.jira.dashboards()
            log_info("Dashboards coletados.")
            return dashboards
        except JIRAError as e:
            log_error(f"Erro ao coletar dashboards: {e}")
            return []

    def collect_custom_fields(self):
        try:
            fields = self.jira.fields()
            log_info("Campos customizados coletados.")
            return fields
        except JIRAError as e:
            log_error(f"Erro ao coletar campos customizados: {e}")
            return []

    def collect_users(self):
        try:
            query = 'query'
            users = self.jira.search_users(query=query)
            log_info("Usuários coletados.")
            return [{"displayName": user.displayName, "emailAddress": user.emailAddress} for user in users]
        except JIRAError as e:
            log_error(f"Erro ao coletar usuários: {e}")
            return []
