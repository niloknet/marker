# Integer to
int_value = 5
float_value = float(int_value)  # 5.0
str_value = str(int_value)  # '5'
bool_value = bool(int_value)  # True

int_value = 0
bool_value = bool(int_value)  # False

# Float to
float_value = 5.75
int_value = int(float_value)  # 5
str_value = str(float_value)  # '5.75'
bool_value = bool(float_value)  # True

float_value = 0.0
bool_value = bool(float_value)  # False

# String to
str_value = "10"
int_value = int(str_value)  # 10
float_value = float(str_value)  # 10.0

str_value = "10.0"
int_value = int(str_value)  # ValueError: invalid literal for int() with base 10: '10.0'
float_value = float(str_value)  # 10.0

str_value = "10.5"
int_value = int(str_value)  # ValueError: invalid literal for int() with base 10: '10.5'
float_value = float(str_value)  # 10.5

str_value = "True"
bool_value = bool(str_value)  # True

str_value = "False"
bool_value = bool(str_value)  # True

str_value = ""
bool_value = bool(str_value)  # False

# Boolean to
bool_value = True
int_value = int(bool_value)  # 1
float_value = float(bool_value)  # 1.0
str_value = str(bool_value)  # 'True'

bool_value = False
int_value = int(bool_value)  # 0
float_value = float(bool_value)  # 0.0
str_value = str(bool_value)  # 'False'

# None To
none_value = None
int_value = int(none_value)
# TypeError: int() argument must be a string, a bytes-like object or a number, not 'NoneType'
float_value = float(none_value)
# TypeError: float() argument must be a string or a number, not 'NoneType'
str_value = str(none_value)  # 'None'
bool_value = bool(none_value)  # False
