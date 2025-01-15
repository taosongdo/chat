from flask import render_template,request,jsonify,redirect,session
from app import app,login
import hashlib
from app import utils
from app.models import NguoiDung
from app import dao 
from flask_login import login_user,current_user,login_required

@login.user_loader
def load_user(id_nguoi_dung):
    return NguoiDung.query.filter(NguoiDung.id_nguoi_dung==id_nguoi_dung).first()

@app.route("/DangNhap", methods=["POST","GET"])
def dang_nhap():
    if not(current_user.is_authenticated):
        err = None
        if request.method == "POST":
            tai_khoan = request.form.get("tai_khoan")
            mat_khau = request.form.get("mat_khau")
            nguoi_dung = dao.lay_nguoi_dung_dang_nhap(mat_khau=mat_khau, tai_khoan=tai_khoan)
            if nguoi_dung:
                login_user(nguoi_dung)
                return redirect("/TrangChat")
            else:
                err = True
        return render_template("TrangDangNhap.html",err=err)
    return redirect("/TrangChat")

@app.route("/TrangChat", methods=["GET"])
def chat():
    return render_template("TrangChat.html")

@app.route("/DangKy", methods=["GET","POST"])
def dang_ky():
    buoc = 1
    err = None
    if request.method == "POST":
        buoc = int(request.form.get("buoc"))
        if buoc == 2:
            ten_nguoi_dung = request.form.get("ten_nguoi_dung")
            tai_khoan = request.form.get("tai_khoan")
            email = request.form.get("email")
            mat_khau = request.form.get("mat_khau")
            nguoi_dung = dao.kiem_tra_thong_tin(ten_nguoi_dung,tai_khoan,email,mat_khau)
            if nguoi_dung:
                buoc = 1
                err = "thông tin đã đc dùng để tạo tài khoản hoặc thông tin ko hợp lệ"
            else:
                xac_nhan_mat_khau = request.form.get("xac_nhan_mat_khau")
                if mat_khau != xac_nhan_mat_khau:
                    err = "xác nhận và mật khẩu ko giống nhau"
                    buoc = 1
                else:
                    err = "mã đã được gửi về email của bạn"
                    session["ten_nguoi_dung"] = ten_nguoi_dung
                    session["tai_khoan"] = tai_khoan
                    session["email"] = email
                    session["mat_khau"] = str(hashlib.md5(mat_khau.encode('utf-8')).hexdigest())
                    session["ma_xac_nhan_email"] = utils.gui_email(email)
        elif buoc == 3:
            ma_xac_nhan_email = request.form.get("ma_xac_nhan_email")
            if session["ma_xac_nhan_email"] == ma_xac_nhan_email:
                nguoi_dung = dao.tao_nguoi_dung_moi(ten_nguoi_dung=session["ten_nguoi_dung"],tai_khoan=session["tai_khoan"],email=session["email"],mat_khau=session["mat_khau"])
                session['id_nguoi_dung'] = nguoi_dung.id_nguoi_dung
            else:
                err = "mã không trùng khớp"
                buoc = 2
        elif buoc == 4:
            hinh_anh = request.files.get("hinh_anh")
            dao.sua_nguoi_dung(id_nguoi_dung=session['id_nguoi_dung'],hinh_anh=hinh_anh)
            return redirect("/DangNhap")
    return render_template("TrangDangKy.html",buoc=buoc,err=err)
        
#api
@app.route("/api/LayDsTimKiem",methods=["POST"])
@login_required
def lay_ds_tim_kiem():  
    tu_khoa = request.json.get("tu_khoa")
    ds_nguoi_dung = dao.lay_ds_nguoi_dung(tu_khoa=tu_khoa,id_nguoi_dung = current_user.id_nguoi_dung)
    return jsonify(ds_nguoi_dung)

@app.route("/api/LayDsNhomChat",methods=["POST"])
@login_required
def lay_ds_nhom_chat():
    ds_nhom_chat = dao.lay_ds_nhom(id_nguoi_dung=current_user.id_nguoi_dung)
    return jsonify(ds_nhom_chat)

@app.route("/api/TaoTinNhanMoi",methods=["POST"])
@login_required
def tao_tin_nhan_moi():
    noi_dung = request.json.get("noi_dung")
    id_nhom = request.json.get("id_nhom")
    nhom = dao.tao_tin_nhan_moi(id_nguoi_dung=current_user.id_nguoi_dung,noi_dung=noi_dung,id_nhom=id_nhom)
    return jsonify(nhom)

@app.route("/api/TaoNhomMoi",methods=["POST"])
@login_required
def tao_nhom_moi():
    id_nguoi_dung = request.json.get("id_nguoi_dung")
    ket_qua = dao.tao_nhom_moi(id_nguoi_dung_1=id_nguoi_dung,id_nguoi_dung_2=current_user.id_nguoi_dung)
    return jsonify(ket_qua)

@app.route("/api/LayDuLieuTheoThoiGian",methods=["POST"])
@login_required
def lay_du_lieu_theo_thoi_gian():
    id_nhom = request.json.get("id_nhom")
    ds_nhom_chua_nhan = dao.lay_ds_nhom_chua_nhan(id_nguoi_dung=current_user.id_nguoi_dung,id_nhom=id_nhom)
    return jsonify(ds_nhom_chua_nhan)

@app.route("/api/LayDsTinNhan",methods=["POST"])
@login_required
def lay_ds_tin_nhan():
    id_nhom = request.json.get("id_nhom")
    return jsonify(dao.lay_ds_tin_nhan(id_nhom=id_nhom,id_nguoi_dung=current_user.id_nguoi_dung))

@app.route("/api/LayDsTinNhanTiepTheo",methods=["POST"])
@login_required
def lay_ds_tin_nhan_tiep_theo():
    bat_dau = request.json.get("bat_dau")
    id_nhom = request.json.get("id_nhom")
    return jsonify(dao.lay_ds_tin_nhan(id_nhom=id_nhom,id_nguoi_dung=current_user.id_nguoi_dung,bat_dau=bat_dau))

if __name__ == "__main__":
    app.run()