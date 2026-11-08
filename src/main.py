""" Основные операции  (Этап 3)."""

import argparse
import sys
import gzip
from urllib.request import urlopen
from urllib.error import URLError

DEFAULT_DEPTH = 3
DEFAULT_MODE = "local"
DEFAULT_OUTPUT = "graph.png"
DEFAULT_FORMAT = "tree"


def create_parser():
    """Создание парсеров аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Визуализация графа зависимостей пакетов"
    )
    parser.add_argument(
        "--package",
        required=True,
        help="Имя анализируемого пакета"
    )
    parser.add_argument(
        "--source",
        required=True,
        help="URL-адрес репозитория или путь к файлу" 
         " тестового репозитория"
    )
    parser.add_argument(
        "--mode",
        default=DEFAULT_MODE,
        choices=["local", "remote","test"],
        help="Режим работы с тестовым репозиторием"
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Имя сгенерированного файла с изображением графа"
    )
    parser.add_argument(
        "--format",
        default=DEFAULT_FORMAT,
        choices=["tree", "list"],
        help="Режим вывода зависимостей в формате ASCII-дерева"
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=DEFAULT_DEPTH,
        help="Максимальная глубина анализа зависимостей"
    )
    
    return parser


def validate_args(args):
    """Проверка ошибок."""
    if args.depth <= 0:
        print("Error: глубина не может равняться 0")
        sys.exit(1)
    if not args.package:
        print("Error: имя пакета не может быть пустым")
        sys.exit(1)
    if not args.source:
        print("Error: источник не может быть пустым")
        sys.exit(1)


def print_params(args):
    """Вывести все параметры в формате ключ-значение."""
    print("Настройки приложения:")
    print(f"  package: {args.package}")
    print(f"  source:  {args.source}")
    print(f"  mode:    {args.mode}")
    print(f"  output:  {args.output}")
    print(f"  format:  {args.format}")
    print(f"  depth:   {args.depth}")


def fetch_packages_file(source):
    """Скачать файл Packages.gz из репозитория."""
    try:
        url = f"{source}/dists/jammy/main/binary-amd64/Packages.gz"
        with urlopen(url) as response:
            return response.read()
    except URLError as error:
        print(f"Error: не удалось скачать файл: {error}")
        sys.exit(1)


def read_local_file(path):
    """Прочитать локальный файл."""
    try:
        with open(path, "rb") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: файл не найден: {path}")
        sys.exit(1)


def parse_dependencies(data, package_name):
    """Найти зависимости пакета в данных."""
    decompressed = gzip.decompress(data).decode("utf-8")
    packages = decompressed.split("\n\n")
    
    for package_block in packages:
        lines = package_block.strip().split("\n")
        current_package = None
        dependencies = []
        
        for line in lines:
            if line.startswith("Package:"):
                current_package = line.split(": ", 1)[1].strip()
            elif line.startswith("Depends:") and current_package == package_name:
                deps_str = line.split(": ", 1)[1].strip()
                dependencies = [
                    dep.strip().split("(")[0].strip()
                    for dep in deps_str.split(",")
                ]
                return dependencies
    
    return []


def get_dependencies(package_name, source, mode):
    """Получить зависимости пакета."""
    if mode == "remote":
        data = fetch_packages_file(source)
    elif mode == "local":
        data = read_local_file(source)
    else:
        print(f"Error: неизвестный режим: {mode}")
        sys.exit(1)
    
    return parse_dependencies(data, package_name)

def load_test_graph(path):
    """Загрузить граф из тестового файла (Пункт 4)."""
    try:
        graph = {}
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                package, deps_str = line.split(":", 1)
                package = package.strip()
                deps = [
                    dep.strip()
                    for dep in deps_str.split(",")
                    if dep.strip()
                ]
                graph[package] = deps
        return graph
    except FileNotFoundError:
        print(f"Error: файл не найден: {path}")
        sys.exit(1)


def build_graph_dfs(package, graph_data, source, mode, max_depth):
    """Построить граф зависимостей через DFS (Пункт 1, 2)."""
    result = {}
    visited = set()
    
    def dfs(current, depth):
        if depth > max_depth:
            return
        if current in visited:
            return
        visited.add(current)
        
        if mode == "test":
            deps = graph_data.get(current, [])
        else:
            deps = get_dependencies(current, source, mode)
        
        result[current] = deps
        
        for dep in deps:
            dfs(dep, depth + 1)
    
    dfs(package, 0)
    return result


def print_graph_ascii(graph, root):
    """Вывести граф в формате ASCII-дерева (Пункт 3)."""
    print(f"\nГраф зависимостей пакета '{root}':")
    
    def print_node(node, prefix, is_last, visited):
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{node}")
        
        if node in visited:
            print(f"{prefix}{'    ' if is_last else '│   '}(цикл)")
            return
        
        visited.add(node)
        deps = graph.get(node, [])
        
        for i, dep in enumerate(deps):
            is_last_dep = (i == len(deps) - 1)
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_node(dep, new_prefix, is_last_dep, visited.copy())
    
    print(root)
    deps = graph.get(root, [])
    for i, dep in enumerate(deps):
        is_last = (i == len(deps) - 1)
        print_node(dep, "", is_last, {root})

def print_dependencies(dependencies, package_name):
    """Вывести зависимости на экран. (Пункт 3. Этап 2.)"""
    print(f"\nПрямые зависимости пакета '{package_name}':")
    if dependencies:
        for dependency in dependencies:
            print(f"  - {dependency}")
    else:
        print("  Зависимости не найдены")


def main():
    """Главная функция приложения."""
    parser = create_parser()
    args = parser.parse_args()
    validate_args(args)
    print_params(args)
    
    if args.mode == "test":
        graph_data = load_test_graph(args.source)
        graph = build_graph_dfs(
            args.package,
            graph_data,
            args.source,
            args.mode,
            args.depth
        )
        if args.format == "tree":
            print_graph_ascii(graph, args.package)
        else:
            for package, deps in graph.items():
                print(f"{package}: {', '.join(deps)}")
    else:
        dependencies = get_dependencies(
            args.package,
            args.source,
            args.mode
        )
        print_dependencies(dependencies, args.package)

if __name__ == "__main__":
    main()