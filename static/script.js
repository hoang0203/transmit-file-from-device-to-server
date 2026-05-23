// Dùng DataTransfer để lưu trữ và quản lý danh sách file có thể thêm/xóa
let dataTransfer = new DataTransfer();

// Kích hoạt thẻ input ẩn
function triggerFileInput() {
    document.getElementById('fileInput').click();
}

// Bắt sự kiện khi người dùng chọn file
document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.getElementById('fileInput');

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            // Khi chọn file mới, ta thay thế danh sách cũ bằng danh sách mới
            dataTransfer = new DataTransfer(); 
            for (let i = 0; i < fileInput.files.length; i++) {
                dataTransfer.items.add(fileInput.files[i]);
            }
            updateFileListUI();
        });
    }
});

// Hàm Xóa 1 file khỏi danh sách dựa trên vị trí (index)
function removeFile(index) {
    const fileInput = document.getElementById('fileInput');
    const newDataTransfer = new DataTransfer();
    
    // Copy tất cả file sang danh sách mới, NGOẠI TRỪ file bị xóa
    for (let i = 0; i < dataTransfer.files.length; i++) {
        if (i !== index) {
            newDataTransfer.items.add(dataTransfer.files[i]);
        }
    }
    
    dataTransfer = newDataTransfer; // Cập nhật lại biến toàn cục
    fileInput.files = dataTransfer.files; // Gắn lại vào thẻ input thật
    updateFileListUI(); // Vẽ lại giao diện
}

// Hàm vẽ danh sách file ra HTML và quản lý nút Tải Lên
function updateFileListUI() {
    const listContainer = document.getElementById('fileListContainer');
    const uploadBtn = document.getElementById('uploadBtn');
    const fileInput = document.getElementById('fileInput');
    const files = dataTransfer.files;
    
    // Lấy danh sách đuôi file hợp lệ từ thuộc tính accept của input
    const allowedExtensions = fileInput.getAttribute('accept').split(',').map(ext => ext.trim().toLowerCase());
    
    listContainer.innerHTML = ''; 

    if (files.length === 0) {
        listContainer.innerHTML = '<div class="text-muted small text-center mt-4">Chưa có file nào</div>';
        uploadBtn.disabled = true;
        return;
    }

    let hasInvalidFile = false; // Cờ kiểm tra xem có file nào lỗi không

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const fileName = file.name;
        const fileExt = "." + fileName.split('.').pop().toLowerCase();
        
        // Kiểm tra tính hợp lệ
        const isValid = allowedExtensions.includes(fileExt);
        if (!isValid) hasInvalidFile = true;

        const itemDiv = document.createElement('div');
        itemDiv.className = 'file-item';
        
        // Icon báo hiệu: 🟢 hợp lệ, 🔴 không hợp lệ
        const statusIcon = isValid ? "✅" : "⚠️";

        itemDiv.innerHTML = `
            <span>${statusIcon} ${fileName.length > 20 ? fileName.substring(0, 15) + "..." : fileName}</span>
            <button type="button" class="remove-btn" onclick="removeFile(${i})">&times;</button>
        `;
        listContainer.appendChild(itemDiv);
    }

    // Nếu có file không hợp lệ, khóa nút Tải Lên
    uploadBtn.disabled = hasInvalidFile;
    
    if (hasInvalidFile) {
        // Có thể thêm cảnh báo nhỏ cho người dùng
        listContainer.insertAdjacentHTML('afterbegin', 
            '<div class="text-danger small text-center p-1">⚠️ Có file không được hỗ trợ!</div>');
    }
}

// --- HÀM TẢI LÊN GIỮ NGUYÊN HOÀN TOÀN CỦA BẠN ---
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

    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
    }

    uploadSection.classList.add('d-none');
    progressContainer.classList.remove('d-none');
    statusMessage.innerHTML = "Đang tải lên...";

    const xhr = new XMLHttpRequest();
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

// --- RESET LẠI GIAO DIỆN CHUẨN XÁC ---
function resetForm() {
    document.getElementById('fileInput').value = "";
    dataTransfer = new DataTransfer(); // Reset biến quản lý file
    updateFileListUI(); // Reset UI danh sách

    document.getElementById('uploadSection').classList.remove('d-none');
    
    document.getElementById('progressContainer').classList.add('d-none');
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = "0%";
    progressBar.innerText = "0%";
    progressBar.classList.remove('bg-success');
    
    document.getElementById('statusMessage').innerHTML = "";
    document.getElementById('resetBtn').classList.add('d-none');
}