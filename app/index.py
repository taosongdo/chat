from flask import render_template,request,jsonify,redirect
from app import app,login
from app.models import NguoiDung
from app import dao as dao
from flask_login import login_user,current_user,login_required

@login.user_loader
def load_user(id_nguoi_dung):
    return NguoiDung.query.filter(NguoiDung.id_nguoi_dung==id_nguoi_dung).first()

@app.route("/", methods=["POST","GET"])
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
    
#api

@app.route("/api/LayDsTimKiem",methods=["POST"])
def lay_ds_tim_kiem():  
    tu_khoa = request.json.get("tu_khoa")
    ds_nguoi_dung = dao.lay_ds_nguoi_dung(tu_khoa=tu_khoa,id_nguoi_dung = current_user.id_nguoi_dung)
    return jsonify(ds_nguoi_dung)

@app.route("/api/LayDsNhomChat",methods=["POST"])
def lay_ds_nhom_chat():
    ds_nhom_chat = dao.lay_ds_nhom(id_nguoi_dung=current_user.id_nguoi_dung)
    print(ds_nhom_chat)
    return jsonify(ds_nhom_chat)

@app.route("/api/TaoTinNhanMoi",methods=["POST"])
def tao_tin_nhan_moi():
    noi_dung = request.json.get("noi_dung")
    id_nhom = request.json.get("id_nhom")
    nhom = dao.tao_tin_nhan_moi(id_nguoi_dung=current_user.id_nguoi_dung,noi_dung=noi_dung,id_nhom=id_nhom)
    return jsonify(nhom)

@app.route("/api/TaoNhomMoi",methods=["POST"])
def tao_nhom_moi():
    id_nguoi_dung = request.json.get("id_nguoi_dung")
    ket_qua = dao.tao_nhom_moi(id_nguoi_dung_1=id_nguoi_dung,id_nguoi_dung_2=current_user.id_nguoi_dung)
    return jsonify(ket_qua)

@app.route("/api/LayDuLieuTheoThoiGian",methods=["POST"])
def lay_du_lieu_theo_thoi_gian():
    id_nhom = request.json.get("id_nhom")
    ds_nhom_chua_nhan = dao.lay_ds_nhom_chua_nhan(id_nguoi_dung=current_user.id_nguoi_dung,id_nhom=id_nhom)
    return jsonify(ds_nhom_chua_nhan)

@app.route("/api/LayDsTinNhan",methods=["POST"])
def lay_ds_tin_nhan():
    id_nhom = request.json.get("id_nhom")

    return jsonify(dao.lay_ds_tin_nhan(id_nhom=id_nhom,id_nguoi_dung=current_user.id_nguoi_dung))
if __name__ == "__main__":
    app.run()