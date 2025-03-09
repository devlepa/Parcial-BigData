import io
import os
from unittest.mock import MagicMock
from descargar import archivos_s3_descargados


def test_archivos_s3_descargados_success(tmp_path):
    # Simula un s3 que devuelve dos archivos
    fake_s3 = MagicMock()
    fake_s3.list_objects_v2.return_value = {
        "Contents": [
            {"Key": "file1.html"},
            {"Key": "file2.html"}
        ]
    }

    # HTML de ejemplo que devolverá get_object
    fake_html = "<html><body>Content</body></html>"
    # Cada llamada a get_object retorna un nuevo objeto BytesIO
    fake_s3.get_object.side_effect = lambda Bucket, Key: {"Body": io.BytesIO(fake_html.encode("utf-8"))}

    # Cambiamos el directorio de trabajo a uno temporal para capturar los archivos escritos
    old_dir = os.getcwd()
    os.chdir(tmp_path)
    try:
        # Creamos la carpeta "html" ya que la función escribe en "./html/index<i>.html"
        html_dir = tmp_path / "html"
        html_dir.mkdir(exist_ok=True)

        result = archivos_s3_descargados(fake_s3, "fake_bucket")
        assert result["status"] == "success"
        assert result["archivos_almacenados y guardados en local"] == ["file1.html", "file2.html"]

        # Verifica que se hayan creado los archivos en la carpeta "html"
        file1 = tmp_path / "html" / "index1.html"
        file2 = tmp_path / "html" / "index2.html"
        assert file1.exists(), "File index1.html was not created."
        assert file2.exists(), "File index2.html was not created."

        # Comprueba que el contenido de los archivos es el HTML de ejemplo
        with open(file1, "r") as f:
            content1 = f.read()
        with open(file2, "r") as f:
            content2 = f.read()
        assert content1 == fake_html
        assert content2 == fake_html
    finally:
        os.chdir(old_dir)
