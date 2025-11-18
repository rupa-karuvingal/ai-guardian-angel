# Deploying to Cloud Run (high level)

1. Build container:
   gcloud builds submit --tag gcr.io/$PROJECT_ID/emergency-agent

2. Create Cloud SQL (Postgres) instance and user. Note the instance connection name.

3. Deploy:
   gcloud run deploy emergency-agent \
     --image gcr.io/$PROJECT_ID/emergency-agent \
     --platform managed \
     --region $GCP_REGION \
     --set-env-vars DATABASE_URL='<CLOUDSQL_CONNECTION_STRING>',FERNET_KEY='<FERNET_KEY>',TWILIO_ACCOUNT_SID='<..>' \
     --add-cloudsql-instances=<INSTANCE_CONNECTION_NAME>

4. Set up Cloud Tasks queue and service account with Cloud Tasks Enqueuer role.

5. Store secrets in Secret Manager and mount or load at runtime.

