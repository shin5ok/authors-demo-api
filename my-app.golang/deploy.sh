#!/bin/bash

gcloud run deploy --region=asia-northeast1 --source=. --set-env-vars=PROJECT=$PROJECT my-app