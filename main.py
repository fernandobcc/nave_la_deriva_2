import uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class PhaseChangeResponse(BaseModel):
    specific_volume_liquid: float
    specific_volume_vapor: float


def liquid_line_params() -> tuple:
    P1, V1 = 0.05, 0.00105
    P2, V2 = 10.0, 0.0035
    m1 = (V2 - V1) / (P2 - P1)
    b1 = V1 - m1 * P1
    return m1, b1


def vapor_line_params() -> tuple:
    P2, V2 = 10.0, 0.0035
    P3, V3 = 0.05, 30.0
    m2 = (V3 - V2) / (P3 - P2)
    b2 = V2 - m2 * P2
    return m2, b2


def get_phase_change_data(pressure: float) -> PhaseChangeResponse:
    m1, b1 = liquid_line_params()
    m2, b2 = vapor_line_params()

    # Calculate specific volume for liquid and vapor based on the pressure
    if pressure < 0.05 or pressure > 10:
        raise HTTPException(
            status_code=400, detail="Pressure must be between 0.05 and 10 MPa."
        )

    specific_volume_liquid = round(m1 * pressure + b1, 4)
    specific_volume_vapor = round(m2 * pressure + b2, 4)

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
