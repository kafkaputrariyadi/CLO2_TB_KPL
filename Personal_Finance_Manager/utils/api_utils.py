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

def get_investment_options():
    """
    Mendapatkan daftar opsi investasi dari API eksternal
    
    Returns:
        list: Daftar opsi investasi dengan perkiraan return
        
    Contoh Response API:
    [
        {
            "name": "Deposito",
            "return": 5.0
        },
        {
            "name": "Reksadana Saham",
            "return": 10.0
        }
    ]
    """
    try:
        return [
            {"name": "Deposito", "return": 5.0},
            {"name": "Reksadana Pendapatan Tetap", "return": 7.0},
            {"name": "Reksadana Saham", "return": 10.0},
            {"name": "Saham Blue Chip", "return": 12.0}
        ]
    except:
        return []