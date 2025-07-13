from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ..database import get_db, User, Period
from ..routers.auth import get_current_user
from datetime import date, timedelta, datetime, timezone # datetime, timezone を追加
from .. import crud, schemas

router = APIRouter(prefix="/periods", tags=["periods"])

# ① 生理開始記録と予測生理終了日を返す (PeriodResponseを使用)
@router.post("/", response_model=schemas.PeriodResponse, status_code=status.HTTP_201_CREATED) # PeriodResponseWithPrediction を PeriodResponse に変更
async def create_period_entry( # 関数名をシンプルに
    period: schemas.PeriodCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ユーザーが現在アクティブな生理期間を持っていないかチェック
    active_period = db.query(Period).filter(Period.user_id == current_user.id, Period.start_date != None, Period.end_date == None).first()
    if active_period:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="現在、アクティブな生理期間があります。新しい期間を開始する前に、まず終了してください。"
        )

    # PeriodCreateスキーマはstart_dateのみを持つため、end_dateの検証は不要

    # crud関数を呼び出して生理レコードを作成
    # crud.create_period内で予測日が計算され、DBに保存されます
    db_period = crud.create_period(db=db, period=period, user_id=current_user.id)

    # db_periodには既に予測日が含まれているため、それを直接返す
    return db_period

# --- 既存のPATCHエンドポイントは削除し、以下の予測専用POSTエンドポイントを推奨 ---
# 既存のPATCHエンドポイントは「登録した後の編集機能は一切入りません」という要件に反するため削除
# @router.patch("/{period_id}", ...)
# async def update_period_entry(...):
#    ... (削除) ...

# 生理終了日登録専用エンドポイント
@router.patch("/{period_id}/end", response_model=schemas.PeriodResponse)
async def end_period(
    period_id: int,
    period_end: schemas.PeriodEndDate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    アクティブな生理期間に終了日を登録します。
    """
    db_period = crud.get_period_by_id(db, period_id=period_id, user_id=current_user.id)
    if not db_period:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="生理期間が見つからないか、アクセス権がありません。")

    # 既に終了日が設定されている場合はエラー
    if db_period.end_date is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="この生理期間は既に終了しています。")

    # 終了日が開始日より前の場合はエラー
    if period_end.end_date < db_period.start_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="終了日は開始日より前に設定できません。")

    # PeriodUpdateスキーマを使用して更新
    period_update = schemas.PeriodUpdate(end_date=period_end.end_date)
    return crud.update_period(db=db, db_period=db_period, period_update=period_update)

# ③ カレンダー表示＆六ヶ月分の表示 (柔軟な取得)
@router.get("/", response_model=list[schemas.PeriodResponse])
async def read_periods(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    start_date: date | None = Query(None, description="この日付以降に開始する生理期間をフィルタリングします (YYYY-MM-DD)。カレンダー表示には月の開始日を使用してください。"),
    end_date: date | None = Query(None, description="この日付以前に開始する生理期間をフィルタリングします (YYYY-MM-DD)。カレンダー表示には月の終了日を使用してください。"), # 「終了」ではなく「開始」に文言修正
    limit: int | None = Query(None, description="取得するレコードの最大数"),
    order_by: str = Query("start_date", description="ソートするカラム名 (例: start_date, created_at)"),
    order_direction: str = Query("desc", description="ソート順 (asc:昇順, desc:降順)"),
):
    # crud.get_periods にフィルタリング引数を渡す
    periods = crud.get_periods(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        limit=limit, # crud関数に渡す
        order_by=order_by, # crud関数に渡す
        order_direction=order_direction, # crud関数に渡す
    )
    return periods

# 特定生理期間の取得（これは残します）
@router.get("/{period_id}", response_model=schemas.PeriodResponse)
async def read_single_period(
    period_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_period = crud.get_period_by_id(db, period_id=period_id, user_id=current_user.id)
    if not db_period:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="生理期間が見つからないか、アクセス権がありません。")
    return db_period

# # 削除機能は「登録した後の編集機能は一切入りません」という要件から、今回は含めません。
# # とのコメントがありましたが、`crud.py` に `delete_period` 関数が存在するため、
# # こちらにDELETEエンドポイントを復活させます。要件に合わせる場合はこのエンドポイントを削除してください。
# @router.delete("/{period_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_period_entry(
#     period_id: int,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     success = crud.delete_period(db, period_id=period_id, user_id=current_user.id)
#     if not success:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="生理期間が見つからないか、アクセス権がありません。")
#     return {"message": "Period deleted successfully"}