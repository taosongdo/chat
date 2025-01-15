const loadBatSuKienDoiHinh = () => {
    const inputHinhAnh = document.getElementById('idInputHinhAnh');
    const imgHinhAnh = document.getElementById('idImgHinhAnh');
    inputHinhAnh.addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file) {
            imgHinhAnh.src = URL.createObjectURL(file);
        }
    });
}

window.onload = () => {
    loadBatSuKienDoiHinh()
}

