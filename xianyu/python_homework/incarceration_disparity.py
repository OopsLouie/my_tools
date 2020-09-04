# global values
largest_disparity = 0
state_with_largest_disparity = ""
all_states = ""

# assume enter at least one state
state_name = raw_input("State: ")
all_states += state_name

# start while loop
while state_name:
    # ask for input
    african_american_increased_population = int(raw_input("African American Incarcerated Population (per 100,000): "))
    caucasian_increased_population = int(raw_input("Caucasian Incarcerated Population (per 100,000): "))
    # count disparity
    disparity = float(african_american_increased_population) / float(caucasian_increased_population)
    # compaire and save
    if disparity > largest_disparity:
        largest_disparity = disparity
        state_with_largest_disparity = state_name
    # ask for another state
    state_name = raw_input("State: ")
    while state_name in all_states:
        print("You have already entered data for %s" % state_name)
        state_name = raw_input("State: ")
        if state_name == "":
            break
    all_states += state_name

# finally print the largest state with its disparity
print("The state with the highest disparity is %s" % state_with_largest_disparity)
print("The disparity is %0.15f" % largest_disparity)



