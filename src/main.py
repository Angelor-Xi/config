"""Реализация минимального прототипа с конфигурацией (Этап 1)."""

import argparse
import sys


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
        choices=["local", "remote"],
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


def main():
    """Главная функция приложения."""
    parser = create_parser()
    args = parser.parse_args()
    validate_args(args)
    print_params(args)


if __name__ == "__main__":
    main()