# adf_github_cicd_repo

## Release configuration

Before running the release workflow, configure these repository settings:

- Secret `DATABRICKS_ACCESS_TOKEN`: a valid access token for the target Databricks workspace.
- Variable `DATABRICKS_CLUSTER_ID`: the existing cluster ID in that workspace.

`configs/adf_params_test.json` uses `{"env": "VARIABLE_NAME"}` entries to
resolve these values from the environment during ARM parameter generation.
Missing or empty environment values fail the update before deployment without
printing credentials. Literal config values continue to be used unchanged.