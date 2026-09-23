import json, csv, os

def load_prices(fname):
    tickets = []
    if fname.endswith('.json'):
        with open(fname) as f:
            data = json.load(f)
        for disc, types in data.items():
            for typ, items in types.items():
                for name, price in items.items():
                    tickets.append((disc, typ, name, float(price)))
    else:  # CSV
        with open(fname, 'r', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f, delimiter=';'):
                price = float(row['price'].replace(',', '.'))
                tickets.append((row['discount'], row['duration'], row['name'], price))
    return tickets

cart = []                     # lista (ticket, ilość)
tickets = load_prices('prices.json' if os.path.exists('prices.json') else 'prices.csv')

def show_cart():
    if not cart:
        print("Koszyk pusty")
        return 0.0
    total = 0.0
    print("\nKOSZYK:")
    for (disc, typ, name, price), qty in cart:
        s = price * qty
        total += s
        print(f"{name} ({disc}, {typ}) x{qty} = {s:.2f}")
    print(f"Razem: {total:.2f}")
    return total

def add_ticket():
    disc = input("[N]ormalny / [U]lgowy: ").lower()
    if disc not in ('n', 'u'): return print("Zły wybór")
    disc = 'normalny' if disc == 'n' else 'ulgowy'
    
    typ = input("[O]kresowy / [C]zasowy / [J]ednorazowy: ").lower()
    typ_map = {'o':'okresowy', 'c':'czasowy', 'j':'jednorazowy'}
    if typ not in typ_map: return print("Zły wybór")
    typ = typ_map[typ]
    
    available = [t for t in tickets if t[0]==disc and t[1]==typ]
    if not available:
        print("Brak biletów")
        return
    
    keys = [chr(ord('a')+i) for i in range(26)] + [str(i) for i in range(10)]
    print("Dostępne:")
    for i, (_, _, name, price) in enumerate(available):
        print(f"[{keys[i].upper()}] {name} - {price:.2f}")
    ch = input("Wybierz: ").lower()
    try:
        idx = keys.index(ch)
    except ValueError:
        return print("Zły wybór")
    ticket = available[idx]
    
    qty = input("Ilość (1-9): ").strip()
    if not qty.isdigit() or not (1 <= int(qty) <= 9):
        return print("Nieprawidłowa ilość")
    cart.append((ticket, int(qty)))
    print(f"Dodano {qty} x {ticket[2]}")

def checkout():
    total = show_cart()
    if total == 0:
        return
    while True:
        try:
            paid = float(input("Wpłata (zł): ").replace(',', '.'))
            if paid < total:
                print(f"Brakuje {total-paid:.2f}")
                continue
            print(f"Reszta: {paid-total:.2f}")
            print("Wydano bilety:")
            for (disc, typ, name, price), qty in cart:
                print(f"- {qty} x {name}")
            cart.clear()
            break
        except:
            print("Błędna kwota")

print("=== AUTOMAT BILETOWY ===")
while True:
    cmd = input("\n[D]odaj  [K]asa  [W]yjście: ").lower()
    if cmd == 'd':
        add_ticket()
    elif cmd == 'k':
        checkout()
    elif cmd == 'w':
        break
    else:
        print("Nieznane polecenie")
print("Do widzenia")