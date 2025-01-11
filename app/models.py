from app import db, app
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, UniqueConstraint, Enum, Time, DECIMAL
from sqlalchemy.orm import relationship, backref
import hashlib
from flask_login import UserMixin


class NguoiDung(db.Model, UserMixin):
    __tablename__ = "nguoidung"
    id_nguoi_dung = Column(Integer,primary_key=True,autoincrement=True)
    tai_khoan = Column(String(50),nullable=False,unique=True)
    mat_khau = Column(String(50),nullable=False)
    ten_nguoi_dung = Column(String(50),nullable=False)
    hinh_anh = Column(String(255),nullable=False)

    def get_id(self):
        return self.id_nguoi_dung

class Nhom(db.Model):
    __tablename__ = "nhom"
    id_nhom = Column(Integer,primary_key=True,autoincrement=True)
    ten_nhom = Column(String(50),unique=True)
    hinh_anh = Column(String(50))

class TinNhan(db.Model):
    __tablename__="tinnhan"
    id_tin_nhan = Column(Integer,primary_key=True,autoincrement=True)
    id_nguoi_dung = Column(Integer,ForeignKey("nguoidung.id_nguoi_dung"),nullable=False)
    id_nhom = Column(Integer,ForeignKey("nhom.id_nhom"),nullable=False)
    noi_dung = Column(String(255),nullable=False)
    thoi_gian = Column(DateTime,nullable=False)

class ThuocNhom(db.Model):
    __tablename__ = "thuocnhom"
    id_thuoc_nhom = Column(Integer,primary_key=True,autoincrement=True)
    id_nguoi_dung = Column(Integer,ForeignKey("nguoidung.id_nguoi_dung"),nullable=False)
    id_nhom = Column(Integer,ForeignKey("nhom.id_nhom"),nullable=False)
    __table_args__= (
        UniqueConstraint("id_nguoi_dung","id_nhom",name="unix_nguoi_dung_nhom"),
    )

class NguoiDung_TinNhan(db.Model):
    __tablename__ = "nguoidung_tinnhan"
    id_nguoi_dung_tin_nhan = Column(Integer,primary_key=True,autoincrement=True)
    id_nguoi_dung = Column(Integer,ForeignKey("nguoidung.id_nguoi_dung"),nullable=False)
    id_tin_nhan = Column(Integer,ForeignKey("tinnhan.id_tin_nhan"),nullable=False)
    thoi_gian_nhan = Column(DateTime)
    thoi_gian_xem = Column(DateTime)
    __table_args__=(
        UniqueConstraint("id_nguoi_dung","id_tin_nhan",name="unix_nguoi_dung_tin_nhan"),
    )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        Vinh_Tien = NguoiDung(tai_khoan="VinhTien",ten_nguoi_dung="Vĩnh Tiến",mat_khau=str(hashlib.md5('lkjhg09876'.encode('utf-8')).hexdigest()),hinh_anh="./static/Images/VinhTien.jpg")
        Gia_Tuan = NguoiDung(tai_khoan="GiaTuan",ten_nguoi_dung="Gia Tuấn",mat_khau=str(hashlib.md5('lkjhg09876'.encode('utf-8')).hexdigest()),hinh_anh="./static/Images/GiaTuan.jpg")
        Tran_Nhu = NguoiDung(tai_khoan="TranNhu",ten_nguoi_dung="Trân Như",mat_khau=str(hashlib.md5('lkjhg09876'.encode('utf-8')).hexdigest()),hinh_anh="./static/Images/GiaTuan.jpg")
        db.session.add(Tran_Nhu)
        db.session.add(Gia_Tuan)
        db.session.add(Vinh_Tien)
        db.session.commit()
