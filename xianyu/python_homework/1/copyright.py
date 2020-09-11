# ask questions
# assume user will only enter integer for year/month/day
published_year = int(raw_input("In what year was the work published? "))
while published_year <= 1922:
    print("The year input must be a number greater than 1922.")
    published_year = int(raw_input("In what year was the work published? "))
published_month = int(raw_input("In what month was the work published? "))
while published_month > 12 or published_month < 1:
    print("The month input must be a number between 1 and 12.")
    published_month = int(raw_input("In what month was the work published? "))
published_day = int(raw_input("On what day of the month was the work published? "))
while published_day > 31 or published_day < 1:
    print("The day input must be a number between 1 and 31.")
    published_day = int(raw_input("On what day of the month was the work published? "))
input_is_given_notice = raw_input("Was notice of copyright given? ")
input_is_properly_renewed = raw_input("Was the work properly renewed (manually or automatically)? ")
input_has_protection_expired = raw_input("Has the original term of copyright protection expired? ")

if input_is_given_notice == 'y' or input_is_given_notice == 'yes':
    is_given_notice = True
else:
    is_given_notice = False

if input_is_properly_renewed == 'y' or input_is_given_notice == 'yes':
    is_properly_renewed = True
else:
    is_properly_renewed = False

if input_has_protection_expired == 'y' or input_has_protection_expired == 'yes':
    has_protection_expired = True
else:
    has_protection_expired = False

# make judgement
if published_year <= 1963:
    if is_given_notice and is_properly_renewed and not has_protection_expired:
        print("In Copyright")
    else:
        print("In Public Domain")
elif published_year >= 1964 and published_year <= 1977:
    if is_given_notice and not has_protection_expired:
        print("In Copyright")
    else:
        print("In Public Domain")
elif (published_year >= 1978 and published_year <= 1988) or (published_year == 1989 and published_month <= 2):
    if is_given_notice:
        print("In Copyright")
    else:
        print("In Public Domain")
elif published_year >= 1989 and published_month <= 2002:
    print("In Copyright")
else:
    if not expired:
        print("In Copyright")
    else:
        print("In Public Domain")

