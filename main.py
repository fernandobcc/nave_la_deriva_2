import uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class PhaseChangeResponse(BaseModel):
    specific_volume_liquid: float
    specific_volume_vapor: float


def line_params(Y1: float, X1: float, Y2: float, X2: float) -> tuple:
    m = (Y2 - Y1) / (X2 - X1)
    b = Y1 - m * X1
    return m, b


def liquid_line_params() -> tuple:
    return line_params(0.05, 0.00105, 10.0, 0.0035)


def vapor_line_params() -> tuple:
    return line_params(10.0, 0.0035, 0.05, 30.0)


def get_phase_change_data(pressure: float) -> PhaseChangeResponse:
    m_liquid, b_liquid = liquid_line_params()
    m_vapor, b_vapor = vapor_line_params()

    # Calculate specific volume for liquid and vapor based on the pressure
    specific_volume_liquid = (pressure - b_liquid) / m_liquid
    specific_volume_vapor = (pressure - b_vapor) / m_vapor

    return PhaseChangeResponse(
        specific_volume_liquid=specific_volume_liquid,
        specific_volume_vapor=specific_volume_vapor,
    )


@app.get("/phase-change-diagram", response_model=PhaseChangeResponse)
async def phase_change_diagram(pressure: float) -> PhaseChangeResponse:
    data = get_phase_change_data(pressure)
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
