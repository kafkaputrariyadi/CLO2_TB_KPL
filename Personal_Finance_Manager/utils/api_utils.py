import requests

def get_interest_rate():
    """
    Mendapatkan suku bunga terkini dari API eksternal
    
    Returns:
        float: Suku bunga dalam persen (default 3.5 jika API gagal)
    
    Contoh Response API:
    {
        "rate": 3.5
    }
    """
    try:
        response = requests.get('https://api.example.com/v1/interest-rate', timeout=3)
        if response.status_code == 200:
            return float(response.json().get('rate', 3.5))
    except:
        pass
    return 3.5
