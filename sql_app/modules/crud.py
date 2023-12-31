from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


# ユーザー取得
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


# ユーザー一覧取得
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# 会議室取得
def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.room_id == room_id).first()


# 会議室一覧取得
def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()


# 予約一覧取得
def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()


# 予約取得
def get_booking(db: Session, booking_id: int):
    return (
        db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    )


# 指定した会議室の予約一覧取得
def get_bookings_filtered_room(room_id, db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Booking)
        .filter(models.Booking.room_id == room_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# ユーザー登録
def create_user(db: Session, user: schemas.User):
    db_user = models.User(user_name=user.user_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 会議室登録
def create_room(db: Session, room: schemas.Room):
    db_room = models.Room(room_name=room.room_name, capacity=room.capacity)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


# 予約登録
def create_booking(db: Session, booking: schemas.Booking):
    db_booked = (
        db.query(models.Booking)
        .filter(models.Booking.room_id == booking.room_id)
        .filter(models.Booking.end_datetime > booking.start_datetime)
        .filter(models.Booking.start_datetime < booking.end_datetime)
        .all()
    )
    # 重複するデータがなければ予約
    if len(db_booked) == 0:
        db_booking = models.Booking(
            user_id=booking.user_id,
            room_id=booking.room_id,
            booked_num=booking.booked_num,
            start_datetime=booking.start_datetime,
            end_datetime=booking.end_datetime,
        )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return db_booking
    else:
        raise HTTPException(status_code=404, detail="Already booked")


# ユーザー更新
def update_user(db: Session, user_id: int, user_update: schemas.User):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        db_user.user_id = user_update.user_id
        db_user.user_name = user_update.user_name
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        raise HTTPException(status_code=404, detail="User not found")


# 会議室更新
def update_room(db: Session, room_id: int, room_update: schemas.Room):
    db_room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    if db_room:
        db_room.room_id = room_update.room_id
        db_room.room_name = room_update.room_name
        db_room.capacity = room_update.capacity
        db.commit()
        db.refresh(db_room)
        return db_room
    else:
        raise HTTPException(status_code=404, detail="Room not found")


# 予約更新
def update_booking(db: Session, booking_id: int, booking_update: schemas.BookingUpdate):
    db_booking = (
        db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    )
    if db_booking:
        db_booking.user_id = booking_update.user_id
        db_booking.room_id = booking_update.room_id
        db_booking.booked_num = booking_update.booked_num
        db_booking.start_datetime = booking_update.start_datetime
        db_booking.end_datetime = booking_update.end_datetime
        db.commit()
        db.refresh(db_booking)
        return db_booking
    else:
        raise HTTPException(status_code=404, detail="Booking not found")


# ユーザー削除
def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()


# 会議室削除
def delete_room(db: Session, room: models.Room):
    db.delete(room)
    db.commit()


# 予約削除
def delete_booking(db: Session, booking: models.Booking):
    db.delete(booking)
    db.commit()
