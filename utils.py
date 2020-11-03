from datetime import datetime

# time stamp


def timeStamp():
    return datetime.now().strftime("%H:%M:%S")


# timeStamped comment
def comment(commentContent, empty=False):
    if empty:
        print(f"{' '*len(timeStamp())} &> {commentContent}")
    else:
        print(f"{timeStamp()} &> {commentContent}")


def get(msg=''):
    return input(f"{8*' '} $> {msg}")


if __name__ == "__main__":
    print("-- utility file for Saaty project --")
