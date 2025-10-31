# 💸 Transaction Processor API

A Django REST-based service that receives transaction webhooks from external payment processors (e.g., RazorPay), acknowledges them instantly, and processes them asynchronously with a simulated delay.

Live Demo:  
🌐 **https://transaction-processor-api-6.onrender.com/**  [Please use Postman for accurate API testing.]

---

## 🧾 Overview

This API receives webhook notifications, stores transaction details, and processes them in the background.  
It ensures:
- Fast acknowledgments (`< 500ms`)
- Background processing (simulated **30-second delay**)
- Duplicate prevention (via unique `transaction_id`)
- Persistent data storage
- Cloud deployment (Render)

---

## ✅ Implemented Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/v1/webhooks/transactions` | Accepts new transaction webhook |
| `GET` | `/v1/transactions/{transaction_id}` | Retrieve transaction status |

---

## 🧪 How to Test the API (Step-by-Step)

> Use **Postman** or **curl**.  
> Browser-only testing will not show POST results correctly.

### 🔹 Step 1: Health Check
**Request**
GET https://transaction-processor-api-6.onrender.com/




Expected Response

{
  "status": "HEALTHY",
  "current_time": "2025-11-01T12:34:56Z"
}

✅ Confirms the app is live and reachable.

🔹 Step 2: Send a Webhook
Request


[ 1. Below URL paste it into Postman URL With POST request ]
  
POST https://transaction-processor-api-6.onrender.com/v1/webhooks/transactions



[2. Under Body select JSON and type context ]

{
  "transaction_id": "txn_1009",
  "source_account": "acc_user_789",
  "destination_account": "acc_merchant_456",
  "amount": 1500,
  "currency": "INR"
}

Expected Response :

{
  "message": "Accepted for processing",
  "transaction_id": "txn_1009"
}


📈 HTTP Status: 202 Accepted
⚡ Response Time: under 500 ms
💡 The background process now runs for ~30 seconds.

🔹 Step 3: Check Processing Status
After ~30 seconds, check the status:

Request


[ Put this URL in Postman with GET request for checking Status ]

GET https://transaction-processor-api-6.onrender.com/v1/transactions/txn_1009

Expected Response (after 30 seconds)


{
  "transaction_id": "txn_1009",
  "source_account": "acc_user_789",
  "destination_account": "acc_merchant_456",
  "amount": 1500.0,
  "currency": "INR",
  "status": "PROCESSED",
  "created_at": "2025-10-31T20:05:39.167538Z",
  "processed_at": "2025-10-31T20:06:09.175100Z"
}

If called before 30s, status will show "PROCESSING" and "processed_at": null.

🔹 Step 4: Duplicate Webhook Prevention
Re-send the same webhook request (txn_1009 again).
You’ll still get a 202 Accepted, but the system will not duplicate records.

Each transaction_id is unique.

Repeated webhooks are gracefully ignored.

🔹 Step 5: Example of an Already Processed Transaction
You can view this sample transaction:


GET https://transaction-processor-api-6.onrender.com/v1/transactions/txn_1004
Example Response


{
  "transaction_id": "txn_1004",
  "source_account": "acc_user_789",
  "destination_account": "acc_merchant_456",
  "amount": 1500.0,
  "currency": "INR",
  "status": "PROCESSED",
  "created_at": "2025-10-31T20:05:39.167538Z",
  "processed_at": "2025-10-31T20:06:09.175100Z"
}
⚙️ Example cURL Commands
Health Check


curl -i https://transaction-processor-api-6.onrender.com/
Send Webhook


curl -i -X POST https://transaction-processor-api-6.onrender.com/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{"transaction_id":"txn_1009","source_account":"acc_user_789","destination_account":"acc_merchant_456","amount":1500,"currency":"INR"}'
Check Status (after 30s)


curl -i https://transaction-processor-api-6.onrender.com/v1/transactions/txn_1009

🧰 How to Run Locally
Clone Repo


git clone https://github.com/codingwithrsn33/transaction-processor-api.git
cd transaction-processor-api
Create Virtual Environment


python -m venv env
source env/bin/activate  # (Mac/Linux)
env\Scripts\activate     # (Windows)
Install Dependencies


pip install -r requirements.txt
Apply Migrations


python manage.py makemigrations
python manage.py migrate
Run Development Server


python manage.py runserver
Test Locally

Visit http://127.0.0.1:8000/ → health check

Use Postman to test same endpoints locally.

🧠 Technical Choices

Feature	Technology	Reason

Framework	Django + Django REST Framework	Fast, reliable API development

DB	SQLite	Lightweight, persistent local DB

Background Tasks	Thread-based async delay	Simulates real async (Celery )

Deployment	Render.com	Free cloud hosting, simple setup

Idempotency	Unique transaction_id check	Prevents duplicates

Logging	Django default + print statements	Simple monitoring


🧩 Key Requirements Covered

✅ Fast Response (<500ms) on webhook receive
✅ Background Processing (30s delay)
✅ Persistent Storage
✅ Idempotency (no duplicates)
✅ Health Check Endpoint
✅ Public Cloud Deployment
✅ Test Instructions & README Provided


🚀 Quick Verification Checklist (for reviewers)
Test	Expected Outcome
GET /	Returns status: HEALTHY
POST /v1/webhooks/transactions	Returns 202 Accepted instantly
Wait 30s + GET /v1/transactions/{id}	Shows status: PROCESSED
Duplicate POST	No duplicate record created
Render link works 24x7	✅

🧩 Troubleshooting
Issue	Cause	Fix
transaction_id is required	Missing JSON or Content-Type	Set header Content-Type: application/json
DisallowedHost	Render host missing from ALLOWED_HOSTS	Added "*" in settings
Response delay >500ms	Network lag or free-tier wake-up time	Retry after app wakes up
Empty result on /v1/transactions/{id}	Queried before processing completed	Wait 30s and retry


💬 Final Note 
Please test using Postman as per the above instructions.
The API is live and publicly hosted at:


👉 https://transaction-processor-api-6.onrender.com/


You can verify health, send webhooks, and check the transaction status after ~30 seconds to confirm background processing.

🧱 Author

Rohan Subhash Darekar
Python | Django | REST APIs | SQL | Cloud Deployment
📍 Built for Backend Developer Assessment
GitHub: codingwithrsn33




