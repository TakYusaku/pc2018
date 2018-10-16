import sys
def test():
    a = [[1,2],
         [3,4],
         [5,6]]

    try:
        b = a[3,0]
        result = True
    except:
        return False

    return result

if __name__ == "__main__":
    print(test())
