import os

def extract_filename(file_path: str) -> str:
    """
    Extrae el nombre base del archivo sin la extensión.

    Args:
        file_path (str): La ruta del archivo, por ejemplo, 'track3.wav'.

    Returns:
        str: El nombre base del archivo, por ejemplo, 'track3'.
    """
    # Obtener el nombre del archivo sin la ruta
    base_name = os.path.basename(file_path)

    # Dividir el nombre del archivo en nombre y extensión
    name, _ = os.path.splitext(base_name)

    return name
