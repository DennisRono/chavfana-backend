# ChavFana — Farm Management System

**ChavFana** is a modern farm management system designed to help farmers track and manage their daily operations — from crops to livestock and everything in between.

### 1. Clone the repository

```bash
git clone https://github.com/DennisRono/chavfana-backend.git
cd chavfana
```

### 2. Set up the environment

Create your environment file and install dependencies:

```bash
mkdir .env && poetry install
```

> 💡 Make sure you have [Poetry](https://python-poetry.org/docs/) installed.
> You can copy `.env.example` to `.env` and update environment variables as needed.

## Run the Development Server

You can start the app using `make` or `uvicorn` directly.

**Option 1: Using Makefile**

```bash
make dev
```

**Option 2: Using Uvicorn**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on **[http://localhost:8000](http://localhost:8000)**

## API Documentation

Once the server is running, you can access the interactive API docs here:

- **RapiDocs:** [http://localhost:8000/rapi-docs](http://localhost:8000/rapi-docs)
- _(Optional)_ **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- _(Optional)_ **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)


## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
