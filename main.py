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
    subparsers = parser.add_subparsers(
        dest="command",
        help="Доступные команды",
        required=True,
        metavar="Команда"
    )

    # Версия
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0 beta'
    )
    # Отдельный обработчик для создания редактирования файлов
    # region Возможные аргументы для
    # region process
    process_parser = subparsers.add_parser(
        'process',
        help="Обработать файлы"
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
    # region find
    find_parser = subparsers.add_parser(
        'find',
        help="Искать файлы"
    )
    # Имя файла
    find_parser.add_argument(
        "-n", "--name",
        help="Имя файла для поиска"
    )
    # Патерн для поиска
    find_parser.add_argument(
        "-p", "--pattern",
        help="Патерн названия файла"
    )
    # endregion
    # region status
    status_parser = subparsers.add_parser(
        'status',
        help="Вывести статус о файле"
    )
    # Выбор файла
    status_parser.add_argument(
        "-f", "--filename",
        help="Файл для просмотра"
    )
    # Режим вывода
    status_parser.add_argument(
        "-a", "--all",
        help="Вывести весь статус файла",
    )
    # endregion
    # endregion
    # region Получение аргументов
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    try:
        if args.command == "process":
            handle_process(args)
        elif args.command == "find":
            handle_find(args)
        elif args.command == "status":
            handle_status(args)
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
def handle_find(args):
    found = False
    if args.name == args.pattern == None:
         raise Exception("Дебик, чё мне делать, укажи!")
    elif args.name != None and args.pattern != None:
        raise Exception("Дебик, выбери только 1 способ для поиска!")
    elif args.name != None:
        print("Найденные файлы:")
        for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
            for file in files:
                if file == args.name:
                    print(root+"/"+file)
                    found = True
        if not found:
            print("Файлы не найдены!")
    elif args.pattern != None:
        print("Найденные файлы:")
        for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
            for file in files:
                if args.pattern in file:
                    print(root+"\\"+file)
                    found = True
        if not found:
            print("Файлы не найдены!")
def handle_status(args):
    filename = args.filename
    if not os.path.exists(filename):
        raise Exception("Дебик, файл мне укажи!")
    amountLines = 0
    amountChars = 0
    with open(filename, "r") as f:
        for line in f:
            amountLines += 1
            amountChars += len(line)
    print(f"Информация о файле {filename}:")
    print("Размер -", os.path.getsize(filename))
    print("Количество строк -", amountLines)
    print("Количество символов -", amountChars)
    print("Формат файла -", filename.split(".")[-1])

if __name__ == '__main__':
    main()
