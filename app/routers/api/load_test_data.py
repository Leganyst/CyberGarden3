from app.startup_test import main as load_data
from fastapi import APIRouter

router = APIRouter(prefix="/load-test-data", tags=["Load Test Data"])

@router.get("/")
async def load_test_data():
    """
    Загрузка тестовых данных в базу данных.
    """
    load_data()
    return {"message": "Test data loaded successfully"}