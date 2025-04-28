# Coaching Engine Project

This is a basic FastAPI application that serves as a (mostly) stateless coaching engine to provide recommendations,
feedback, and coaching to users based on their input. The application is designed to be extensible and can be 
integrated with various machine learning models or external APIs to enhance its capabilities.

It provides some additional features around content moderation to ensure that the content being generated is
appropriate and safe for users.

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
- On Windows:
```bash
.venv\Scripts\activate
```
- On macOS/Linux:
```bash
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Add Local Environment Variables:
```bash
# Assuming you are in the root dir and you don't already have an env file
echo 'OPEN_API_KEY="<REPLACE_WITH_YOUR_KEY>"' > .env
````
Outside of this key, all other env variables in the default `config.py` file are optional to set for the app to work.

## Running the Application

To run the application locally, use the following command:
```bash
fastapi dev main.py
```

The application will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing
There are some sample payloads in the `sample_payloads` directory. 
You can use them to test the API endpoints to view different responses and behaviors. 

## High Level Project Structure
```
.
│                                                             
├── client/              # 3rd party clients                               
├── dto/                 # Data Transfer Objects (DTOs)                  
├── model/               # Internal ML/RL models      
├── notebooks/           # Jupyter notebooks for model creation      
├── router/              # API routers                                
├── service/             # Service layer for business logic                                 
├── sample_payloads/     # Sample payloads for testing
├── config.py            # App config file                           
├── main.py              # Main application file + entry point
├── Dockerfile           # Dockerfile for containerization
├── requirements.txt     # Project dependencies
└── README.md            # This file
``` 