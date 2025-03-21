import functions_framework
from googleapiclient.discovery import build

@functions_framework.cloud_event
def trigger_dflow_job(cloud_event):
    service = build('dataflow', 'v1b3')
    project = "noted-point-444318-r3"

    data = cloud_event.data
    file_name = data.get("name")

    template_path = "gs://dataflow-templates-us-central1/latest/GCS_Text_to_BigQuery"
    
    template_body = {
        "jobName": "load-csv-to-bquery",
        "parameters": {
            "javascriptTextTransformGcsPath" : "gs://bkt-metadata-all/udf-transform_string.js",
            "JSONPath" : "gs://bkt-metadata-all/bq_schema_string.json",
            "javascriptTextTransformFunctionName": "transform_stock_data",
            "outputTable": "noted-point-444318-r3:stock_data.vug_financial_data",
            "inputFilePattern" : "gs://bkt-stocks/"+file_name,
            "bigQueryLoadingTemporaryDirectory":"gs://bkt-metadata-all/temp_dir/"
        }
    }

    request = service.projects().templates().launch(projectId = project, gcsPath = template_path, body = template_body)
    response = request.execute()
    print(response) 