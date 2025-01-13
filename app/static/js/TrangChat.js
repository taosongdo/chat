// var idTinNhan
// var idNguoiDung
// var idNguoiNhan
// var idThoiGianDung
// var idThoiGianLayTinNhan
var idNhomHienThi

const layDuLieu = (tinNhan) => {
    tinNhan2 = ""
    if (tinNhan.includes("https://")) {
        tinNhan = `<a href="${tinNhan}}">${tinNhan}</a>`
    }

    while (20 < tinNhan.length) {
        tinNhanTruoc = tinNhan.substring(0, 20)
        viTri = tinNhanTruoc.lastIndexOf(" ") === -1 ? 20 : tinNhanTruoc.lastIndexOf(" ")
        if (viTri == 0) {
            tinNhan = tinNhan.substring(1)
        }
        else {
            tinNhan2 += tinNhan.substring(0, viTri) + "\n"
            tinNhan = tinNhan.substring(viTri)
        }
    }

    tinNhan2 += tinNhan
    return tinNhan2
}

const catNganDuLieu = (tinNhan, kiemTra) => {
    if (kiemTra) {
        tinNhan = "bạn: " + tinNhan
    }
    if (tinNhan.length > 15) {
        tinNhan = tinNhan.substring(0, 15) + "..."
    }

    return tinNhan
}


const loadNhapTimKiem = () => {
    var inputThanhTimKiem = document.getElementById("idInputThanhTimKiem")
    inputThanhTimKiem.addEventListener('input', () => {

        var divDsNhomChat = document.getElementById("idDivDsNhomChat")
        var divDsKetQua = document.getElementById("idDivDsKetQua")
        var divThanhTimKiemIcon = document.getElementById("idDivThanhTimKiemIcon")

        if (inputThanhTimKiem.value != "") {
            divDsKetQua.classList.add("div-ds-ket-qua-2")
            divThanhTimKiemIcon.classList.add("div-thanh-tim-kiem-icon-2")
            divDsNhomChat.style.height = document.body.offsetHeight - 270;
            fetch("/api/LayDsTimKiem", {
                "method": "post",
                "body": JSON.stringify({
                    "tu_khoa": inputThanhTimKiem.value,
                }),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }).then(res => res.json()).then(dsTimKiem => {
                divDsKetQua.innerHTML = ``
                for (timKiem of dsTimKiem) {
                    divDsKetQua.innerHTML +=
                        `
                        <div class="div-ket-qua" id="idDivKetQua${timKiem.id_nguoi_dung}">
                            <button class="button-ket-qua" onclick="taoNhom('${timKiem.id_nguoi_dung}','${timKiem.hinh_anh}')">
                                <div class="div-avatar-ket-qua">
                                    <img class="img-avatar-ket-qua" src="${timKiem.hinh_anh}"/>
                                </div>
                                <div class="div-ten-ket-qua">
                                    <h4>${timKiem.ten_nguoi_dung}</h4>
                                </div>
                            </button>
                        </div>
                    `
                }
            })
        }
        else {
            divDsKetQua.classList.remove("div-ds-ket-qua-2")
            divThanhTimKiemIcon.classList.remove("div-thanh-tim-kiem-icon-2")
            divDsNhomChat.style.height = document.body.offsetHeight - 60;
        }


    });

}

const loadNhomTinNhan = () => {
    var divDsNhomChat = document.getElementById("idDivDsNhomChat")
    fetch("/api/LayDsNhomChat", {
        "method": "POST",
        "headers": {
            "Content-type": "application-json"
        }
    }).then(res => res.json()).then(dsNhomChat => {
        for (nhomChat of dsNhomChat) {

            if (nhomChat.thoi_gian_xem == null) {
                divDsNhomChat.innerHTML =
                    `
                    <div class="div-nhom-tin-nhan" id="idDivNhomTinNhan${nhomChat.id_nhom}">
                        <button class="button-nhom-tin-nhan" onclick="chonNhom(${nhomChat.id_nhom},'${nhomChat.ten_nguoi_dung}','${nhomChat.hinh_anh}')">
                            <div class="div-avatar-nhom-tin-nhan">
                                <img class="img-avatar-nhom-tin-nhan" src="${nhomChat.hinh_anh}"/>
                            </div>
                            <div class="div-thong-tin-nhom-tin-nhan div-thong-tin-nhom-tin-nhan-2">
                                <h3 class="h1-ten-nhom-tin-nhan">${nhomChat.ten_nguoi_dung}</h3>
                                <div class="div-tin-nhan-nhom-tin-nhan">${catNganDuLieu(nhomChat.noi_dung, nhomChat.kiem_tra)}</div>
                            </div>
                        </button>
                    </div>  
                `+ divDsNhomChat.innerHTML

            }
            else {
                divDsNhomChat.innerHTML +=
                    `
                    <div class="div-nhom-tin-nhan" id="idDivNhomTinNhan${nhomChat.id_nhom}">
                        <button class="button-nhom-tin-nhan" onclick="chonNhom(${nhomChat.id_nhom},'${nhomChat.ten_nguoi_dung}','${nhomChat.hinh_anh}')">
                            <div class="div-avatar-nhom-tin-nhan">
                                <img class="img-avatar-nhom-tin-nhan" src="${nhomChat.hinh_anh}"/>
                            </div>
                            <div class="div-thong-tin-nhom-tin-nhan">
                                <h3 class="h1-ten-nhom-tin-nhan">${nhomChat.ten_nguoi_dung}</h3>
                                <div class="div-tin-nhan-nhom-tin-nhan">${catNganDuLieu(nhomChat.noi_dung, nhomChat.kiem_tra)}</div>
                            </div>
                        </button>
                    </div>  
                `
            }
        }
    })
}

const taoNhom = (id_nguoi_dung, hinh_anh) => {
    fetch("/api/TaoNhomMoi", {
        "method": "POST",
        "body": JSON.stringify({
            "id_nguoi_dung": id_nguoi_dung
        }),
        "headers": {
            "Content-type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        var divThanhTimKiemIcon = document.getElementById("idDivThanhTimKiemIcon")
        divThanhTimKiemIcon.classList.remove("div-thanh-tim-kiem-icon-2")

        var divDsKetQua = document.getElementById("idDivDsKetQua")
        divDsKetQua.classList.remove("div-ds-ket-qua-2")

        var divNhapLieuNutGui = document.getElementById("idDivNhapLieuNutGui")
        divNhapLieuNutGui.classList.remove("div-nhap-lieu-nut-gui-2")

        idNhomHienThi = data.nhom.id_nhom

        var inputThanhTimKiem = document.getElementById("idInputThanhTimKiem")

        divDsNhom = document.getElementById("idDivDsNhomChat")
        divNhom = document.getElementById(`idDivNhomTinNhan${data.nhom.id_nhom}`)
        if (divNhom) {
            divDsNhom.removeChild(divNhom)
        } 

        divDsNhom.innerHTML =
            `
            <div class="div-nhom-tin-nhan" id = "idDivNhomTinNhan${data.nhom.id_nhom}">
                <button class="button-nhom-tin-nhan" onclick="chonNhom(${data.nhom.id_nhom},'${data.nhom.ten_nguoi_dung}','${data.nhom.hinh_anh}')">
                    <div class="div-avatar-nhom-tin-nhan">
                        <img class="img-avatar-nhom-tin-nhan" src="${data.nhom.hinh_anh}"/>
                    </div>
                    <div class="div-thong-tin-nhom-tin-nhan">
                        <h3 class="h1-ten-nhom-tin-nhan">${data.nhom.ten_nguoi_dung}</h3>
                        <div class="div-tin-nhan-nhom-tin-nhan">${catNganDuLieu(data.nhom.noi_dung, data.nhom.kiem_tra)}</div>
                    </div>
                </button>
            </div>
            `+ divDsNhom.innerHTML

        inputThanhTimKiem.value = ""

        var divDsTinNhan = document.getElementById("idDivDsTinNhan")
        divDsTinNhan.innerHTML = ``

        for (tinNhan of data.ds_tin_nhan) {
            clas = "trai"
            if (tinNhan.kiem_tra) {
                clas = "phai"
            }
            divDsTinNhan.innerHTML +=
                `
                <div class="div-tin-nhan-${clas}">
                    <div class="div-block-${clas}">
                        ${layDuLieu(tinNhan.noi_dung)}
                    </div>
                </div >
            `
            divDsTinNhan.scrollTop = divDsTinNhan.scrollHeight
        }

        var divThongTinNhomTinNhanChon = document.getElementById("idDivThongTinNhomTinNhanChon")
        divThongTinNhomTinNhanChon.innerHTML =
            `
                <div class="div-avatar-nhom-tin-nhan-chon">
                    <img class="img-avatar-nhom-tin-nhan-chon" src="${hinh_anh}" />
                </div>
                <h1 class="div-ten-nhom-tin-nhan-chon">${data.nhom.ten_nguoi_dung}</h1>
                `

        if (window.innerWidth < 768) {
            var divNhomTinNhanChon = document.getElementById("idDivNhomTinNhanChon")
            var divDsBan = document.getElementById("idDivDsBan")
            divNhomTinNhanChon.classList.remove("d-none")
            divDsBan.classList.add("d-none")
        }
    })

}

const xemMenu = () => {
    var divNhomTinNhanChon = document.getElementById("idDivNhomTinNhanChon")
    var divDsBan = document.getElementById("idDivDsBan")
    divNhomTinNhanChon.classList.add("d-none")
    divDsBan.classList.remove("d-none")
}

const chonNhom = (idNhom, tenNguoiDung, hinhAnh) => {
    idNhomHienThi = idNhom

    var divNhapLieuNutGui = document.getElementById("idDivNhapLieuNutGui")
    divNhapLieuNutGui.classList.remove("div-nhap-lieu-nut-gui-2")

    var divDsTinNhan = document.getElementById("idDivDsTinNhan")
    divDsTinNhan.innerHTML = ``

    var divThongTinNhomTinNhanChon = document.getElementById("idDivThongTinNhomTinNhanChon")
    divThongTinNhomTinNhanChon.innerHTML =
        `
            <div class="div-avatar-nhom-tin-nhan-chon">
                <img class="img-avatar-nhom-tin-nhan-chon" src="${hinhAnh}" />
            </div>
            <h1 class="div-ten-nhom-tin-nhan-chon">${tenNguoiDung}</h1>
            `

    fetch("/api/LayDsTinNhan", {
        "method": "POST",
        "body": JSON.stringify({
            "id_nhom": idNhomHienThi
        }),
        "headers": {
            "Content-type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        for (tinNhan of data) {
            clas = "trai"
            if (tinNhan.kiem_tra) {
                clas = "phai"
            }
            divDsTinNhan.innerHTML +=
                `
                    <div class="div-tin-nhan-${clas}">
                        <div class="div-block-${clas}">
                            ${layDuLieu(tinNhan.noi_dung)}
                        </div>
                    </div >
                `
            divDsTinNhan.scrollTop = divDsTinNhan.scrollHeight

            var divNhapLieuNutGui = document.querySelector(`#idDivNhomTinNhan${idNhomHienThi} .div-thong-tin-nhom-tin-nhan`)
            divNhapLieuNutGui.classList.remove("div-thong-tin-nhom-tin-nhan-2")
        }
    })
    if (window.innerWidth < 768) {
        var divNhomTinNhanChon = document.getElementById("idDivNhomTinNhanChon")
        var divDsBan = document.getElementById("idDivDsBan")
        divNhomTinNhanChon.classList.remove("d-none")
        divDsBan.classList.add("d-none")
    }
}

const gui = () => {
    var inputNhapLieu = document.getElementById("idInputNhapLieu")
    if (inputNhapLieu.value.trim() != "") {

        fetch("/api/TaoTinNhanMoi", {
            "method": "POST",
            "body": JSON.stringify({
                "noi_dung": inputNhapLieu.value,
                "id_nhom": idNhomHienThi
            }),
            "headers": {
                "Content-type": "application/json"
            }
        }).then(res => res.json()).then(data => {

            var divDsTinNhan = document.getElementById("idDivDsTinNhan")
            divDsTinNhan.innerHTML +=
                `
            <div class="div-tin-nhan-phai" >
                <div class="div-block-phai">
                    ${layDuLieu(data.noi_dung)}
                </div>
            </div >
            `
            divDsTinNhan.scrollTop = divDsTinNhan.scrollHeight

            divDsNhom = document.getElementById("idDivDsNhomChat")
            divNhom = document.getElementById(`idDivNhomTinNhan${data.id_nhom}`)
            divDsNhom.removeChild(divNhom)
            divDsNhom.innerHTML =
                `
                <div class="div-nhom-tin-nhan" id = "idDivNhomTinNhan${data.id_nhom}">
                    <button class="button-nhom-tin-nhan" onclick="chonNhom(${data.id_nhom},'${data.ten_nguoi_dung}','${data.hinh_anh}')">
                        <div class="div-avatar-nhom-tin-nhan">
                            <img class="img-avatar-nhom-tin-nhan" src="${data.hinh_anh}"/>
                        </div>
                        <div class="div-thong-tin-nhom-tin-nhan">
                            <h3 class="h1-ten-nhom-tin-nhan">${data.ten_nguoi_dung}</h3>
                            <div class="div-tin-nhan-nhom-tin-nhan">${catNganDuLieu(data.noi_dung, data.kiem_tra)}</div>
                        </div>
                    </button>
                </div>
    `+ divDsNhom.innerHTML
            inputNhapLieu.value = ""
        })
    }
}


const loadSuKienEnter = () => {
    document.addEventListener('keydown', (event) => {
        if (event.key == 'Enter') {
            gui()
        }
    })
}

const layDuLieuTheoThoiGian = () => {
    setInterval(() => {
        fetch("/api/LayDuLieuTheoThoiGian", {
            "method": "POST",
            "body": JSON.stringify({
                "id_nhom": idNhomHienThi
            }),
            "headers": {
                "Content-type": "application/json"
            }
        }).then(res => res.json()).then(dsNhom => {

            divDsNhom = document.getElementById("idDivDsNhomChat")
            dsNhom2 = ``
            
            for (nhom of dsNhom) {

                divNhom = document.getElementById(`idDivNhomTinNhan${nhom.id_nhom}`)
                divDsNhom.removeChild(divNhom)

                if (nhom.id_nhom != idNhomHienThi) {
                    dsNhom2 =
                        `
                            <div class="div-nhom-tin-nhan" id = "idDivNhomTinNhan${nhom.id_nhom}">
                                <button class="button-nhom-tin-nhan" onclick="chonNhom(${nhom.id_nhom},'${nhom.ten_nguoi_dung}','${nhom.hinh_anh}')">
                                    <div class="div-avatar-nhom-tin-nhan">
                                        <img class="img-avatar-nhom-tin-nhan" src="${nhom.hinh_anh}" />
                                    </div>
                                    <div class="div-thong-tin-nhom-tin-nhan div-thong-tin-nhom-tin-nhan-2">
                                        <h3 class="h1-ten-nhom-tin-nhan">${nhom.ten_nguoi_dung}</h3>
                                        <div class="div-tin-nhan-nhom-tin-nhan">${catNganDuLieu(nhom.noi_dung, nhom.kiem_tra)}</div>
                                    </div>
                                </button>
                            </div>
                        `+ dsNhom2
                }
                else {

                    dsNhom2 +=
                        `
                            <div class="div-nhom-tin-nhan" id = "idDivNhomTinNhan${nhom.id_nhom}" >
                                <button class="button-nhom-tin-nhan" onclick="chonNhom(${nhom.id_nhom},'${nhom.ten_nguoi_dung}','${nhom.hinh_anh}')">
                                    <div class="div-avatar-nhom-tin-nhan">
                                        <img class="img-avatar-nhom-tin-nhan" src="${nhom.hinh_anh}" />
                                    </div>
                                    <div class="div-thong-tin-nhom-tin-nhan">
                                        <h3 class="h1-ten-nhom-tin-nhan">${nhom.ten_nguoi_dung}</h3>
                                        <div class="div-tin-nhan-nhom-tin-nhan">${catNganDuLieu(nhom.noi_dung, nhom.kiem_tra)}</div>
                                    </div>
                                </button>
                            </div>
                        `
                    var divDsTinNhan = document.getElementById("idDivDsTinNhan")
                    var clas = "trai"
                    if (nhom.kiem_tra) {
                        clas = "phai"
                    }
                    divDsTinNhan.innerHTML +=
                        `
                            <div class="div-tin-nhan-${clas}">
                                <div class="div-block-${clas}">
                                    ${layDuLieu(nhom.noi_dung)}
                                </div>
                            </div>
                        `
                    divDsTinNhan.scrollTop = divDsTinNhan.scrollHeight
                }
            }
            if (dsNhom2 != ``) {
                divDsNhom.innerHTML = dsNhom2 + divDsNhom.innerHTML
            }
        })
    }, 1000)
}

window.onload = async () => {
    var divDsTinNhan = document.getElementById("idDivDsTinNhan")
    var divDsNhomChat = document.getElementById("idDivDsNhomChat")
    divDsNhomChat.style.height = document.body.offsetHeight - 60;
    divDsTinNhan.style.height = document.body.offsetHeight - 120;
    loadNhapTimKiem()
    loadNhomTinNhan()
    loadSuKienEnter()
    layDuLieuTheoThoiGian()
}