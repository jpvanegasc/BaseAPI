from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import db_session

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    description="Overall service health",
)
def service_health(db: Session = Depends(db_session)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except SQLAlchemyError:
        db_status = "down"
    status = {
        "api": "ok",
        "database": db_status,
    }
    return status


@router.get(
    "/ping",
    status_code=status.HTTP_200_OK,
    description="API health",
)
def ping():
    return {"message": "ok"}


@router.get(
    "/database",
    status_code=status.HTTP_200_OK,
    description="Database health",
)
def database(db: Session = Depends(db_session)):
    try:
        db.execute(text("SELECT 1"))
        return {"message": "ok"}
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="database is down"
        )
