REQUIRED_KEYS = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])

ALLOWED_KEYS = REQUIRED_KEYS | set(["cid"])


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
