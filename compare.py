import argparse
import re


class OpenFiles:
    """
    Принимает на вход строку, создает из нее массив
    """

    def __init__(self, str_with_files):
        self.files = str_with_files.split()


class OutputFiles(OpenFiles):
    """
    Считывает файлы, возвращает массив с 2 файлами
    """

    def readingfiles(self):
        to_out = []
        for eachfile in self.files:
            with open(eachfile, 'r', encoding='utf8') as python_text:
                to_out.append(python_text.read())
            python_text.close()
        return to_out


class StringFormatting:
    """
    Изменяет строку по шаблону
    не дописал :(
    """

    def __init__(self, string_with_files):
        self.files = OutputFiles(string_with_files).readingfiles()

    def formatting(self):
        for i in self.files:
            i = i.lower()
        return self.files


class LevenshteinDistance:
    """
    Рассчитывает расстояние Левенштейна

    Параметры
    ----------
    height,width - длина, ширина получившейся матрицы.
    Матрица строится по длине текста в файлах.

    distance - матрица для подсчета расстояния

    Вовращает
    ----------
    Число, рассчитанное как: 1 - расстояние Левенштейна/длина текста
    """

    def __init__(self, string_with_files):
        self.files = StringFormatting(string_with_files).formatting()

    def count_distance(self):
        # files_after_obr = obrabotka
        height = len(self.files[0]) + 1
        width = len(self.files[1]) + 1
        distance = []
        for i in range(height):
            if i == 0:
                distance.append([j for j in range(width)])
            else:
                distance.append([0] * width)
            distance[i][0] = i

        for i in range(1, height):
            for j in range(1, width):
                m = 1
                if self.files[1][j - 1] == self.files[0][i - 1]:
                    m = 0
                distance[i][j] = min(distance[i][j - 1] + 1, distance[i - 1][j] + 1, distance[i - 1][j - 1] + m)
        return (max(height, width) - distance[height - 1][width - 1]) / max(height, width)


def main():
    """
    Функия для работы программы.
    Принимает на вход необходимые файлы для открытия.

    Параметры
    ----------
    args - файлы для открытия и сохранения, записанные в виде строки
    saved - файл, куда сохранять
    file_with_list - документ c необходимыми для сравнений файлами формата .py
    string_with_files - строка с путями до файлов, одна из множества строк открытого файла
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    parser.add_argument('output', type=str)
    args = parser.parse_args()

    saved = open(args.output, 'w', encoding='utf8')
    with open(args.input, 'r') as file_with_list:
        for string_with_files in file_with_list:
            a = LevenshteinDistance(string_with_files).count_distance()
            saved.write(f'{a}\n')

    saved.close()
    file_with_list.close()


if __name__ == '__main__':
    main()
