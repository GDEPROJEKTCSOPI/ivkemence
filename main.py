import subprocess

# a fileok amiket indítunk
futtatas = [
    'ivkemence.py',
    'fill_the_table.py',
    'filter_the_data.py'
]


# műveletek feldolgása
# adatok feldolgása
# add line to make changes


for file in futtatas:
    print(f"Running {file}...")
    subprocess.run(['python', file], check=True)
    print(f"{file} completed.\n")
