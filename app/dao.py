from app.models import TinNhan,NguoiDung,Nhom,ThuocNhom,NguoiDung_TinNhan
from sqlalchemy.orm import aliased
from sqlalchemy import or_,and_,func
import hashlib 
from datetime import datetime
from app import db,app

def lay_nguoi_dung_dang_nhap(tai_khoan,mat_khau):
    return NguoiDung.query.filter(NguoiDung.tai_khoan==tai_khoan,NguoiDung.mat_khau==hashlib.md5(mat_khau.encode("utf-8")).hexdigest()).first()

def lay_ds_nguoi_dung(tu_khoa,id_nguoi_dung):
    ds_nguoi_dung = NguoiDung.query.filter(NguoiDung.ten_nguoi_dung.contains(tu_khoa),NguoiDung.id_nguoi_dung != id_nguoi_dung).all()
    ds_nguoi_dung_2=[]
    for nguoi_dung in ds_nguoi_dung:
        ds_nguoi_dung_2.append({
            "id_nguoi_dung":nguoi_dung.id_nguoi_dung,
            "ten_nguoi_dung": nguoi_dung.ten_nguoi_dung,
            "hinh_anh": nguoi_dung.hinh_anh
        })
    
    return ds_nguoi_dung_2

def lay_ds_nhom(id_nguoi_dung):
    nguoi_dung_1 = aliased(NguoiDung)
    thuoc_nhom_1 = aliased(ThuocNhom)

    nguoi_dung_2 = aliased(NguoiDung)
    thuoc_nhom_2 = aliased(ThuocNhom)

    ds_nhom_chat = db.session.query(Nhom.id_nhom,nguoi_dung_2.ten_nguoi_dung,nguoi_dung_2.hinh_anh)\
    .join(thuoc_nhom_1,Nhom.id_nhom == thuoc_nhom_1.id_nhom)\
    .join(nguoi_dung_1,nguoi_dung_1.id_nguoi_dung ==  thuoc_nhom_1.id_nguoi_dung)\
    .join(thuoc_nhom_2,Nhom.id_nhom == thuoc_nhom_2.id_nhom)\
    .join(nguoi_dung_2,nguoi_dung_2.id_nguoi_dung ==  thuoc_nhom_2.id_nguoi_dung)\
    .filter(nguoi_dung_1.id_nguoi_dung != nguoi_dung_2.id_nguoi_dung)\
    .filter(nguoi_dung_1.id_nguoi_dung == id_nguoi_dung)\
    .all()

    ds_nhom_chat_2 = []

    for nhom_chat in ds_nhom_chat:
        thong_tin_khac = db.session.query(TinNhan.noi_dung,NguoiDung_TinNhan.thoi_gian_xem)\
        .join(NguoiDung_TinNhan,NguoiDung_TinNhan.id_tin_nhan == TinNhan.id_tin_nhan,isouter=True)\
        .filter(NguoiDung_TinNhan.id_nguoi_dung == id_nguoi_dung)\
        .filter(nhom_chat.id_nhom == TinNhan.id_nhom)\
        .order_by(TinNhan.id_tin_nhan.desc()).first()

        ds_nhom_chat_2.append({
            "id_nhom": nhom_chat.id_nhom,
            "ten_nguoi_dung": nhom_chat.ten_nguoi_dung,
            "hinh_anh": nhom_chat.hinh_anh,
            "noi_dung": thong_tin_khac[0] if thong_tin_khac else "chưa có tin nhắn" ,
            "thoi_gian_xem" : thong_tin_khac[1].strftime("%Y-%m-%d %H:%M:%S") if thong_tin_khac and thong_tin_khac[1] else None
        })

        ds_nguoidung_tinnhan = NguoiDung_TinNhan.query.filter(NguoiDung_TinNhan.id_nguoi_dung == id_nguoi_dung,NguoiDung_TinNhan.thoi_gian_nhan==None).all()

        for nguoidung_tinnhan in ds_nguoidung_tinnhan:
            nguoidung_tinnhan.thoi_gian_nhan = datetime.now()
        
    db.session.commit()

    return ds_nhom_chat_2

def tao_nhom_moi(id_nguoi_dung_1,id_nguoi_dung_2):
        nguoi_dung_1 = aliased(NguoiDung)
        thuoc_nhom_1 = aliased(ThuocNhom)

        nguoi_dung_2 = aliased(NguoiDung)
        thuoc_nhom_2 = aliased(ThuocNhom)

        nhom = db.session.query(Nhom.id_nhom, func.count(ThuocNhom.id_nhom))\
        .join(ThuocNhom,ThuocNhom.id_nhom == Nhom.id_nhom)\
        .join(thuoc_nhom_1,Nhom.id_nhom == thuoc_nhom_1.id_nhom)\
        .join(nguoi_dung_1,nguoi_dung_1.id_nguoi_dung ==  thuoc_nhom_1.id_nguoi_dung)\
        .join(thuoc_nhom_2,Nhom.id_nhom == thuoc_nhom_2.id_nhom)\
        .join(nguoi_dung_2,nguoi_dung_2.id_nguoi_dung ==  thuoc_nhom_2.id_nguoi_dung)\
        .filter(nguoi_dung_1.id_nguoi_dung != nguoi_dung_2.id_nguoi_dung)\
        .filter(nguoi_dung_1.id_nguoi_dung == id_nguoi_dung_1)\
        .filter(nguoi_dung_2.id_nguoi_dung == id_nguoi_dung_2)\
        .group_by(Nhom.id_nhom)\
        .first()

        if not(nhom and nhom[1]==2):
            nguoi_dung_1 = NguoiDung.query.filter(NguoiDung.id_nguoi_dung == id_nguoi_dung_1).first()
            nguoi_dung_2 = NguoiDung.query.filter(NguoiDung.id_nguoi_dung == id_nguoi_dung_2).first()

            nhom = Nhom(ten_nhom = nguoi_dung_1.tai_khoan+"_"+nguoi_dung_2.tai_khoan)
            db.session.add(nhom)
            db.session.commit()

            thuoc_nhom_1 = ThuocNhom(id_nguoi_dung = id_nguoi_dung_1, id_nhom = nhom.id_nhom)
            thuoc_nhom_2 = ThuocNhom(id_nguoi_dung = id_nguoi_dung_2, id_nhom = nhom.id_nhom)
            db.session.add(thuoc_nhom_1)
            db.session.add(thuoc_nhom_2)

            db.session.commit()
  
        ds_tin_nhan = TinNhan.query.filter(TinNhan.id_nhom == nhom.id_nhom).all()
        ds_tin_nhan_2 =[]
        for tin_nhan in ds_tin_nhan:
            ds_tin_nhan_2.append({"noi_dung": tin_nhan.noi_dung,
                              "kiem_tra": tin_nhan.id_nguoi_dung == id_nguoi_dung_2})
        
        return {"nhom":lay_nhom(id_nhom=nhom.id_nhom,id_nguoi_dung=id_nguoi_dung_2),
                "ds_tin_nhan": ds_tin_nhan_2}


def lay_nhom(id_nhom,id_nguoi_dung):
    nguoi_dung_1 = aliased(NguoiDung)
    thuoc_nhom_1 = aliased(ThuocNhom)

    nguoi_dung_2 = aliased(NguoiDung)
    thuoc_nhom_2 = aliased(ThuocNhom)
    nhom_chat = db.session.query(Nhom.id_nhom,nguoi_dung_2.ten_nguoi_dung,nguoi_dung_2.hinh_anh)\
    .join(thuoc_nhom_1,Nhom.id_nhom == thuoc_nhom_1.id_nhom)\
    .join(nguoi_dung_1,nguoi_dung_1.id_nguoi_dung ==  thuoc_nhom_1.id_nguoi_dung)\
    .join(thuoc_nhom_2,Nhom.id_nhom == thuoc_nhom_2.id_nhom)\
    .join(nguoi_dung_2,nguoi_dung_2.id_nguoi_dung ==  thuoc_nhom_2.id_nguoi_dung)\
    .filter(nguoi_dung_1.id_nguoi_dung != nguoi_dung_2.id_nguoi_dung)\
    .filter(nguoi_dung_1.id_nguoi_dung == id_nguoi_dung)\
    .filter(Nhom.id_nhom == id_nhom)\
    .first()

    thong_tin_khac = db.session.query(TinNhan.noi_dung)\
    .join(NguoiDung_TinNhan,NguoiDung_TinNhan.id_tin_nhan == TinNhan.id_tin_nhan,isouter=True)\
    .filter(NguoiDung_TinNhan.id_nguoi_dung == id_nguoi_dung)\
    .filter(nhom_chat.id_nhom == TinNhan.id_nhom)\
    .order_by(TinNhan.id_tin_nhan.desc()).first()

    db.session.commit()
    nhom_chat_2 = {"id_nhom":nhom_chat.id_nhom,
                   "ten_nguoi_dung":nhom_chat.ten_nguoi_dung,
                   "hinh_anh": nhom_chat.hinh_anh,
                   "noi_dung": thong_tin_khac[0] if thong_tin_khac else "chưa có tin nhắn nào"}
    return nhom_chat_2

def tao_tin_nhan_moi(id_nhom,noi_dung,id_nguoi_dung):
    tin_nhan = TinNhan(id_nhom = id_nhom,noi_dung=noi_dung,id_nguoi_dung=id_nguoi_dung,thoi_gian = datetime.now())
    db.session.add(tin_nhan)
    db.session.commit()
    ds_nguoi_dung  = db.session.query(NguoiDung)\
    .join(ThuocNhom,NguoiDung.id_nguoi_dung == ThuocNhom.id_nguoi_dung)\
    .join(Nhom,Nhom.id_nhom == ThuocNhom.id_nhom)\
    .filter(Nhom.id_nhom==id_nhom).all()

    for nguoi_dung in ds_nguoi_dung:
        if nguoi_dung.id_nguoi_dung == id_nguoi_dung:
            nguoidung_tinnhan = NguoiDung_TinNhan(id_nguoi_dung=nguoi_dung.id_nguoi_dung,id_tin_nhan=tin_nhan.id_tin_nhan,thoi_gian_xem=datetime.now(),thoi_gian_nhan=datetime.now())
        else:
            nguoidung_tinnhan = NguoiDung_TinNhan(id_nguoi_dung=nguoi_dung.id_nguoi_dung,id_tin_nhan=tin_nhan.id_tin_nhan)           
        db.session.add(nguoidung_tinnhan)
    db.session.commit()

    nhom_chat_2 = lay_nhom(id_nguoi_dung=id_nguoi_dung,id_nhom=id_nhom)
    
    return nhom_chat_2

def lay_ds_nhom_chua_nhan(id_nguoi_dung,id_nhom):
    nguoi_dung_1 = aliased(NguoiDung)
    thuoc_nhom_1 = aliased(ThuocNhom)

    nguoi_dung_2 = aliased(NguoiDung)
    thuoc_nhom_2 = aliased(ThuocNhom)


    ds_nhom_chat = db.session.query(Nhom.id_nhom,nguoi_dung_2.id_nguoi_dung,nguoi_dung_2.ten_nguoi_dung,nguoi_dung_2.hinh_anh)\
    .join(thuoc_nhom_1,Nhom.id_nhom == thuoc_nhom_1.id_nhom)\
    .join(nguoi_dung_1,nguoi_dung_1.id_nguoi_dung ==  thuoc_nhom_1.id_nguoi_dung)\
    .join(thuoc_nhom_2,Nhom.id_nhom == thuoc_nhom_2.id_nhom)\
    .join(nguoi_dung_2,nguoi_dung_2.id_nguoi_dung ==  thuoc_nhom_2.id_nguoi_dung)\
    .filter(nguoi_dung_1.id_nguoi_dung != nguoi_dung_2.id_nguoi_dung)\
    .filter(nguoi_dung_1.id_nguoi_dung == id_nguoi_dung)\
    .all()

    ds_nhom_chat_2=[]

    for nhom_chat in ds_nhom_chat:
        thong_tin_khac = db.session.query(TinNhan.noi_dung,NguoiDung_TinNhan.thoi_gian_nhan)\
        .join(NguoiDung_TinNhan,NguoiDung_TinNhan.id_tin_nhan == TinNhan.id_tin_nhan,isouter=True)\
        .filter(NguoiDung_TinNhan.id_nguoi_dung == id_nguoi_dung)\
        .filter(NguoiDung_TinNhan.thoi_gian_nhan == None)\
        .filter(nhom_chat.id_nhom == TinNhan.id_nhom)\
        .order_by(TinNhan.id_tin_nhan.desc()).first()
        
        if thong_tin_khac:
            ds_nhom_chat_2.append({
                "kiem_tra": nhom_chat.id_nguoi_dung == id_nguoi_dung,
                "id_nhom": nhom_chat.id_nhom,
                "ten_nguoi_dung": nhom_chat.ten_nguoi_dung,
                "hinh_anh": nhom_chat.hinh_anh,
                "noi_dung": thong_tin_khac[0],
                "thoi_gian_nhan" : thong_tin_khac[1]
            })


    ds_nguoidung_tinnhan = NguoiDung_TinNhan.query.filter(NguoiDung_TinNhan.id_nguoi_dung == id_nguoi_dung,NguoiDung_TinNhan.thoi_gian_nhan==None).all()
    for nguoidung_tinnhan in ds_nguoidung_tinnhan:
        nguoidung_tinnhan.thoi_gian_nhan = datetime.now()


    ds_nguoidung_tinnhan = db.session.query(NguoiDung_TinNhan)\
    .join(NguoiDung,NguoiDung_TinNhan.id_nguoi_dung == NguoiDung.id_nguoi_dung)\
    .join(TinNhan,NguoiDung_TinNhan.id_tin_nhan == TinNhan.id_tin_nhan)\
    .join(Nhom,Nhom.id_nhom == TinNhan.id_nhom)\
    .filter(Nhom.id_nhom == id_nhom)\
    .filter(NguoiDung_TinNhan.thoi_gian_xem == None)\
    .filter(NguoiDung.id_nguoi_dung == id_nguoi_dung)\
    .all()



    for nguoidung_tinnhan in ds_nguoidung_tinnhan:
        nguoidung_tinnhan.thoi_gian_xem = datetime.now()

    db.session.commit()

    return ds_nhom_chat_2

def lay_ds_tin_nhan(id_nhom,id_nguoi_dung):
    ds_tin_nhan = TinNhan.query.filter(TinNhan.id_nhom == id_nhom).all()
    ds_tin_nhan_2 =[]
    for tin_nhan in ds_tin_nhan:
        ds_tin_nhan_2.append({"noi_dung": tin_nhan.noi_dung,
                              "kiem_tra": tin_nhan.id_nguoi_dung == id_nguoi_dung})
        
    ds_nguoidung_tinnhan = db.session.query(NguoiDung_TinNhan)\
    .join(NguoiDung,NguoiDung_TinNhan.id_nguoi_dung == NguoiDung.id_nguoi_dung)\
    .join(TinNhan,NguoiDung_TinNhan.id_tin_nhan == TinNhan.id_tin_nhan)\
    .join(Nhom,Nhom.id_nhom == TinNhan.id_nhom)\
    .filter(Nhom.id_nhom == id_nhom)\
    .filter(NguoiDung_TinNhan.thoi_gian_xem == None)\
    .filter(NguoiDung.id_nguoi_dung == id_nguoi_dung)\
    .all()

    for nguoidung_tinnhan in ds_nguoidung_tinnhan:
        nguoidung_tinnhan.thoi_gian_xem = datetime.now()
    db.session.commit()

    return ds_tin_nhan_2


if __name__ == "__main__":
    with app.app_context():
        pass
