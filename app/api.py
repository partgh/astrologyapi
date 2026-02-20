from fastapi import APIRouter, HTTPException

from app.calculations.calculations import calculate_chart_data
from app.models.schema import ChartRequest, ChartResponse

router = APIRouter()


@router.post("/get_chart", response_model=ChartResponse)
def get_chart(request: ChartRequest):
    try:
        chart = calculate_chart_data(request)
        return ChartResponse(**chart)
    except ValueError as exc:
        detail = exc.args[0] if exc.args else "calculation_error"
        raise HTTPException(status_code=422, detail=detail)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={"error_type": "internal_error", "message": str(exc)},
        )
