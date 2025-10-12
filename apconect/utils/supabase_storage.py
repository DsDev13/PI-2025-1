import os
from supabase import create_client

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_SERVICE_ROLE = os.environ.get('SUPABASE_SERVICE_ROLE')

if SUPABASE_URL and SUPABASE_SERVICE_ROLE:
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)
else:
    supabase = None


def upload_file_to_supabase(bucket_name: str, file_obj, path: str):
    """
    Envia o arquivo para o bucket do Supabase e retorna a URL pública.
    file_obj: objeto file (InMemoryUploadedFile)
    path: caminho no bucket, ex: 'anuncios/usuario123-nome.jpg'
    """
    if not supabase:
        raise RuntimeError('Supabase client not configured. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE in env vars')

    # garante que file pointer está no começo
    try:
        file_obj.seek(0)
    except Exception:
        pass

    data = file_obj.read()
    # upload
    result = supabase.storage.from_(bucket_name).upload(path, data)
    # obter url pública
    public_url = supabase.storage.from_(bucket_name).get_public_url(path)
    # dependendo da versão do client, get_public_url pode retornar dict ou str
    if isinstance(public_url, dict):
        return public_url.get('publicURL')
    return public_url
