from itertools import groupby

REQUIRED_KEYS = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])

ALLOWED_KEYS = REQUIRED_KEYS | set(["cid"])


def readGroups(data):
    data = (line.strip() for line in data)
    return (group for blank, group in groupby(data, lambda v: v == "") if not blank)


def readPassports(data):
    for group in readGroups(data):
        passport = dict()
        for line in group:
            passport.update(value.split(":") for value in line.split(" "))
        yield passport


def filterValidPassports(passports):
    for passport in passports:
        if any(key not in ALLOWED_KEYS for key in passport):
            print([key for key in passport if key not in ALLOWED_KEYS])
            continue
        if all(required in passport for required in REQUIRED_KEYS):
            yield passport


with open("./data.txt", "r") as fp:
    passports = readPassports(fp.readlines())
    valid_passports = filterValidPassports(passports)
    print(sum(1 for p in valid_passports))
