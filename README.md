# adf_github_cicd_repo

## Release configuration

Before running the release workflow, configure these repository settings:

- Secret `DATABRICKS_ACCESS_TOKEN`: a valid access token for the target Databricks workspace.
- Variable `DATABRICKS_CLUSTER_ID`: the existing cluster ID in that workspace.

`configs/adf_params_test.json` uses `{"env": "VARIABLE_NAME"}` entries to
resolve these values from the environment during ARM parameter generation.
Missing or empty environment values fail the update before deployment without
printing credentials. Literal config values continue to be used unchanged.

## Semantic model refresh parameters

The root `arm-template-parameters-definition.json` exposes the `WorkSpaceID`
and `SemanticModelID` pipeline defaults as ARM deployment parameters while
preserving the default parameterization rules and exposing the Databricks
existing cluster ID.

Before deploying to test, replace `<test-workspace-guid>` and
`<test-semantic-model-guid>` in `configs/adf_params_test.json` with the target
workspace and semantic model IDs. The release workflow applies these values
using `scripts/update_arm_template.py`; the Web activity expression is unchanged.

For other environments, use a separate config file and select it in the release
workflow. Values explicitly passed by triggers, parent pipelines, or manual runs
override the deployed pipeline defaults.
