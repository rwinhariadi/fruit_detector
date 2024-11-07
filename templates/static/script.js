// Fungsi untuk menampilkan pratinjau gambar dan langsung mengirim form setelah gambar dipilih
function previewAndSubmit(event) {
  const fileInput = event.target;
  const reader = new FileReader();
  const iconContainer = document.getElementById('icon-container');
  const uploadedImage = document.getElementById('uploaded-image');

  // Tampilkan pratinjau gambar dan ganti ikon cloud
  if (fileInput.files && fileInput.files[0]) {
    reader.onload = function () {
      uploadedImage.src = reader.result;
      uploadedImage.style.display = 'block';
      iconContainer.style.display = 'none'; // Sembunyikan ikon setelah upload
    };
    reader.readAsDataURL(fileInput.files[0]);

    // Membuat FormData dan menambahkan file yang diunggah
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // Mengirim data unggahan ke server dan menampilkan hasil
    fetch('/upload', {
      method: 'POST',
      body: formData,
    })
      .then((response) => response.json())
      .then((result) => {
        if (result.error) {
          throw new Error(result.error);
        }

        // Tampilkan hasil prediksi dan confidence
        document.getElementById('result').innerText = result.prediction;
        document.getElementById('confidence').innerText = `${result.accuracy}%`;
      })
      .catch((error) => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'Gagal memproses gambar';
        document.getElementById('confidence').innerText = '-'; // Reset confidence jika gagal
      });
  } else {
    console.error('No file selected');
  }
}

// Menambahkan event listener untuk file input
document.getElementById('file-input').addEventListener('change', previewAndSubmit);
