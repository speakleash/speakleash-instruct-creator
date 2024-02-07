import os 
import random
import json

try:
    from utils.functions import get_dir_path
except ImportError as e:
    print(f'Error: {e}')
    def get_dir_path(directory):
        return None

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = get_dir_path("data") or os.path.join(base_dir, "data")
output_dir = get_dir_path("output") or os.path.join(base_dir, "output")

source_name = "simple_math_operations"
source_url = "https://speakleash.org/"
source_description = "Instrukcje dla prostych operacji matematycznych wygenerowane automatycznie"
script_name = os.path.basename(__file__)

OBJECTS = [
    "jabłek",
    "gruszek",
    "owoców",
    "marchewek",
    "pomidorów",
    "ogórków",
    "złotych",
    "groszy",
    "banknotów",
    "litrów wody",
    "kropli olejku eterycznego",
    "klocków",
    "samochodów",
    "kubków",
    "talerzy",
    "par butów",
    "bluzek",
    "spodni",
    "kocy",
    "poduszek"
]
NAMES = [
    "Maria",
    "Iza",
    "Sebastian",
    "Krzysiek",
    "Adrian",
    "Grzesiek",
    "Szymek",
    "Paweł",
    "Igor",
    "Waldek"
]
instructions = []

for i in range(-10, 20):
    for j in range(-10, 20):
        instr = random.choice([
            f"Dodaj liczbę {i} do liczby {j}.",
            f"Weź liczbę {i} i zwiększ ją o liczbę {j}.",
            f"Liczbę {i} powiększ o {j}.",
            f"Oblicz sumę liczb {i} i {j}.",
            f"Zsumuj liczby {i} i {j}.",
            f"Liczba {i} plus liczba {j} jaki daje wynik?",
            f"Oblicz ile to będzie {i} dodać {j}.",
            f"Podaj rezultat dodawania {i} oraz {j}.",
            f"Jaka będzie sumaryczna wartość liczb {i} i {j}?",
            f"Wykonaj operację dodawania liczb {i} oraz {j}.",
            f"Oblicz: {i} + {j}",
            f"Policz ile otrzymamy dodając {i} do {j}.",
            f"Wykonaj działanie: {i} + {j}",
            f"Znajdź sumę {i} i {j}.",
            f"Wykonaj dodawanie: {i} + {j}",
            f"Jaką liczbę otrzymasz dodając {i} do {j}?",
            f"Ile to jest {i} + {j}?",
            f"Jaki będzie wynik, gdy do {i} dodamy {j}?",
            f"Połącz wartości {i} i {j}, aby uzyskać ich sumę.",
            f"Policz: {i} + {j}",
            f"Jaki jest wynik dodawania {i} + {j}?",
            f"Dodaj {i} do {j}. Jaki wynik otrzymałeś?",
            f"Jaką jest suma liczb {i} i {j}?",
            f"Ile to będzie {i} + {j}?",
            f"Jaka liczbę otrzymamy po dodaniu do siebie {i} i {j}?",
            f"Wykonaj proste zadanie matematyczne polegające na dodaniu do siebie dwóch liczb: {i} i {j}. Jaki wynik otrzymałeś?",
            f"Napisz ile to jest {i} + {j}.",
            f"Jeśli dodam {i} do {j}, to jaki wynik otrzymam?",
            f"Dodałam {i} do {j}. Jaki wynik otrzymałam?"
        ])
        r = i + j
        output = random.choice([
            f"Wynik to: {r}.",
            f"Wynikiem tego dodawania jest {r}.",
            f"{r}",
            f"Wynikiem jest {r}.",
            f"Odpowiedź: {r}.",
            f"Odpowiedź to {r}.",
            f"Prawidłowa odpowiedź to {r}.",
            f"{i} + {j} = {r}",
            f"Jeśli dodamy {i} do {j} to otrzymamy {r}.",
            f"{i} plus {j} jest równe {r}",
            f"{i} plus {j} to {r}"
        ])
        instructions.append({"instruct": instr, "input": "", "output": output, "source_name" : source_name, "source_url" : source_url, "source_description" : source_description, "script_name" : script_name})


for i in range(5, 20):
    for j in range(i+1, 40-i):
        obj = random.choice(OBJECTS)
        name1, name2 = random.sample(NAMES, 2)
        instr = random.choice([
            f"Miałem {i} {obj}, po czym kolega dał mi jeszcze {j}. Ile teraz mam {obj}?",
            f"Wczoraj dostałem od rodziców {i} {obj}. Dziś przyjechali do mnie dziadkowie i dali mi jeszcze {i} {obj}. Policz ile mam teraz {obj}."
            f"Do {i} {obj} dodaj jeszcze {j}. Jaka jest suma?",
            f"{name1} ma {i} {obj}, a {name2} {j} {obj}. Ile razem mają {obj}?",
            f"Jeśli {name1} ma {i} {obj} i {name2} ma {j} {obj}, to ile razem mają?",
            f"Niech {name1} dostanie {i} {obj}, a {name2} dostanie {j} {obj}. Ile łącznie będą mieli wtedy {obj}?",
            f"{name1} i {name2} mają odpowiednio {i} i {j} {obj}. Ile razem mają {obj}?",
            f"Załóżmy, że {name1} ma {i} {obj}, a {name2} ma {j} {obj}. Ile łącznie mają {obj}?",
            f"Gdy {name1} ma {i} {obj}, a {name2} ma {j} {obj}, to razem mają ile {obj}?",
            f"Przedwczoraj miałem 0 {obj}. Wczoraj dostałem {i} {obj}, a dzisiaj dostałem jeszcze {j}. Ile teraz mam {obj}?",
            f"{name1} ma {i} {obj}. Obok stoi {name2} i ma {j} {obj}. Policz ile razem mają {obj}."
        ])
        r = i + j
        output = random.choice([
            f"Wynik to {r}.",
            f"Wynikiem tego dodawania jest {r}.",
            f"{r} {obj}",
            f"Wynikiem jest {r}",
            f"Odpowiedź: {r}.",
            f"Odpowiedź to {r} {obj}.",
            f"Prawidłowa odpowiedź to {r} {obj}.",
            f"{i} {obj} + {j} {obj} = {r} {obj}",
            f"Jeśli dodamy {i} {obj} i {j} {obj}, to otrzymamy {r} {obj}."
        ])
        instructions.append({"instruct": instr, "input": "", "output": output, "source_name" : source_name, "source_url" : source_url, "source_description" : source_description, "script_name" : script_name})


for i in range(-10, 10):
    for j in range(-10, 10):
        instr = random.choice([
            f"Pomnóż liczbę {i} przez liczbę {j}.",
            f"Przemnóż liczbę {i} przez {j}.",
            f"Liczbę {i} pomnóż przez {j}.",
            f"Oblicz iloczyn liczb {i} i {j}.",
            f"Pomnóż liczby {i} i {j}.",
            f"Liczba {i} razy liczba {j} jaki daje wynik?",
            f"Oblicz ile to będzie {i} razy {j}.",
            f"Podaj rezultat mnożenia {i} oraz {j}.",
            f"Jaki będzie iloczyn liczb {i} i {j}?",
            f"Wykonaj operację mnożenia liczb {i} oraz {j}.",
            f"Oblicz: {i} * {j} =",
            f"Policz ile otrzymamy mnożąc {i} z {j}.",
            f"Wykonaj działanie: {i} * {j} =",
            f"Znajdź iloczyn {i} i {j}.",
            f"Wykonaj działanie: {i} * {j} =",
            f"Jaką liczbę otrzymasz mnożąc {i} oraz {j}?",
            f"Ile to jest {i} * {j}?",
            f"Jaki będzie wynik, gdy {i} pomnożymy z {j}?",
            f"Ile wynosi iloczyn liczb {i} i {j}?",
            f"Policz: {i} * {j} =",
            f"Jaki jest wynik mnożenia {i} * {j}?",
            f"Mnożysz {i} * {j}. Jaki wynik otrzymałeś?",
            f"Jaki jest iloczyn liczb {i} i {j}?",
            f"Ile to będzie {i} * {j}?",
            f"Jaką liczbę otrzymamy po przemnożeniu {i} i {j}?",
            f"Wykonaj proste zadanie matematyczne polegające na pomnożeniu dwóch liczb: {i} i {j}. Jaki wynik otrzymałeś?",
            f"Napisz ile to jest {i} * {j}.",
            f"Jeśli pomnożyłam {i} i {j}, to jaki wynik otrzymałam?",
            f"Pomnożyłem {i} razy {j}. Jaki wynik otrzymałem?"
        ])
        r = i * j
        output = random.choice([
            f"Wynik to {r}.",
            f"Wynikiem tego mnożenia jest {r}.",
            f"Iloczyn tych liczb jest równy {r}.",
            f"{r}",
            f"Wynikiem jest {r}.",
            f"Odpowiedź: {r}.",
            f"Odpowiedź to {r}.",
            f"Prawidłowa odpowiedź to {r}.",
            f"{i} * {j} = {r}",
            f"Mnożąc {i} razy {j} otrzymamy {r}.",
            f"{i} razy {j} jest równe {r}",
            f"{i} razy {j} to {r}"
        ])
        instructions.append({"instruct": instr, "input": "", "output": output, "source_name" : source_name, "source_url" : source_url, "source_description" : source_description, "script_name" : script_name})


for i in range(-10, 20):
    for j in range(-10, 20):
        instr = random.choice([
            f"Odejmij liczbę {j} od liczby {i}.",
            f"Weź liczbę {i} i pomniejsz ją o liczbę {j}.",
            f"Liczbę {i} zmniejsz o {j}.",
            f"Oblicz różnicę liczb {i} i {j}.",
            f"Odejmij {j} od liczby {i}.",
            f"Liczba {i} minus liczba {j} jaki daje wynik?",
            f"Oblicz ile to będzie {i} minus {j}.",
            f"Podaj rezultat odejmowania {i} minus {j}.",
            f"Jaka będzie różnica liczb {i} i {j}?",
            f"Wykonaj operację odejmowania liczb {i} oraz {j}.",
            f"Oblicz: {i} - {j}",
            f"Policz ile otrzymamy odejmując {j} od {i}.",
            f"Wykonaj działanie: {i} - {j}",
            f"Znajdź różnicę {i} minus {j}.",
            f"Wykonaj działanie: {i} - {j}",
            f"Jaką liczbę otrzymasz w wyniku odejmowania {i} minus {j}?",
            f"Ile to jest {i} - {j}?",
            f"Jaki będzie wynik, gdy od {i} odejmiemy {j}?",
            f"Wykonaj działanie arytmetyczne {i} minus {j} i podaj wynik.",
            f"Policz: {i} - {j}",
            f"Jaki jest wynik odejmowania {i} - {j}?",
            f"Wykonaj odejmowanie {i} - {j}. Jaki wynik otrzymałeś?",
            f"Jaka jest różnica liczb {i} i {j}?",
            f"Ile to będzie {i} - {j}?",
            f"Jaką liczbę otrzymamy po odjęciu {j} od {i}?",
            f"Wykonaj proste zadanie matematyczne polegające na znalezieniu różnicy dwóch liczb: {i} i {j}. Jaki wynik otrzymałeś?",
            f"Napisz ile to jest {i} - {j}.",
            f"Jeśli odejmę {j} od {i}, to jaki wynik otrzymam?",
            f"Jaki wynik otrzymam dla działania {i} minus {j}?"
        ])
        r = i - j
        output = random.choice([
            f"Wynik to: {r}.",
            f"Wynikiem tego odejmowania jest {r}.",
            f"{r}",
            f"Wynikiem jest {r}.",
            f"Odpowiedź: {r}.",
            f"Odpowiedź to {r}.",
            f"Prawidłowa odpowiedź to {r}.",
            f"{i} - {j} = {r}",
            f"W wyniku odejmowania {i} - {j} otrzymamy {r}.",
            f"{i} minus {j} jest równe {r}",
            f"{i} minus {j} to {r}"
        ])
        instructions.append({"instruct": instr, "input": "", "output": output, "source_name" : source_name, "source_url" : source_url, "source_description" : source_description, "script_name" : script_name})


for i in range(5, 20):
    for j in range(i+1, 40):
        obj = random.choice(OBJECTS)
        name1, name2 = random.sample(NAMES, 2)
        name1_verb_end = 'a' if name1[-1] == 'a' else ''
        instr = random.choice([
            f"Miałem {j} {obj}, po czym kolega zabrał mi {i}. Ile teraz mam {obj}?",
            f"Wczoraj dostałem od rodziców {j} {obj}. Dziś oddałem {i} {obj} mojej siostrze. Policz ile mam teraz {obj}."
            f"Od {j} {obj} odejmij {j} {obj}. Ile otrzymałeś?",
            f"{name1} miał{name1_verb_end} {j} {obj}. Ktoś ukradł {i}. Ile teraz {obj} ma {name1}?",
            f"Jeśli {name1} miał{name1_verb_end} {j} {obj} i stracił{name1_verb_end} {i} {obj}, to ile teraz ma?",
            f"Niech {name1} dostanie {j} {obj} i odda {i}. Ile będzie wtedy mieć {obj}?",
            f"{name1} i {name2} mieli razem {j} {obj}. Oddali koledze {i}. Ile teraz mają {obj}?",
            f"Załóżmy, że {name1} ma {j} {obj}, a {name2} zabiera {j}. Ile {obj} zostaje?",
            f"Gdy {name1} miał{name1_verb_end} {j} {obj}, oddał{name1_verb_end} koleżance {i} {obj}. Oblicz ile {obj} pozostało.",
            f"Przedwczoraj miałem {j} {obj}. Wczoraj straciłem {i}. Ile mi zostało?",
            f"{name1} ma {j} {obj}. Obok stoi {name2} i zabiera {i} {obj}. Oblicz ile teraz {name1} ma {obj}."
        ])
        r = j - i
        output = random.choice([
            f"Wynik to {r}.",
            f"Wynikiem tego odejmowania jest {r}.",
            f"{r} {obj}",
            f"Wynikiem jest {r}",
            f"Odpowiedź: {r}.",
            f"Odpowiedź to {r} {obj}.",
            f"Prawidłowa odpowiedź to {r} {obj}.",
            f"{j} {obj} - {i} {obj} = {r} {obj}",
            f"Jeśli odejmiemy {i} {obj} od {j} {obj}, to otrzymamy {r} {obj}."
        ])
        instructions.append({"instruct": instr, "input": "", "output": output, "source_name" : source_name, "source_url" : source_url, "source_description" : source_description, "script_name" : script_name})


for k in range(3, 6):
    for _ in range(40):
        numbers = random.sample(range(1, 8), k)
        formula = " + ".join([str(n) for n in numbers])
        instr = random.choice([
            f"Wykonaj dodawanie {formula}.",
            f"Oblicz {formula}."
            f"Jaki jest wynik dodawania {formula}?",
            f"Podaj wynik dodawania {formula}.",
            f"Dodaj {formula}.",
            f"Ile wynosi {formula}?",
        ])
        s = numbers[0] + numbers[1]
        output = random.choice([
            "Wykonajmy obliczenia krok po kroku.\n",
            "Obliczmy to krok po kroku.\n",
            "Policzmy to małymi krokami.\n",
            "Rozbijmy obliczenia na mniejsze części.\n",
        ])
        output += f"W pierwszym kroku dodajmy dwie pierwsze liczby {numbers[0]} + {numbers[1]} = {s}."
        for i in range(2, k):
            output += f" Teraz nasze działanie wygląda tak: {s} + {' + '.join([str(n) for n in numbers[i:]])}.\n"
            output += f"Dodajmy {'kolejną' if i+1<k else 'ostatnią'} liczbę {s} + {numbers[i]} = {s + numbers[i]}."
            s += numbers[i]
        output += random.choice([
            f"\nZatem ostateczny wynik to {s}.",
            f"\nWynikiem całego dodawania jest {s}.",
            f"\nWynikiem jest {s}.",
            f"\nOdpowiedź: {s}.",
            f"\nOdpowiedź to {s}.",
            f"\nPrawidłowa odpowiedź to {s}.",
            f"\nWynikiem dodawania {formula} jest {s}",
            f"\nZatem {formula} = {s}."
        ])
        instructions.append({"instruct": instr, "input": "", "output": output, "source_name" : source_name, "source_url" : source_url, "source_description" : source_description, "script_name" : script_name})


for i in range(5, 20):
    for j in range(i+5, 40):
        obj = random.choice(OBJECTS)
        name1, name2 = random.sample(NAMES, 2)
        name1_verb_end = 'a' if name1[-1] == 'a' else ''
        instr = random.choice([
            f"Miałem {j} {obj}, po czym kolega zabrał mi {i}. Ile teraz mam {obj}?",
            f"Wczoraj dostałem od rodziców {j} {obj}. Dziś oddałem {i} {obj} mojej siostrze. Policz ile mam teraz {obj}."
            f"Od {j} {obj} odejmij {j} {obj}. Ile otrzymałeś?",
            f"{name1} miał{name1_verb_end} {j} {obj}. Ktoś ukradł {i}. Ile teraz {obj} ma {name1}?",
            f"Jeśli {name1} miał{name1_verb_end} {j} {obj} i stracił{name1_verb_end} {i} {obj}, to ile teraz ma?",
            f"Niech {name1} dostanie {j} {obj} i odda {i}. Ile będzie wtedy mieć {obj}?",
            f"{name1} i {name2} mieli razem {j} {obj}. Oddali koledze {i}. Ile teraz mają {obj}?",
            f"Załóżmy, że {name1} ma {j} {obj}, a {name2} zabiera {j}. Ile {obj} zostaje?",
            f"Gdy {name1} miał{name1_verb_end} {j} {obj}, oddał{name1_verb_end} koleżance {i} {obj}. Oblicz ile {obj} pozostało.",
            f"Przedwczoraj miałem {j} {obj}. Wczoraj straciłem {i}. Ile mi zostało?",
            f"{name1} ma {j} {obj}. Obok stoi {name2} i zabiera {i} {obj}. Oblicz ile teraz {name1} ma {obj}."
        ])
        s = j - i
        output = random.choice([
            f"Wynik to {s} {obj}.",
            f"Wynikiem tego odejmowania jest {s}.",
            f"{s} {obj}",
            f"Wynikiem jest {s} {obj}.",
            f"Odpowiedź: {s}.",
            f"Odpowiedź to {s} {obj}.",
            f"Prawidłowa odpowiedź to {s} {obj}.",
            f"{j} {obj} - {i} {obj} = {s} {obj}",
            f"Jeśli odejmiemy {i} {obj} od {j} {obj}, to otrzymamy {s} {obj}."
        ])
        instructions.append({"instruct": instr, "input": "", "output": output, "source_name" : source_name, "source_url" : source_url, "source_description" : source_description, "script_name" : script_name})


random.shuffle(instructions)
with open(os.path.join(output_dir, script_name.replace(".py", ".json")), "w", encoding='utf-8') as f:
    json.dump(instructions, f, indent=4, ensure_ascii=False)
print("Instructions: " + str(len(instructions)))

