from pathlib import Path

directory = Path(r'C:\Users\dblmo\PycharmProjects\WhiteStarTeleBot')
line_count = 0

for f in directory.rglob('*.py'):
    if '.venv' in f.parts or not f.is_file() or not f.exists():
        # Пропускаем файлы в папке venv
        continue

    local_count = 0
    try:
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()

            if not line or line.startswith(('#', '"', "'")):
                continue
            local_count += 1

        print(f'{f} - {local_count} ст')
        line_count += local_count
    except UnicodeDecodeError:
        print(f"Ошибка декодирования файла: {f}")

print("=====================================")
print(f"Всего строк - {line_count}")