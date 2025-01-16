from app.models import TinNhan,NguoiDung,Nhom,ThuocNhom,NguoiDung_TinNhan
from sqlalchemy.orm import aliased
from sqlalchemy import or_
import hashlib,re
import cloudinary.uploader
from datetime import datetime
from app import db,app

def tao_nguoi_dung_moi(ten_nguoi_dung,tai_khoan,mat_khau,email):
    nguoi_dung = NguoiDung(ten_nguoi_dung=ten_nguoi_dung,tai_khoan=tai_khoan,mat_khau=mat_khau,email=email,hinh_anh="https://res.cloudinary.com/dx6brcofe/image/upload/v1736245841/woxspsofipalpoz8r4aj.jpg")
    db.session.add(nguoi_dung)
    db.session.commit()
    return nguoi_dung

def sua_nguoi_dung(id_nguoi_dung,hinh_anh=None):
    nguoi_dung = NguoiDung.query.filter(NguoiDung.id_nguoi_dung == id_nguoi_dung).first()
    if hinh_anh:
        res = cloudinary.uploader.upload(hinh_anh)
        nguoi_dung.hinh_anh = res['secure_url']
    
    db.session.commit()
    
def kiem_tra_thong_tin(tai_khoan,ten_nguoi_dung,email,mat_khau):
    if re.match(r'^[A-Za-z0-9!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~-]+$', tai_khoan) and re.match(r'^[A-Za-z0-9!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~-]+$', mat_khau):
        return True
    return NguoiDung.query.filter(or_(NguoiDung.tai_khoan == tai_khoan,NguoiDung.email == email)).first()



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
    .join(TinNhan,TinNhan.id_nhom == Nhom.id_nhom)\
    .filter(nguoi_dung_1.id_nguoi_dung != nguoi_dung_2.id_nguoi_dung)\
    .filter(nguoi_dung_1.id_nguoi_dung == id_nguoi_dung)\
    .order_by(TinNhan.id_tin_nhan.desc())\
    .all()
    
    
    ds_nhom_chat_2 = []
    for item in ds_nhom_chat:
        if item not in ds_nhom_chat_2:
            ds_nhom_chat_2.append(item)
    
    ds_nhom_chat = ds_nhom_chat_2

    ds_nhom_chat_2 = []

    for nhom_chat in ds_nhom_chat:
        thong_tin_khac = db.session.query(TinNhan.noi_dung,NguoiDung_TinNhan.da_xem,NguoiDung.id_nguoi_dung)\
        .join(NguoiDung_TinNhan,NguoiDung_TinNhan.id_tin_nhan == TinNhan.id_tin_nhan,isouter=True)\
        .join(NguoiDung,TinNhan.id_nguoi_dung == NguoiDung.id_nguoi_dung)\
        .filter(NguoiDung_TinNhan.id_nguoi_dung == id_nguoi_dung)\
        .filter(nhom_chat.id_nhom == TinNhan.id_nhom)\
        .order_by(TinNhan.id_tin_nhan.desc()).first()
        
        ds_nhom_chat_2.append({
            "id_nhom": nhom_chat.id_nhom,
            "ten_nguoi_dung": nhom_chat.ten_nguoi_dung,
            "hinh_anh": nhom_chat.hinh_anh,
            "noi_dung": thong_tin_khac[0] if thong_tin_khac else "chưa có tin nhắn",
            "kiem_tra": thong_tin_khac[2] == id_nguoi_dung if thong_tin_khac else False,
            "da_xem" : thong_tin_khac[1] if thong_tin_khac else False
        })

    ds_nguoidung_tinnhan = NguoiDung_TinNhan.query.filter(NguoiDung_TinNhan.id_nguoi_dung == id_nguoi_dung,NguoiDung_TinNhan.da_nhan==False).all()

    for nguoidung_tinnhan in ds_nguoidung_tinnhan:
        nguoidung_tinnhan.da_nhan = True
        
    db.session.commit()

    return ds_nhom_chat_2

def tao_nhom_moi(id_nguoi_dung_1,id_nguoi_dung_2):
        nguoi_dung_1 = aliased(NguoiDung)
        thuoc_nhom_1 = aliased(ThuocNhom)

        nguoi_dung_2 = aliased(NguoiDung)
        thuoc_nhom_2 = aliased(ThuocNhom)

        nhom = db.session.query(Nhom.id_nhom)\
        .join(ThuocNhom,ThuocNhom.id_nhom == Nhom.id_nhom)\
        .join(thuoc_nhom_1,Nhom.id_nhom == thuoc_nhom_1.id_nhom)\
        .join(nguoi_dung_1,nguoi_dung_1.id_nguoi_dung ==  thuoc_nhom_1.id_nguoi_dung)\
        .join(thuoc_nhom_2,Nhom.id_nhom == thuoc_nhom_2.id_nhom)\
        .join(nguoi_dung_2,nguoi_dung_2.id_nguoi_dung ==  thuoc_nhom_2.id_nguoi_dung)\
        .filter(nguoi_dung_1.id_nguoi_dung != nguoi_dung_2.id_nguoi_dung)\
        .filter(nguoi_dung_1.id_nguoi_dung == id_nguoi_dung_1)\
        .filter(nguoi_dung_2.id_nguoi_dung == id_nguoi_dung_2)\
        .first()

        if not(nhom):
            nguoi_dung_1 = NguoiDung.query.filter(NguoiDung.id_nguoi_dung == id_nguoi_dung_1).first()
            nguoi_dung_2 = NguoiDung.query.filter(NguoiDung.id_nguoi_dung == id_nguoi_dung_2).first()

            nhom = Nhom()
            db.session.add(nhom)
            db.session.commit()

            thuoc_nhom_1 = ThuocNhom(id_nguoi_dung = id_nguoi_dung_1, id_nhom = nhom.id_nhom)
            thuoc_nhom_2 = ThuocNhom(id_nguoi_dung = id_nguoi_dung_2, id_nhom = nhom.id_nhom)
            db.session.add(thuoc_nhom_1)
            db.session.add(thuoc_nhom_2)

            db.session.commit()
  
        ds_tin_nhan = lay_ds_tin_nhan(id_nguoi_dung=id_nguoi_dung_2,id_nhom=nhom.id_nhom)
   
        ket_qua = {}
        ket_qua["nhom"] = lay_nhom(id_nhom=nhom.id_nhom,id_nguoi_dung=id_nguoi_dung_2)
        ket_qua["ds_tin_nhan"] = ds_tin_nhan["ds_tin_nhan"]
        
        if "ds_thong_tin" in ds_tin_nhan:
            ket_qua["ds_thong_tin"] = ds_tin_nhan["ds_thong_tin"]
        else:
            ket_qua["ds_nguoi_dung"] = ds_tin_nhan["ds_nguoi_dung"]

        return ket_qua

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

    thong_tin_khac = db.session.query(TinNhan.noi_dung,NguoiDung.id_nguoi_dung,TinNhan.thoi_gian)\
    .join(NguoiDung,NguoiDung.id_nguoi_dung == TinNhan.id_nguoi_dung,isouter=True)\
    .filter(nhom_chat.id_nhom == TinNhan.id_nhom)\
    .order_by(TinNhan.id_tin_nhan.desc()).first()

    db.session.commit()
    nhom_chat_2 = {
                    "id_nhom":nhom_chat.id_nhom,
                    "ten_nguoi_dung":nhom_chat.ten_nguoi_dung,
                    "hinh_anh": nhom_chat.hinh_anh,
                    "noi_dung": thong_tin_khac[0] if thong_tin_khac else "chưa có tin nhắn",
                    "kiem_tra": thong_tin_khac[1] == id_nguoi_dung if thong_tin_khac else False,
                    "thoi_gian": thong_tin_khac[2].strftime("%d-%m-%Y %H:%M:%S") if thong_tin_khac else None
    }
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
            nguoidung_tinnhan = NguoiDung_TinNhan(id_nguoi_dung=nguoi_dung.id_nguoi_dung,id_tin_nhan=tin_nhan.id_tin_nhan,da_xem=True,da_nhan=True)
        else:
            nguoidung_tinnhan = NguoiDung_TinNhan(id_nguoi_dung=nguoi_dung.id_nguoi_dung,id_tin_nhan=tin_nhan.id_tin_nhan,da_xem=False,da_nhan=False)           
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
        thong_tin_khac = db.session.query(TinNhan.noi_dung)\
        .join(NguoiDung_TinNhan,NguoiDung_TinNhan.id_tin_nhan == TinNhan.id_tin_nhan,isouter=True)\
        .filter(TinNhan.id_nguoi_dung != id_nguoi_dung)\
        .filter(TinNhan.id_nhom == nhom_chat.id_nhom)\
        .filter(NguoiDung_TinNhan.da_nhan == False)\
        .order_by(TinNhan.id_tin_nhan.desc()).first() 

        if thong_tin_khac:
            ds_nhom_chat_2.append({
                "kiem_tra": nhom_chat.id_nguoi_dung == id_nguoi_dung,
                "id_nhom": nhom_chat.id_nhom,
                "ten_nguoi_dung": nhom_chat.ten_nguoi_dung,
                "hinh_anh": nhom_chat.hinh_anh,
                "noi_dung": thong_tin_khac[0]
            })
    
    ds_nhom_chat = ds_nhom_chat_2
            
    ds_nguoi_dung_tin_nhan = db.session.query(TinNhan.noi_dung,NguoiDung_TinNhan)\
    .join(NguoiDung_TinNhan, NguoiDung_TinNhan.id_tin_nhan == TinNhan.id_tin_nhan)\
    .filter(NguoiDung_TinNhan.id_nguoi_dung == id_nguoi_dung)\
    .filter(NguoiDung_TinNhan.da_nhan == False)\
    .all()
    for nguoi_dung_tin_nhan in ds_nguoi_dung_tin_nhan:
        nguoi_dung_tin_nhan[1].da_nhan = True
        
    ds_noi_dung = []
    ds_nguoi_dung_tin_nhan = db.session.query(TinNhan.noi_dung,TinNhan.thoi_gian)\
    .join(NguoiDung,NguoiDung_TinNhan.id_nguoi_dung == NguoiDung.id_nguoi_dung)\
    .join(TinNhan,NguoiDung_TinNhan.id_tin_nhan == TinNhan.id_tin_nhan)\
    .join(Nhom,Nhom.id_nhom == TinNhan.id_nhom)\
    .filter(Nhom.id_nhom == id_nhom)\
    .filter(NguoiDung_TinNhan.da_xem == False)\
    .filter(NguoiDung.id_nguoi_dung == id_nguoi_dung)\
    .all()
    for nguoi_dung_tin_nhan in ds_nguoi_dung_tin_nhan:
        ds_noi_dung.append({
            "noi_dung":nguoi_dung_tin_nhan[0],
            "thoi_gian":nguoi_dung_tin_nhan[1]
        })
        nguoi_dung_tin_nhan[1].da_xem = True

    tin_nhan = TinNhan.query.filter(TinNhan.id_nhom == id_nhom).order_by(TinNhan.id_tin_nhan.desc()).first()
    ds_nguoi_dung_tin_nhan = []
    if tin_nhan:
        ds_nguoi_dung_tin_nhan = db.session.query(NguoiDung_TinNhan.id_nguoi_dung, NguoiDung_TinNhan.da_xem)\
        .filter(NguoiDung_TinNhan.id_tin_nhan == tin_nhan.id_tin_nhan)\
        .filter(NguoiDung_TinNhan.id_nguoi_dung != id_nguoi_dung)\
        .filter(NguoiDung_TinNhan.da_xem == True)\
        .all()
    ds_nguoi_dung_tin_nhan_2 = []
    for nguoi_dung_tin_nhan in ds_nguoi_dung_tin_nhan:
        ds_nguoi_dung_tin_nhan_2.append({
            "id_nguoi_dung": nguoi_dung_tin_nhan.id_nguoi_dung,
            "da_xem": nguoi_dung_tin_nhan.da_xem
        })
        
    ds_nguoi_dung_tin_nhan = ds_nguoi_dung_tin_nhan_2
    db.session.commit()

    return {
                "ds_nhom": ds_nhom_chat,
                "ds_nguoi_xem": ds_nguoi_dung_tin_nhan,
                "ds_noi_dung": ds_noi_dung
            }

def lay_ds_tin_nhan(id_nhom,id_nguoi_dung,bat_dau=0):
    ds_tin_nhan = TinNhan.query.filter(TinNhan.id_nhom == id_nhom).order_by(TinNhan.id_tin_nhan.desc()).offset(bat_dau).limit(20).all()
    ds_tin_nhan = list(reversed(ds_tin_nhan))
    ds_nguoi_dung_tin_nhan = db.session.query(NguoiDung_TinNhan)\
    .join(NguoiDung,NguoiDung_TinNhan.id_nguoi_dung == NguoiDung.id_nguoi_dung)\
    .join(TinNhan,NguoiDung_TinNhan.id_tin_nhan == TinNhan.id_tin_nhan)\
    .join(Nhom,Nhom.id_nhom == TinNhan.id_nhom)\
    .filter(Nhom.id_nhom == id_nhom)\
    .filter(NguoiDung_TinNhan.da_xem == False)\
    .filter(NguoiDung.id_nguoi_dung == id_nguoi_dung)\
    .all()

    for nguoidung_tinnhan in ds_nguoi_dung_tin_nhan:
        nguoidung_tinnhan.da_xem = True
        
    ds_tin_nhan_2 =[]
    ds_thong_tin = {}
    ds_nguoi_dung_da_co = []
    for tin_nhan in ds_tin_nhan:
        ds_tin_nhan_2.append({
                                "id_tin_nhan": tin_nhan.id_tin_nhan,
                                "noi_dung": tin_nhan.noi_dung,
                                "kiem_tra": tin_nhan.id_nguoi_dung == id_nguoi_dung,
                                "thoi_gian": tin_nhan.thoi_gian.strftime("%d-%m-%Y %H:%M:%S")
        })
        ds_nguoi_dung_tin_nhan = NguoiDung_TinNhan.query.filter(tin_nhan.id_tin_nhan == NguoiDung_TinNhan.id_tin_nhan).all()

        for nguoi_dung_tin_nhan in ds_nguoi_dung_tin_nhan:
            kiem_tra = True
            if nguoi_dung_tin_nhan.id_nguoi_dung in ds_nguoi_dung_da_co:
     
                kiem_tra = False
                break

            if not(nguoi_dung_tin_nhan.da_xem) and kiem_tra:
                ds_thong_tin[tin_nhan.id_tin_nhan] = []
                ds_thong_tin[tin_nhan.id_tin_nhan].append({
                    "id_nguoi_dung": nguoi_dung_tin_nhan.id_nguoi_dung,
                    "hinh_anh": NguoiDung.query.filter(NguoiDung.id_nguoi_dung == nguoi_dung_tin_nhan.id_nguoi_dung).first().hinh_anh,
                })
                ds_nguoi_dung_da_co.append(nguoi_dung_tin_nhan.id_nguoi_dung)


    ds_nguoi_dung = db.session.query(NguoiDung.id_nguoi_dung, NguoiDung.hinh_anh)\
    .join(ThuocNhom, ThuocNhom.id_nguoi_dung == NguoiDung.id_nguoi_dung)\
    .filter(ThuocNhom.id_nhom == id_nhom)\
    .filter(NguoiDung.id_nguoi_dung != id_nguoi_dung)\
    .all()

    ds_nguoi_dung_2 = []
    for nguoi_dung in ds_nguoi_dung:
        ds_nguoi_dung_2.append({
            "id_nguoi_dung": nguoi_dung[0],
            "hinh_anh": nguoi_dung[1]
        })



    db.session.commit()

    ket_qua = {}
    if len(ds_thong_tin) == 0:
        ket_qua = {
            "ds_tin_nhan": ds_tin_nhan_2,
            "ds_nguoi_dung": ds_nguoi_dung_2
            }
    else:
        ket_qua = {
            "ds_tin_nhan": ds_tin_nhan_2,
            "ds_thong_tin": ds_thong_tin
            }
        
    return ket_qua

if __name__ == "__main__":
    with app.app_context():
        pass

