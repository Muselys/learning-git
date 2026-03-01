name = "sahra musse"
print(name.title())
print(name.upper())
print(name.lower())

first_name = "sahra"
last_name = "musse"
full_name = f"{first_name} {last_name}"
print(full_name)

print(f"Hello, {full_name.title()}!")

message = f"Hello, {full_name.title()}!"
print(message)

print("python")
print("\tpython")
print("Languages:\npython\nC\nJavaScript")
print("Languages:\n\tpython\n\tC\n\tJavaScript")

favourite_language = ' python '
print(favourite_language)
print(favourite_language.lstrip())

nostarch_url = 'https://nostarch.com'
simple_url = nostarch_url.removeprefix('https://')
print(simple_url)