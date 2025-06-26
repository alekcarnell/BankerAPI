# Banking API

A simple RESTful API built with Flask that allows users to view, filter, 
and submit bank interest rate data. Data is stored persistently in a local 
`data.json` file — no database required at this time. 

Right now the API is serving interest rates for deposit accounts. There
may be some expansion on this in the future. 

---

## Features

- `GET /api/rates`: Retrieve all bank interest rates
  - Optional filtering by `country`, `bank`, and `account_type`
- `GET /api/rates/<id>`: Retrieve a single rate by ID
- `POST /api/rates`: Submit a new interest rate (with input validation)
- `DELETE /api/rates`: Remove an interest rate 
- Data is saved to and loaded from `data.json` 

---

## Project Structure

├── app.py # Main Flask app and blueprint registration
├── routes.py # All API route definitions
├── validators.py # Recieves and sanitizes data 
├── data_handler.py # Functions for reading/writing data.json
├── data.json # Persistent data store for rates
└── requirements.txt # Dependencies

---

## Getting Started

### 1. Clone the project

```
git clone https://github.com/yourusername/bank-rates-api.git
cd bank-rates-api
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Run the app
```
python app.py
```

App will be running at: http://127.0.0.1:5000