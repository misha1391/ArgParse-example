import argparse
import sys
import os

def main():
    # Создание обработчика команд
    parser = argparse.ArgumentParser(
        description="Утилита для работы с файлами",
        epilog="""
       Примеры использования:
       %(prog)s --file data.txt
       """
    )
    # parser.add_help(

    # )
    subparsers = parser.add_subparsers(
        dest="command",
        help="Доступные команды",
        required=True,
        metavar="Команда"
    )
    # region Возможные аргументы
    # Версия
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0 beta'
    )
    # Отдельный обработчик для создания редактирования файлов
    # Обработка файлов
    process_parser = subparsers.add_parser(
        'process',
        help="Обработать файлы",
    )
    # Входной файл
    process_parser.add_argument(
        "-i", "--input",
        required=True,
        help="Входной файл",
    )
    # Выходной файл
    process_parser.add_argument(
        "-o", "--output",
        help="Выходной файл",
    )
    # Режим работы
    process_parser.add_argument(
        "-m","--mode",
        choices=['fast', 'normal', 'extreme'],
        default='normal',
        help="Выбор режима работы",
    )
    # Перезаписать файлы
    process_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Перезаписать файлы",
    )
    # endregion
    # region Получение аргументов
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    try:
        if args.command == 'process':
            handle_process(args)
    except Exception as e:
        print(e)
        sys.exit(1)
    # endregion

def handle_process(args):
    input_file = args.input
    output_file = args.output or f"{os.path.splitext(input_file)[0]}_processed.txt"
    print(args)
    print(input_file)
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Дурак, ты файл мне передай, а то как мне работать!") # Выдать ошибку
    if os.path.exists(output_file) and not args.overwrite:
        raise Exception("Дебик, Такой файл уже есть я не буду его трогать потому что ты уго уже трогал")

    print(f"Обработка файла: {input_file}")
    print(f"Ещё чуть-чуть: {input_file}")
    print(f"Результат будет сохранен в  : {output_file}")

    with open(input_file, 'r', encoding="utf-8") as f:
        content = f.read()
    processed_content = content.upper()
    with open(output_file, 'w', encoding="utf-8") as f:
        content = f.write(processed_content)
    print("Файл обработан")

if __name__ == '__main__':
    main()