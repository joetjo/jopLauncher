
def GHconsoleConfirm( label ):
    answer = input(label)
    print(answer)
    return answer == 'y'
