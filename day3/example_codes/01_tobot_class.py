class NotFoundTokeyError(Exception):
    """Exception raised when the tokey is not found."""

    def __init__(self, message="또키가 없습니다."):
        self.message = message
        super().__init__(self.message)


class Car:
    def __init__(self, name):
        self.__name = name  # 캡슐화: 이름을 private 속성으로 보호
        self.__state = "stop"  # 캡슐화: 상태를 private 속성으로 보호

    def get_name(self):
        return self.__name  # 캡슐화: private 속성에 접근하기 위한 public 메서드

    def get_state(self):
        return self.__state  # 캡슐화: private 속성에 접근하기 위한 public 메서드

    def run(self):
        self.__state = "running"
        return f"{self.get_name()}는 주행중입니다."


class Tobot(Car):
    def __init__(self, name):
        super().__init__(name)  # 상속: Car 클래스의 속성과 메서드를 상속받음
        self.__tokey = False  # 캡슐화: 변신을 제어하는 private 속성

    def insert_tokey(self):
        self.__tokey = True

    def release_tokey(self):
        self.__tokey = False

    def check_tokey(self):  # 캡슐화: tokey 존재 여부 확인 메서드
        if not self.__tokey:
            raise NotFoundTokeyError()
        return True

    def transform(self):
        # 추상화: 변신 기능을 위한 메서드로, 구체적인 구현은 서브클래스에서 제공
        raise NotImplementedError("이 메서드는 서브클래스에서 구현되어야 합니다.")


class TobotOriginal(Tobot):
    def transform(self):
        self.check_tokey()  # 캡슐화: 변신 전에 tokey 확인
        self._Car__state = "transformed"  # 캡슐화: 부모 클래스의 private 속성 접근
        return f"{self.get_name()}는 또봇 모드로 변신합니다."


class TobotAdventure(Tobot):
    def transform(self):
        self.check_tokey()  # 캡슐화: 변신 전에 tokey 확인
        self._Car__state = (
            "adventure_transformed"  # 캡슐화: 부모 클래스의 private 속성 접근
        )
        return f"{self.get_name()}는 어드벤쳐 또봇 모드로 변신합니다."


# 다형성: 변신 메서드를 호출할 때 각 클래스의 구현에 따라 다른 결과를 출력
def display_transformation(tobot):
    try:
        print(tobot.transform())
    except NotFoundTokeyError as e:
        print(e)


# 인스턴스 생성 및 사용
tobot_original_x = TobotOriginal("또봇 X")
tobot_adventure_x = TobotAdventure("또봇 X")

# 캡슐화: 객체의 상태를 보호하고, 메서드를 통해서만 접근
print(f"현재 {tobot_original_x.get_name()}의 상태: {tobot_original_x.get_state()}")
print(f"현재 {tobot_adventure_x.get_name()}의 상태: {tobot_adventure_x.get_state()}")

# 상속: Car 클래스의 run 메서드를 사용하여 상태 변경
tobot_original_x.run()
tobot_adventure_x.run()

# 객체의 상태 변화 확인
print(f"현재 {tobot_original_x.get_name()}의 상태: {tobot_original_x.get_state()}")
print(f"현재 {tobot_adventure_x.get_name()}의 상태: {tobot_adventure_x.get_state()}")

# 변신을 위한 키 삽입
tobot_original_x.insert_tokey()
tobot_adventure_x.insert_tokey()

# 다형성: 변신 메서드를 호출할 때 각 클래스의 구현에 따라 다른 결과를 출력
display_transformation(tobot_original_x)  # 또봇 X는 또봇 모드로 변신합니다.
display_transformation(tobot_adventure_x)  # 또봇 X는 어드벤쳐 또봇 모드로 변신합니다.

# 객체의 상태 변화 확인
print(f"현재 {tobot_original_x.get_name()}의 상태: {tobot_original_x.get_state()}")
print(f"현재 {tobot_adventure_x.get_name()}의 상태: {tobot_adventure_x.get_state()}")
