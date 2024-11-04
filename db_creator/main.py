import subprocess

# a fileok amiket indítunk
futtatas = [
    'ivkemence.py',
    'fill_the_table.py',
    'filter_the_data.py'
]

for file in futtatas:
    print(f"{file} futtatása...")
    subprocess.run(['python', file], check=True)
    print(f"{file} befejezve.\n")
