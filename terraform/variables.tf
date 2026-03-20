variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "bq_dataset" {
  description = "BigQuery dataset name"
  type        = string
  default     = "medicare_insights"
}

variable "gcs_bucket" {
  description = "GCS bucket name"
  type        = string
}

variable "credentials" {
  description = "Path to GCP service account key JSON"
  type        = string
}