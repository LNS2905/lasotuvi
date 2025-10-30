"""FastAPI application exposing lasotuvi services."""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from lasotuvi.api import database, schemas, services

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield


app = FastAPI(title="lasotuvi API", version="0.1.0", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    allow_origin_regex="https?://.*localhost.*",
)


def ensure_db() -> None:
    database.init_db()


@app.post("/charts", response_model=schemas.ChartResponse)
def create_chart(request: schemas.ChartRequest, _=Depends(ensure_db)):
    board, overview = services.build_chart(
        day=request.day,
        month=request.month,
        year=request.year,
        hour_branch=request.hour_branch,
        gender=request.gender,
        name=request.name,
        solar_calendar=request.solar_calendar,
        timezone=request.timezone,
    )

    houses = services.serialize_board(board)
    extra = services.extract_overview_info(overview)

    chart_id = database.insert_chart(
        request.model_dump(),
        houses,
        extra,
    )

    return schemas.ChartResponse(id=chart_id, request=request, houses=houses, extra=extra)


@app.get("/charts/{chart_id}", response_model=schemas.ChartResponse)
def get_chart(chart_id: int, _=Depends(ensure_db)):
    stored = database.fetch_chart(chart_id)
    if not stored:
        raise HTTPException(status_code=404, detail="Chart not found")

    request = schemas.ChartRequest(**stored["payload"])
    return schemas.ChartResponse(
        id=stored["id"],
        request=request,
        houses=stored["houses"],
        extra=stored["extra"],
    )


@app.get("/charts", response_model=list[schemas.ChartResponse])
def list_latest(limit: int = 20, _=Depends(ensure_db)):
    results = []
    for chart in database.list_charts(limit=limit):
        request = schemas.ChartRequest(**chart["payload"])
        results.append(
            schemas.ChartResponse(
                id=chart["id"],
                request=request,
                houses=chart["houses"],
                extra=chart["extra"],
            )
        )
    return results
