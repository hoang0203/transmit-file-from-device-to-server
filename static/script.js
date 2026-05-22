function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;
    const uploadSection = document.getElementById('uploadSection');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    const statusMessage = document.getElementById('statusMessage');
    const resetBtn = document.getElementById('resetBtn');

    if (files.length === 0) {
        statusMessage.innerHTML = "<span class='text-danger'>Vui lòng chọn ít nhất một file!</span>";
        return;
    }

    // 1. LẤY TOKEN TỪ URL HIỆN TẠI
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');

    // Chuẩn bị form data
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
    }

    uploadSection.classList.add('d-none');
    progressContainer.classList.remove('d-none');
    statusMessage.innerHTML = "Đang tải lên...";

    const xhr = new XMLHttpRequest();
    
    // 2. GẮN TOKEN VÀO URL KHI GỬI REQUEST
    // Thay vì open("POST", "/upload", true), hãy dùng:
    xhr.open("POST", "/upload?token=" + encodeURIComponent(token), true);

    xhr.upload.onprogress = function(event) {
        if (event.lengthComputable) {
            let percentComplete = Math.round((event.loaded / event.total) * 100);
            progressBar.style.width = percentComplete + "%";
            progressBar.innerText = percentComplete + "%";
        }
    };

    xhr.onload = function() {
        if (xhr.status === 200) {
            progressBar.classList.add('bg-success');
            statusMessage.innerHTML = `<span class='text-success'>Đã tải lên ${files.length} file thành công!</span>`;
            resetBtn.classList.remove('d-none');
        } else if (xhr.status === 403) {
            statusMessage.innerHTML = "<span class='text-danger'>Lỗi: Token không hợp lệ. Vui lòng tải lại trang!</span>";
            uploadSection.classList.remove('d-none');
        } else {
            statusMessage.innerHTML = "<span class='text-danger'>Có lỗi xảy ra khi tải file.</span>";
            uploadSection.classList.remove('d-none');
        }
    };

    xhr.send(formData);
}

// Hàm reset lại giao diện như lúc mới mở web
function resetForm() {
    // Xóa file cũ trong thẻ input
    document.getElementById('fileInput').value = "";
    
    // Hiện lại khu vực chọn file và tải lên
    document.getElementById('uploadSection').classList.remove('d-none');
    
    // Ẩn và reset thanh tiến trình
    document.getElementById('progressContainer').classList.add('d-none');
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = "0%";
    progressBar.innerText = "0%";
    progressBar.classList.remove('bg-success');
    
    // Xóa tin nhắn trạng thái và ẩn chính nút "Tải Thêm"
    document.getElementById('statusMessage').innerHTML = "";
    document.getElementById('resetBtn').classList.add('d-none');
}