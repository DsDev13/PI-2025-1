import os
import requests

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_SERVICE_ROLE = os.environ.get('SUPABASE_SERVICE_ROLE')


def upload_file_to_supabase(bucket_name: str, file_obj, path: str):
    """
    Faz upload do arquivo para o Supabase Storage via HTTP PUT e retorna a URL pública.

    Args:
        bucket_name: nome do bucket (ex: 'media')
        file_obj: objeto file (InMemoryUploadedFile)
        path: caminho no bucket, ex: 'anuncios/usuario123-nome.jpg'

    Retorna:
        URL pública do arquivo no formato: {SUPABASE_URL}/storage/v1/object/public/{bucket}/{path}

    Lança RuntimeError em caso de falha com detalhes do retorno HTTP para facilitar debug nos logs do Render.
    """
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE:
        raise RuntimeError('Supabase not configured: set SUPABASE_URL and SUPABASE_SERVICE_ROLE in environment')

    # garante que file pointer está no começo
    try:
        file_obj.seek(0)
    except Exception:
        pass

    upload_url = f"{SUPABASE_URL.rstrip('/')}/storage/v1/object/{bucket_name}/{path}"
    headers = {
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE}',
        'x-upsert': 'true'
    }
    # tenta inferir content-type quando disponível
    content_type = getattr(file_obj, 'content_type', None)
    if content_type:
        headers['Content-Type'] = content_type
    else:
        headers['Content-Type'] = 'application/octet-stream'

    data = file_obj.read()
    resp = requests.put(upload_url, headers=headers, data=data)
    if not resp.ok:
        # lança erro com detalhe para aparecer nos logs do Render
        raise RuntimeError(f"Supabase upload failed: {resp.status_code} {resp.text}")

    # URL pública do objeto
    public_url = f"{SUPABASE_URL.rstrip('/')}/storage/v1/object/public/{bucket_name}/{path}"
    return public_url
