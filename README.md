# Jira Data Collector

## Description
The **Jira Data Collector** is a project that collects data from multiple projects, including details about **issues**, **boards**, **sprints**, **dashboards**, **roles**, and much more. The collected data is saved in JSON format, making it easy to analyze and integrate into data lakes or BI systems. The data can be saved locally or in Azure Cloud Storage, depending on your configuration.

## Features
- Collection of all Jira projects.
- Detailed issue collection, including:
  - Issue details (status, priority, assignee, etc.).
  - Comments.
  - Worklogs.
  - Changelogs.
  - Attachments.
- Collection of boards and sprints.
- Collection of dashboards, custom fields, and policies.
- Support for pagination for large volumes of data.
- Detailed logs of operations performed.
- Option to save data locally or to Azure Cloud Storage.

## Project Structure
- **data_collector.py**: Manages the data collection of all projects and their associated entities (issues, boards, etc.).
- **main.py**: Main script that executes the data collection process.
- **save_json.py**: Functions to save the collected data in JSON format, with support for automatic directory creation and cloud storage.
- **log_manager.py**: Manages the logging system, allowing detailed records during the process.
- **config.py**: Configuration file where the Jira URL, credentials, and execution parameters such as the save directory and cloud settings are defined.

## Requirements
- **Python 3.x**
- Required libraries:
  - `jira`
  - `requests`
  - `json`
  - `logging`
  - `azure-storage-blob` (if using Azure Cloud Storage)

You can install the dependencies using the following command:
```bash
pip install jira requests azure-storage-blob
```

## Configuration
In the `config.py` file, configure the following parameters:

### Jira Settings
- **JIRA_BASE_URL**: Your Jira URL (e.g., `https://your-jira.atlassian.net`).
- **USER_EMAIL**: Your Jira authentication email.
- **JIRA_API_TOKEN**: The API token generated for authentication.

### Azure Storage Settings (Optional)
- **AZURE_STORAGE_ACCOUNT_NAME**: Your Azure Storage account name.
- **AZURE_STORAGE_ACCOUNT_KEY**: Your Azure Storage account key.
- **AZURE_CONTAINER_NAME**: The name of the Azure Storage container where data will be saved.

### Save Options
- **SAVE_PATH**: The path where the JSON files will be saved locally (e.g., `'../output/json'`).
- **ENABLE_LOGGING**: Enable or disable logging (`True`/`False`).
- **CONSOLE_LOG**: Enable or disable logging to console (`True`/`False`).
- **LOG_PATH**: The path where log files will be saved (e.g., `'../output/logs'`).
- **LOCAL_SAVE**: Set to `True` to save data locally.
- **CLOUD_SAVE**: Set to `True` to save data to Azure Cloud Storage.

Example of `config.py`:
```python
JIRA_BASE_URL = "https://your-jira.atlassian.net"
USER_EMAIL = "your-email@domain.com"
JIRA_API_TOKEN = "your-api-token"

###########

AZURE_STORAGE_ACCOUNT_NAME = ''
AZURE_STORAGE_ACCOUNT_KEY = ''
AZURE_CONTAINER_NAME = ''

#############

SAVE_PATH = '../output/json'
ENABLE_LOGGING = True
CONSOLE_LOG = True
LOG_PATH = '../output/logs'
LOCAL_SAVE = True
CLOUD_SAVE = False
```

**Note:** If you set `CLOUD_SAVE = True`, ensure that you provide the Azure Storage account details. If `LOCAL_SAVE` and `CLOUD_SAVE` are both set to `True`, the data will be saved both locally and to Azure Cloud Storage.

## How to Run
1. **Configure Settings:**
   - Open `config.py` and ensure all settings are correctly configured.
   - For **local saving**, set `LOCAL_SAVE = True` and specify `SAVE_PATH`.
   - For **Azure Cloud saving**, set `CLOUD_SAVE = True` and provide Azure Storage account details:
     - `AZURE_STORAGE_ACCOUNT_NAME`
     - `AZURE_STORAGE_ACCOUNT_KEY`
     - `AZURE_CONTAINER_NAME`

2. **Install Dependencies:**
   - Install required Python libraries:
     ```bash
     pip install jira requests azure-storage-blob
     ```

3. **Run the Script:**
   ```bash
   python main.py
   ```
4. **Data Storage:**
   - **Local:** Data will be saved in JSON format in the directory specified by `SAVE_PATH`.
   - **Azure Cloud:** Data will be uploaded to the specified Azure Storage container.

## Logs
- **Logging Options:**
  - **ENABLE_LOGGING:** Set to `True` to enable logging to a file.
  - **CONSOLE_LOG:** Set to `True` to enable logging output to the console.
- **Log Files:**
  - Logs are saved in the directory specified by `LOG_PATH`.
  - Log files include detailed information about the data collection process, which aids in monitoring and troubleshooting.

## Azure Cloud Storage Configuration (Optional)
If you choose to save data to Azure Cloud Storage, ensure the following:

1. **Azure Account:**
   - You have an active Azure subscription.
   - An Azure Storage account is created.

2. **Create a Storage Container:**
   - Log in to the [Azure Portal](https://portal.azure.com/).
   - Navigate to your Storage Account.
   - Create a new container (e.g., `jira-data`).

3. **Set Access Keys:**
   - In your Storage Account, go to **Access keys**.
   - Retrieve your **Storage account name** and **key**.
   - Update `AZURE_STORAGE_ACCOUNT_NAME` and `AZURE_STORAGE_ACCOUNT_KEY` in `config.py`.

## Troubleshooting
- **Authentication Errors:**
  - Ensure that `USER_EMAIL` and `JIRA_API_TOKEN` are correct.
  - For Jira Cloud, you need to generate an API token from your Atlassian account.

- **Azure Storage Errors:**
  - Verify that the Azure Storage account details are correct.
  - Ensure that the network allows outbound connections to Azure Storage endpoints.

- **Permission Issues:**
  - Ensure you have the necessary permissions to access Jira projects and Azure Storage containers.

- **Missing Libraries:**
  - Install all required libraries using `pip install` as shown in the **Requirements** section.

## Additional Notes
- **Data Privacy:** Be cautious with sensitive data. Ensure compliance with your organization's data handling policies.
- **Performance Considerations:** Collecting large amounts of data may take time. You can implement multithreading or batching to improve performance.
- **Extendibility:** The project is modular, allowing you to add more features like data transformation or integration with other cloud providers.

---

**Note:** The application includes detailed logging and error handling to assist with monitoring the data collection process and troubleshooting any issues that may arise.