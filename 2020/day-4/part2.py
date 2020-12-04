import re


class ValidationError(Exception):
    pass


def between(val, min, max):
    return val >= min and val <= max


def readPassports(data):
    passport = dict()
    for line in data:
        line = line.strip()
        if line == "":
            yield passport
            passport = dict()
        else:
            passport.update(value.split(":") for value in line.split(" "))
    if passport:
        yield passport


def validateHeight(val):
    units = val[-2:]
    height = int(val[0:-2])
    if units == "cm":
        return between(height, 150, 193)
    elif units == "in":
        return between(height, 59, 76)
    raise Exception(f"Unknown units '{units}'")


EYE_COLORS = set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])

VALIDATIONS = {
    "byr": lambda val: between(int(val), 1920, 2002),
    "iyr": lambda val: between(int(val), 2010, 2020),
    "eyr": lambda val: between(int(val), 2020, 2030),
    "hgt": validateHeight,
    "hcl": re.compile(r"^#[0-9a-f]{6}$").match,
    "ecl": lambda val: val in EYE_COLORS,
    "pid": re.compile(r"^[0-9]{9}$").match,
}

ALLOWED_KEYS = set(list(VALIDATIONS.keys()) + ["cid"])


def validatePassport(passport):
    unallowed_keys = ALLOWED_KEYS - set(passport.keys())
    if not all(key in ALLOWED_KEYS for key in passport):
        raise ValidationError(f"Unallowed keys {unallowed_keys}")

    for key, validation in VALIDATIONS.items():
        val = passport[key]
        if not validation(val):
            raise ValidationError(f"Invalid {key} val - '{val}' failed validation")

    return True


def filterValidPassports(passports):
    for passport in passports:
        try:
            if validatePassport(passport):
                yield passport
        except ValidationError:
            pass
        except KeyError as err:
            if str(err).strip("'") not in VALIDATIONS:
                print(err)
        except Exception as err:
            print(f"Unknown err: {err}")


with open("./data.txt", "r") as fp:
    passports = readPassports(fp.readlines())
    valid_passports = filterValidPassports(passports)
    print(sum(1 for p in valid_passports))
