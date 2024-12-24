# Nave a la Deriva 2

This project is a FastAPI application that provides phase change data for a given pressure. The application calculates the specific volume of liquid and vapor based on the pressure input.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/fernandobcc/nave_a_la_deriva_2.git
    cd nave_a_la_deriva_2
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the application, use the following command:
```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Get Phase Change Data

- **URL:** `/phase-change-diagram`
- **Method:** `GET`
- **Query Parameters:**
  - `pressure` (float): The pressure value for which to get the phase change data. Must be between 0.05 and 10 MPa.
- **Response:**
  - `specific_volume_liquid` (float): The specific volume of the liquid phase.
  - `specific_volume_vapor` (float): The specific volume of the vapor phase.
- **Error Responses:**
  - `400 Bad Request`: If the pressure is outside the valid range or if the temperature condition is not met.

## Example

To get the phase change data for a pressure of 5 MPa, make a GET request to:
```
http://127.0.0.1:8000/phase-change-diagram?pressure=5
```
