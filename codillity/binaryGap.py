

# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(N):
    count_list = []
    binary = '{0:08b}'.format(N)
    binary = binary.lstrip('0')
    binary = binary.rstrip('0')
    for elem in binary.split('1'):
        if '0' in elem:
            count_list.append(elem)
    if len(count_list) > 0:
        return len(max(count_list))
    elif len(count_list) == 0:
        return 0

