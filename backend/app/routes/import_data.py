from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.import_service import ImportService
from app.config import settings
from app.auth.dependencies import require_role

router = APIRouter()


@router.post("/excel", dependencies=[Depends(require_role("admin"))])
async def import_from_excel(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    """Import from Excel - admin only"""
    if not any(
        file.filename.endswith(ext) for ext in settings.allowed_extensions_set
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(settings.allowed_extensions_set)}",
        )
    
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE / (1024*1024)}MB",
        )
    
    service = ImportService(db)
    try:
        result = service.import_from_excel(contents, file.filename)
        return {"message": "Import successful", "stats": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Import failed: {str(e)}",
        )


@router.post("/csv", dependencies=[Depends(require_role("admin"))])
async def import_from_csv(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    """Import from CSV - admin only"""
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only CSV files allowed",
        )
    
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE / (1024*1024)}MB",
        )
    
    service = ImportService(db)
    try:
        result = service.import_from_csv(contents)
        return {"message": "Import successful", "stats": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Import failed: {str(e)}",
        )