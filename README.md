# Securonix Data Visualization Assignment: Backend

This is a Flask project that serves as the backend for the Securonix Data Visualization Assignment.

## Getting Started

To get started with this project, follow the instructions below.

## Prerequisites

### Python

Ensure you have Python installed on your system. This project was created using Python 3.12. You can download it from [python.org](https://www.python.org/downloads/).

#### 1. Clone the repository:

```bash
git clone https://github.com/f0rzaX/securonix-backend
```

#### 2. Navigate to the project directory:

```bash
cd securonix-backend
```

#### 3. Create a virtual environment:

```bash
python -m venv venv
```

#### 4. Activate the virtual environment:

On Windows:

```bash
venv\Scripts\activate
```

#### 5. Install dependencies:

```bash
pip install -r requirements.txt
```


#### 6. Setup the database

We are using Postgres to store user's credentials please run these commands to ensure you have the database configured and running:

```bash
docker run -d --name postgres_securonix -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=postgres -v securonix:/var/lib/postgresql/data -p 5432:5432 postgres
```

```bash
docker cp setup.sql postgres_securonix:/setup.sql
```

```bash
docker exec -it postgres_securonix psql -U postgres -d postgres -f /setup.sql
```


#### 7. Configuration

Create a `.env` file in the project root directory and Add the following environment variables to the `.env` file: (I'll add env to repo for your convenience)

```bash
PORT
SECRET_KEY
DATABASE_URL
JWT_SECRET_KEY
UPLOAD_FOLDER
FRONTEND_URL
ROWS_PER_PAGE
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
GOOGLE_USER_INFO
```

##### Note: Postgres Credentials: Username: 'postgres', Password: 'pass'

#### 8. Usage

Start the application using

```bash
flask run
```

Access the application in at

```bash
http://localhost:5000
```
