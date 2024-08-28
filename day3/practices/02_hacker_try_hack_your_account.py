class Account:
    def __init__(self, balance):
        self._password = "password1"  # 관례적으로 보호된 비밀번호
        self.__login = False  # private로 보호된 로그인 상태
        self.__balance = balance  # private로 보호된 잔고

    def show_password(self):
        # 비밀번호를 직접 노출하지 않음
        return "비밀번호를 보려면 안전한 방법을 사용하시기 바랍니다."

    def authenticate(self, input_password):
        # 입력된 비밀번호를 내부 비밀번호와 비교하여 인증
        self.__login = input_password == self._password

        if self.__login:
            return "인증 성공!"
        else:
            return "인증 실패!"

    def get_balance(self):
        return self.__balance

    def check_login(self):
        if not self.__login:
            raise ValueError("로그인 하셔야합니다.")

    def withdraw(self, amount):
        if self.__balance < amount:
            raise ValueError("잔고가 부족합니다.")
        self.__balance -= amount
        return f"성공적으로 인출되었습니다. 남은 잔고: {self.__balance}"


account = Account(100_0000_0000)  # 10_000_000_000

# 비밀번호 해킹 시도 (실패해야 하지만...)
try:
    print(account.show_password())  # 비밀번호 탈취 시도
    password = account._password  # 다른 방식으로 비밀번호 탈취 시도
    print(password)
    print(account.authenticate(password))  # 해킹 성공?
    account_balance = account.get_balance()
    print(account.withdraw(account_balance))
    print(f"해커는 {account_balance:,}원을 가져갔습니다.")
except AttributeError as e:
    print(f"접근 금지: {e}")  # 성공적으로 비밀번호를 지키면 보여줘야하는 오류
