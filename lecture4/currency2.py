import requests

def main():
    base = input("First Currency: ")
    other = input("Second Currency: ")
    res = requests.get("https://api.fixer.io/latest",
                       params={"base": base, "symbols": other})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    rate = data["rates"][other]
    print(f"1 {base} is equal to {rate} {other}")

if __name__ == "__main__":
    main()
