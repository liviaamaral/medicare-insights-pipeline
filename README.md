# medicare-insights-pipeline
End-to-end data pipeline for analyzing U.S. Medicare inpatient data using GCP, Terraform, dbt, and Looker Studio


## Infrastructure Setup

### Prerequisites

- [GCP account](https://cloud.google.com) with billing enabled
- [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated
- [Terraform](https://developer.hashicorp.com/terraform/install) >= 1.0

### 1. Clone the repository
```bash
git clone https://github.com/livsamaral/medicare-insights-pipeline.git
cd medicare-insights-pipeline
```

### 2. Configure GCP

Set your project:
```bash
gcloud config set project medicare-de-project
```

Enable required APIs:
```bash
gcloud services enable iam.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
```

### 3. Create service account
```bash
gcloud iam service-accounts create medicare-pipeline-sa \
  --display-name="Medicare Pipeline Service Account"

gcloud projects add-iam-policy-binding medicare-de-project \
  --member="serviceAccount:medicare-pipeline-sa@medicare-de-project.iam.gserviceaccount.com" \
  --role="roles/bigquery.admin"

gcloud projects add-iam-policy-binding medicare-de-project \
  --member="serviceAccount:medicare-pipeline-sa@medicare-de-project.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

mkdir -p ~/.gcp
gcloud iam service-accounts keys create ~/.gcp/medicare-de-project.json \
  --iam-account=medicare-pipeline-sa@medicare-de-project.iam.gserviceaccount.com
```

### 4. Provision infrastructure
```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` with your values, then:
```bash
terraform init
terraform plan
terraform apply
```

## Pipeline

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- Infrastructure provisioned (see above)

### Running the pipeline

Copy the environment file:
```bash
cd mage
cp .env.example .env
```

Edit `.env` with your GCP project values, then start Mage:
```bash
docker compose up
```

Access the Mage UI at `http://localhost:6789`.

Run the `medicare_ingestion` pipeline — it will:
1. Extract inpatient charges data from `bigquery-public-data.cms_medicare.inpatient_charges_2015`
2. Clean and transform the data (standardize columns, remove nulls, add `out_of_pocket` derived column)
3. Load raw parquet file to GCS at `inpatient/2015/medicare_inpatient_2015.parquet`
4. Load transformed data to BigQuery table `medicare_insights.inpatient_2015`

## Transformations (dbt)

### Setup

Install dependencies:
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Configure your dbt profile at `~/.dbt/profiles.yml`:
```yaml
medicare_insights:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: medicare-de-project
      dataset: medicare_insights
      keyfile: ~/.gcp/medicare-de-project.json
      threads: 4
      job_execution_timeout_seconds: 300
      location: us-central1
```

### Running dbt
```bash
cd medicare_insights
dbt deps
dbt run
dbt test
```