import numpy as np
from PIL import Image


def Encode(src, message, dest):
    # инициализация фото
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size // n

    # добавляем разделитель
    message += "$t3g0"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    # достаточно ли пикселей
    if req_pixels > total_pixels:
        print("ERROR: Необходим файл с наибольшим разрешением")

    else:
        # изменяем биты сообщения
        index = 0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1

        # собираем изображение
        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Фото успешно закодировано")


def Decode(src):
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size // n

    # извлечь младшие значащие биты из каждого пикселя
    # начиная с верхнего левого угла изображения, и сохранить их в группах по 8

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]

    # преобразуем эти группы в символы ASCII, чтобы найти скрытое сообщение,
    # пока не прочитаем разделитель
    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "$t3g0" in message:
        print("Извлеченное сообщение:", message[:-5])
    else:
        print("Извлеченное сообщение не найдено")


if __name__ == '__main__':
    print("--reeklama lsb-program--")
    print("1: Закодировать")
    print("2: Раскодировать")

    func = input()

    if func == '1':
        print("Введите название входящего файла")
        src = input()
        print("Введите сообщение для внедрения")
        message = input()
        print("Введите название для преобразованного фото")
        dest = input()
        print("Кодирую...")
        print("пу")
        print("пу")
        print("пу")
        Encode(src, message, dest)

    elif func == '2':
        print("Введите название входящего файла")
        src = input()
        print("Раскодирую...")
        Decode(src)

    else:
        print("ERROR: Invalid option chosen")
