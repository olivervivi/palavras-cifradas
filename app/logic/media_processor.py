import subprocess
import os
import tempfile
import shutil  # Verifica se o FFmpeg está disponível

def converter_audio(audio_bytes, formato_saida="wav"):
    """
    Converte um fluxo de bytes de áudio para um formato de saída especificado usando FFmpeg.
    Retorna uma tupla: (resultado_em_bytes, erro_ocorrido).
    """
    # Verifica se o FFmpeg está disponível no sistema
    if not shutil.which("ffmpeg"):
        return None, "Erro Crítico: O FFmpeg não foi encontrado no sistema. Verifique a instalação e o PATH."

    # Cria arquivos temporários em diretório seguro
    temp_dir = tempfile.gettempdir()
    pid = os.getpid()
    input_path = os.path.join(temp_dir, f"temp_input_{pid}.tmp")
    output_path = os.path.join(temp_dir, f"temp_output_{pid}.{formato_saida}")

    try:
        # Grava o áudio original no arquivo de entrada temporário
        with open(input_path, "wb") as f:
            f.write(audio_bytes)

        # Confirma que o arquivo foi criado
        if not os.path.exists(input_path):
            return None, "Erro: O arquivo temporário de entrada não foi criado corretamente."

        # Comando FFmpeg
        command = ["ffmpeg", "-y", "-i", input_path, "-vn", output_path]
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        # Lê o arquivo convertido (output)
        with open(output_path, "rb") as f:
            resultado_bytes = f.read()

        return resultado_bytes, None  # Sucesso

    except subprocess.CalledProcessError as e:
        return None, f"O FFmpeg falhou ao processar o arquivo. Detalhes:\n{e.stderr}"

    except Exception as e:
        return None, f"Ocorreu um erro inesperado ao processar o áudio: {str(e)}"

    finally:
        # Limpa os arquivos temporários
        for path in [input_path, output_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass  # Não interrompe o fluxo se não conseguir remover
