# encoding=utf-8
import cv2

mapping = {
    "0101000": 1,
    "0110111": 2,
    "0101111": 3,
    "1101010": 4,
    "1001111": 5,
    "1011111": 6,
    "0101100": 7,
    "1101100": 7,
    "1111111": 8,
    "1101110": 9,
    "1101111": 9,
    "1111101": 0,
}


def line_profile(image, profType, loc):
    height, width = image.shape[:2]
    if (profType == "h"):
        return image[int(round(height * loc)):int(round(height * loc)) + 1, 0:width]
    elif (profType == "v"):
        return image[0:height, int(round(0.5 * width)):int(round(0.5 * width) + 1)]


def check_high(arraySlice, N=4, threshold=100):
    numInRow = 0
    maxInRow = 0
    for x in arraySlice:
        if (x >= threshold):
            numInRow = numInRow + 1
        else:
            if numInRow > maxInRow:
                maxInRow = numInRow
            numInRow = 0
    if (maxInRow > N or numInRow > N):
        return 1
    else:
        return 0


def get_process_string_horiz(arr):
    firstHalf = check_high(arr[0:int(round(len(arr) / 2))])
    lastHalf = check_high(arr[int(round(len(arr) / 2)):len(arr)])
    return str(firstHalf) + str(lastHalf)


def get_process_string_vert(arr):
    firstQuarter = check_high(arr[0:int(round(len(arr) / 4))])
    middleHalf = check_high(arr[int(round(1 * len(arr) / 4)):int(round(3 * len(arr) / 4))])
    lastQuarter = check_high(arr[int(3 * round(len(arr) / 4)):len(arr)])
    return str(firstQuarter) + str(middleHalf) + str(lastQuarter)


def resolve_digit(croppedImage):
    l1 = line_profile(croppedImage, "h", 0.25)
    l2 = line_profile(croppedImage, "h", 0.75)
    l3 = line_profile(croppedImage, "v", 0.5)
    l1_arr = [int(x) for x in l1[0]]
    l2_arr = [int(x) for x in l2[0]]
    l3_arr = [int(x) for x in l3]

    processString = get_process_string_horiz(l1_arr) + get_process_string_horiz(
        l2_arr) + get_process_string_vert(l3_arr)
    digit = mapping.get(processString)
    return digit
