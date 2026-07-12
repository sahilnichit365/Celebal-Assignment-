# Week 4 - Azure Data Factory Assignment

## Objective
Build an end-to-end Azure Data Factory pipeline to copy data from one Azure Blob Storage container to another while validating file metadata.

## Azure Services Used
- Azure Resource Group
- Azure Storage Account
- Azure Blob Storage
- Azure Data Factory
- Azure IAM

## Dataset
Titanic Dataset (tested.csv)
(superstore dataset's copy data doesn't get succeed that's why i have used titanic dataset)

## Pipeline Flow
Source Blob Storage
↓
Get Metadata Activity
↓
Copy Data Activity
↓
Destination Blob Storage

## Activities Used
- Get Metadata
- Copy Data

## IAM Roles Assigned
- Reader
- Storage Blob Data Contributor

## Result
The pipeline executed successfully and copied the dataset from the source blob container to the destination blob container.

## Learning Outcomes
- Created Azure Storage Account and Blob Containers
- Configured Azure Data Factory
- Created Linked Services and Datasets
- Used Get Metadata and Copy Data activities
- Assigned IAM roles for secure access
- Successfully executed and monitored the pipeline
