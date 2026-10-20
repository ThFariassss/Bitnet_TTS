"""Piper residente (--json-input), compartilhado por voice.py e servidor_conversa.py.

Compatibilidade: Python 3.6 da Jetson."""
import json
import os
import subprocess
import tempfile
import threading

from pronuncia import para_fala


class Piper:
    """Piper residente (--json-input): o modelo carrega uma vez e cada frase
    vira um WAV, sem pagar o custo de iniciar o processo a cada fala."""

    def __init__(self, pasta=None, voz=None):
        pasta = pasta or os.environ.get("LSA_PIPER_DIR") or os.path.expanduser("~/piper")
        voz = voz or os.environ.get("LSA_PIPER_VOICE") or os.path.join(pasta, "voices", "pt_BR-faber-medium.onnx")
        for caminho in (os.path.join(pasta, "piper"), voz):
            if not os.path.exists(caminho):
                raise FileNotFoundError("Piper: nao encontrei %s" % caminho)
        self._saida = tempfile.mkdtemp(prefix="lsa-piper-")
        self._lock = threading.Lock()
        self._cache = {}      # texto -> WAV (frases fixas repetem; evita ~2s de sintese)
        self._proc = subprocess.Popen(
            [os.path.join(pasta, "piper"), "-m", voz, "--json-input", "--output_dir", self._saida],
            cwd=pasta, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            universal_newlines=True, bufsize=1)

    def sintetizar(self, texto):
        """Devolve os bytes do WAV falado."""
        if texto in self._cache:
            return self._cache[texto]
        with self._lock:
            if texto in self._cache:          # outra thread acabou de gerar
                return self._cache[texto]
            self._proc.stdin.write(json.dumps({"text": para_fala(texto)}, ensure_ascii=False) + "\n")
            self._proc.stdin.flush()
            caminho = self._proc.stdout.readline().strip()
        if not caminho or not os.path.exists(caminho):
            raise RuntimeError("Piper nao gerou audio para %r" % texto)
        try:
            with open(caminho, "rb") as f:
                wav = f.read()
        finally:
            os.remove(caminho)
        if len(texto) <= 200 and len(self._cache) < 400:
            self._cache[texto] = wav
        return wav
