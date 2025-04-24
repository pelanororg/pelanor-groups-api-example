# Pelanor Tenant Group Upserter

This is a simple utility script to bulk-create or update **tenant groups** in [Pelanor](https://pelanor.io)'s API using a CSV file.
Refer to the full API documentation here:
- [US environment](https://app.pelanor.io/api-docs)
- [EU environment](https://app-eu.pelanor.io/api-docs)

---

## 📁 Files

- `bulk_upsert_tenants.py` — The main Python script to read tenant names and call the Pelanor API.
- `example_tenants.csv` — Sample CSV file to show expected structure.
- `.env` — You must create this yourself with your API token (see below).

---

## 🧪 Prerequisites

- Python 3.8+
- [Requests](https://pypi.org/project/requests/) and [python-dotenv](https://pypi.org/project/python-dotenv/)

Install dependencies (if using a virtual environment):

```
pip install -r requirements.txt
```

If not using `requirements.txt`, you can run:

```
pip install requests python-dotenv
```

---

## 🛠️ Setup

1. Clone or download the repo.
2. Copy this into a new file called `.env` in the same directory:

```
PELANOR_API_TOKEN=<your-pelanor-api-token-here>
```

3. Update or replace `example_tenants.csv` with your own list.

CSV format:

```
name,type,status
alpha,Demo,Active
bravo,Demo,Active
charlie,Demo,Inactive
```

Only the `name` field is used by the script.

---

## ▶️ Usage

```
python bulk_upsert_tenants.py
```

Each tenant will be sent as a `PUT` request to the Pelanor `/v1/groups` API under the `Tenants` dimension. The payload includes tag, Kubernetes namespace, and Snowflake database filters based on the tenant name.

---

## ✅ Output

The script will print a success or failure message for each tenant:

```
✔  Upserted tenant 'alpha'
✖  Failed for 'delta': 400 — Invalid request...
```

---

## 📎 Notes

- The API request includes an empty `global_filters` array as required by Pelanor.
- Each request is case-adjusted (e.g., `Tag=lowercase`, `SnowflakeDatabase=UPPERCASE`, etc.).

---

## 📄 License

MIT — free to use and adapt.
