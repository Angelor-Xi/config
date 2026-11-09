Выполненные этапы

Этап 1. Минимальный прототип с конфигурацией
- Реализован CLI с настраиваемыми параметрами через `argparse`
- Параметры: `--package`, `--source`, `--mode`, `--output`, `--format`, `--depth`
- Валидация аргументов и вывод настроек в формате ключ-значение
  
Данные для проверки:

python src/main.py --package requests --source https://github.com/psf/requests

python src/main.py --help

python src/main.py --package requests --source test --depth -1

Этап 2. Сбор данных
- Извлечение информации о прямых зависимостях пакета из URL репозитория
- Парсинг сжатого файла `Packages.gz` из репозитория Ubuntu (jammy)
- Поддержка локального и удалённого режимов работы
  
Данные для проверки:

python src/main.py --package nginx --source http://archive.ubuntu.com/ubuntu --mode remote

Этап 3. Основные операции
- Построение графа зависимостей алгоритмом DFS с рекурсией
- Учёт максимальной глубины анализа (`--depth`)
- Корректная обработка циклических зависимостей
- Тестовый режим с файлом описания графа
  
Содержимое файла test_graph.txt:

A: B, C

B: D

C: D, E

D: F

E:

F:

Данные для проверки:

python src/main.py --package A --source tests/test_graph.txt --mode test --depth 3

Проверка цикла:

  test_graph.txt:
  
  A: B
  
  B: C
  
  C: A
  
  Данные для проверки:
  
  python src/main.py --package A --source tests/test_graph.txt --mode test --depth 5

Этап 4. Дополнительные операции
- Поддержка режима обратных зависимостей (`--direction backward`)
- Использование того же алгоритма обхода для обоих направлений
  
Содержимое файла test_graph.txt:

A: B, C

B: D

C: D, E

D: F

E:

F:

Данные для проверки:

python src/main.py --package D --source tests/test_graph.txt --mode test --depth 3 --direction forward

python src/main.py --package D --source tests/test_graph.txt --mode test --depth 3 --direction backward

Этап 5. Визуализация
- Генерация текстового представления графа на языке Mermaid
- Сохранение изображения графа в формате SVG через API mermaid.ink
- Вывод зависимостей в виде ASCII-дерева
- Демонстрация на трёх различных пакетах (A, B, C)
  
Данные для проверки:

python src/main.py --package A --source tests/test_graph.txt --mode test --depth 3 --output pkg_A.svg

python src/main.py --package B --source tests/test_graph.txt --mode test --depth 3 --output pkg_B.svg

python src/main.py --package D --source tests/test_graph.txt --mode test --depth 3 --direction backward --output pkg_D_backward.svg
