// var idTinNhan
// var idNguoiDung
// var idNguoiNhan
// var idThoiGianDung
// var idThoiGianLayTinNhan
var idNhomHienThi
var soLuongTin = 0

const loadSuKienCuon = () => {
    var divDsTinNhan = document.getElementById("idDivDsTinNhan")
    divDsTinNhan.addEventListener("scroll", () => {
        if (divDsTinNhan.scrollTop == 0) {
            soLuongTin += 20
            fetch("/api/LayDsTinNhanTiepTheo", {
                "method": "POST",
                "body": JSON.stringify({
                    "bat_dau": soLuongTin,
                    "id_nhom": idNhomHienThi
                }),
                "headers": {
                    "Content-type": "application/json"
                }
            }).then(res => res.json()).then(data => {

                var divDsTinNhan = document.getElementById("idDivDsTinNhan")
                noiDung = ``
                chieuCao = divDsTinNhan.scrollHeight

                for (tinNhan of data.ds_tin_nhan) {
                    if (data.ds_thong_tin) {

                        dsNguoiDung = data.ds_thong_tin[tinNhan.id_tin_nhan]
                        if (dsNguoiDung) {
                            noiDung += `<div class="div-ds-hinh-anh-da-xem">`

                            for (nguoiDung of dsNguoiDung) {
                                divHinhAnhDaXem = document.getElementById(`idDivHinhAnhDaXem${nguoiDung.id_nguoi_dung}`)
                                divCha = divHinhAnhDaXem.parentElement
                                divCha.removeChild(divHinhAnhDaXem)
                                if (divCha.innerHTML.trim() == ``) {
                                    divDsTinNhan.removeChild(divCha)
                                }

                                noiDung +=
                                    `
                                            <div class="div-hinh-anh-da-xem" id="idDivHinhAnhDaXem${nguoiDung.id_nguoi_dung}">
                                                <img src="${nguoiDung.hinh_anh}" class="img-hinh-anh-da-xem" />
                                            </div>
                                        `
                            }
                            noiDung += `</div>`
                        }
                    }

                    clas = "trai"
                    if (tinNhan.kiem_tra) {
                        clas = "phai"
                    }

                    noiDung +=
                        `
                            <div class="div-tin-nhan-${clas}">
                                <div class="div-block-${clas}">
                                    <div class="div-noi-dung-${clas}">
                                        ${layDuLieu(tinNhan.noi_dung)}
                                    </div>
                                    <div class="div-thoi-gian-tin-nhan">
                                        ${tinNhan.thoi_gian}
                                    </div> 
                                </div>
                            </div>
                        `
                }
                if (noiDung != ``) {
                    divDsTinNhan.innerHTML = noiDung + divDsTinNhan.innerHTML
                }
            })
        }
    })
}

const layDuLieu = (tinNhan) => {
    tinNhan2 = ""
    if (tinNhan.includes("https://")) {
        tinNhan = `<a href="${tinNhan}">${tinNhan}</a>`
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

            if (!nhomChat.da_xem) {
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

const taoNhom = (id_nguoi_dung) => {
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

        var divThongTinNhomTinNhanChon = document.getElementById("idDivThongTinNhomTinNhanChon")
        divThongTinNhomTinNhanChon.innerHTML =
            `
            <div class="div-avatar-nhom-tin-nhan-chon">
                <img class="img-avatar-nhom-tin-nhan-chon" src="${data.nhom.hinh_anh}" />
            </div>
            <h1 class="div-ten-nhom-tin-nhan-chon">${data.nhom.ten_nguoi_dung}</h1>
            `

        inputThanhTimKiem.value = ""

        loadTinNhan(data)

    })

}

const xemMenu = () => {
    var divNhomTinNhanChon = document.getElementById("idDivNhomTinNhanChon")
    var divDsBan = document.getElementById("idDivDsBan")
    divNhomTinNhanChon.classList.add("d-none")
    divDsBan.classList.remove("d-none")
}

const loadTinNhan = (data) => {
    if (window.innerWidth < 768) {
        var divNhomTinNhanChon = document.getElementById("idDivNhomTinNhanChon")
        var divDsBan = document.getElementById("idDivDsBan")
        divNhomTinNhanChon.classList.remove("d-none")
        divDsBan.classList.add("d-none")
    }

    soLuongTin = 0

    var divDsTinNhan = document.getElementById("idDivDsTinNhan")
    divDsTinNhan.innerHTML = ``

    for (tinNhan of data.ds_tin_nhan) {

        if (data.ds_thong_tin) {
            dsNguoiDung = data.ds_thong_tin[tinNhan.id_tin_nhan]
            if (dsNguoiDung) {
                noiDung = `<div class="div-ds-hinh-anh-da-xem">`
                for (nguoiDung of dsNguoiDung) {
                    noiDung +=
                        `
                            <div class="div-hinh-anh-da-xem" id="idDivHinhAnhDaXem${nguoiDung.id_nguoi_dung}">
                                <img src="${nguoiDung.hinh_anh}" class="img-hinh-anh-da-xem" />
                            </div>
                        `
                }
                noiDung += `</div>`
                divDsTinNhan.innerHTML += noiDung
            }
        }

        clas = "trai"
        if (tinNhan.kiem_tra) {
            clas = "phai"
        }

        divDsTinNhan.innerHTML +=
            `
                <div class="div-tin-nhan-${clas}">
                    <div class="div-block-${clas}">
                        <div class="div-noi-dung-${clas}">
                            ${layDuLieu(tinNhan.noi_dung)}
                        </div>
                        <div class="div-thoi-gian-tin-nhan">
                            ${tinNhan.thoi_gian}
                        </div> 
                    </div>
                </div>
            `
    }

    if (data.ds_nguoi_dung) {
        noiDung = `<div class="div-ds-hinh-anh-da-xem">`
        for (nguoiDung of data.ds_nguoi_dung) {
            noiDung +=
                `
                    <div class="div-hinh-anh-da-xem" id="idDivHinhAnhDaXem${nguoiDung.id_nguoi_dung}">
                        <img src="${nguoiDung.hinh_anh}" class="img-hinh-anh-da-xem" />
                    </div>
                `
        }
        noiDung += `</div>`
        divDsTinNhan.innerHTML += noiDung
    }

    var divNhapLieuNutGui = document.querySelector(`#idDivNhomTinNhan${idNhomHienThi} .div-thong-tin-nhom-tin-nhan`)
    divNhapLieuNutGui.classList.remove("div-thong-tin-nhom-tin-nhan-2")
    divDsTinNhan.innerHTML += `<div class="div-ds-hinh-anh-da-xem"></div>`

    divDsTinNhan.scrollTop = divDsTinNhan.scrollHeight



}
const chonNhom = (idNhom, tenNguoiDung, hinhAnh) => {
    idNhomHienThi = idNhom
    soLuongTin = 0

    var divNhapLieuNutGui = document.getElementById("idDivNhapLieuNutGui")
    divNhapLieuNutGui.classList.remove("div-nhap-lieu-nut-gui-2")

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
        loadTinNhan(data)
    })
}

const gui = () => {
    var inputNhapLieu = document.getElementById("idInputNhapLieu")
    if (inputNhapLieu.value.trim() != "") {
        soLuongTin++
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
            var divDsHinhAnhDaXemCuoiCung = document.getElementsByClassName("div-ds-hinh-anh-da-xem")[document.getElementsByClassName("div-ds-hinh-anh-da-xem").length - 1]

            if (divDsHinhAnhDaXemCuoiCung.innerHTML.trim() == ``) {
                divDsTinNhan.removeChild(divDsHinhAnhDaXemCuoiCung)
            }

            divDsTinNhan.innerHTML +=
                `
                    <div class="div-tin-nhan-phai" >
                        <div class="div-block-phai">
                            <div class="div-noi-dung-phai">
                                ${layDuLieu(data.noi_dung)}
                            </div>
                            <div class="div-thoi-gian-tin-nhan">
                                ${layDuLieu(data.thoi_gian)}
                            </div>
                        </div>
                    </div>
                    <div class="div-ds-hinh-anh-da-xem"></div>
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
        }).then(res => res.json()).then(data => {

            var divDsNhom = document.getElementById("idDivDsNhomChat")
            var dsNhom2 = ``
            var divDsTinNhan = document.getElementById("idDivDsTinNhan")

            for (nhom of data.ds_nhom) {

                divNhom = document.getElementById(`idDivNhomTinNhan${nhom.id_nhom}`)
                divDsNhom.removeChild(divNhom)

                if (nhom.id_nhom != idNhomHienThi) {
                    dsNhom2 +=
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
                }
            }
            for (noiDung of data.ds_noi_dung) {
                divDsTinNhan.innerHTML +=
                    `
                    <div class="div-tin-nhan-trai">
                        <div class="div-block-trai">
                            <div class="div-noi-dung-trai">
                                ${layDuLieu(noiDung.noi_dung)}
                            </div>
                            <div class="div-thoi-gian-tin-nhan">
                                ${noiDung.thoi_gian}
                            </div>
                        </div>
                    </div>
                    <div class="div-ds-hinh-anh-da-xem"></div>
                `
                divDsTinNhan.scrollTop = divDsTinNhan.scrollHeight
            }

            if (dsNhom2 != ``) {
                divDsNhom.innerHTML = dsNhom2 + divDsNhom.innerHTML
            }

            for (nguoiDung of data.ds_nguoi_xem) {
                dsDivDsHinhAnhDaXem = document.getElementsByClassName("div-ds-hinh-anh-da-xem")
                divDsHinhAnhDaXemCuoiCung = dsDivDsHinhAnhDaXem[dsDivDsHinhAnhDaXem.length - 1]

                divHinhAnhDaXem = document.getElementById(`idDivHinhAnhDaXem${nguoiDung.id_nguoi_dung}`)

                if (!(divHinhAnhDaXem.parentElement == divDsHinhAnhDaXemCuoiCung)) {
                    noiDung = divHinhAnhDaXem.innerHTML

                    divDsHinhAnhDaXemCuoiCung.innerHTML += `
                        <div class="div-hinh-anh-da-xem" id=idDivHinhAnhDaXem${nguoiDung.id_nguoi_dung}>
                            ${noiDung}
                        </div>
                    `

                    divCha = divHinhAnhDaXem.parentElement
                    divCha.removeChild(divHinhAnhDaXem)
                    if (divCha.innerHTML.trim() == ``) {
                        divDsTinNhan.removeChild(divCha)
                    }
                }
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
    loadSuKienCuon()
}