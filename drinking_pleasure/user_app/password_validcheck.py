def password_validcheck(pwd):
    if len(pwd) < 8:
        print("패스워드의 길이기 적당하지 않습니다. 8자 이상으로 입력해주세요.")
        return False

    if pwd.isalnum() == False:
        return True
    else:
        print("비밀번호가 알파벳과 숫자로만 구성되어 있습니다. 특수 문자를 추가해주세요.")
        return False