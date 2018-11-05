import requests

def main():
    res = requests.get("https://api.fixer.io/latest?base=USD&symbols=EUR")
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    rate = data["rates"]["EUR"]
    print(f"1 USD is equal to {rate} EUR")

if __name__ == "__main__":
    main()
