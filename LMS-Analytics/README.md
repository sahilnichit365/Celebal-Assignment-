# LearnTrack: LMS Analytics Pipeline

## Overview

LearnTrack is a batch data engineering pipeline for analyzing Learning Management System (LMS) data.

The project uses Python, PySpark, Databricks, Delta Lake, and SQL to transform raw LMS data into analytics-ready business metrics.

## Datasets

The pipeline uses three source datasets:

- `learners.csv` - learner information
- `courses.csv` - course and instructor information
- `enrolment_activity.csv` - learner enrollment, progress, and assessment activity

## Architecture

The project follows the Medallion Architecture:

```text
Raw CSV Data
     ↓
Bronze Layer
     ↓
Silver Layer
     ↓
Gold Layer
     ↓
Business Analytics