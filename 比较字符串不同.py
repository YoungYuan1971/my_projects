string1 = 'abcdegfjkhi'
string2 = 'abcdefghkij'

zip_string = zip(string1, string2)
enum_string = enumerate(zip_string)

for i, (a, b) in enum_string:
    if a != b:
        print(f'index: {i}...{a, b}')
