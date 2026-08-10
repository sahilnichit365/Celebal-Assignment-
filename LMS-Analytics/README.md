# LMS Analytics Data Pipeline

## 📌 Project Overview

The LMS Analytics Data Pipeline is a data engineering project designed to process and transform Learning Management System (LMS) data using Apache Spark and Databricks.

The project follows the Medallion Architecture:

**Bronze → Silver → Gold**

The pipeline converts raw LMS data into clean, enriched, and business-ready analytical datasets.

---

## 🏗️ Architecture

```text
                    LMS Raw Data
                         │
                         ▼
              ┌─────────────────────┐
              │   🥉 BRONZE LAYER   │
              │                     │
              │ Raw LMS Data        │
              │ - Courses           │
              │ - Learners          │
              │ - Enrolments        │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   🥈 SILVER LAYER   │
              │                     │
              │ Data Cleaning       │
              │ Data Transformation │
              │ Data Enrichment     │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │     🥇 GOLD LAYER   │
              │                     │
              │ Business Analytics  │
              │ Course Performance  │
              │ Learner Performance │
              │ Enrollment Analytics│
              │ Activity Analytics  │
              └─────────────────────┘