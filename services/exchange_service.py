import requests

def get_usd_brl_rate():
    """
    Consulta cotação USD -> BRL usando API pública.
    """
    try:
        response = requests.get(
            "https://economia.awesomeapi.com.br/json/last/USD-BRL",
            timeout=5
        )
        data = response.json()
        rate = float(data["USDBRL"]["bid"])
        return rate
    except Exception:
        raise RuntimeError("Erro ao consultar API de câmbio.")