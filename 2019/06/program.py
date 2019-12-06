orbits = {}

with open("local_orbits.txt", "r") as f:
    for line in f:
        (orbitee, orbiter) = line.rstrip().split(")")

        orbits[orbiter] = orbitee

def orbit_length(key):
    count = 1
    while orbits[key] in orbits:
        count += 1
        key = orbits[key]
    return count

def orbit_path_to_com(key):
    path = []
    while orbits[key] in orbits:
        path.append(orbits[key])
        key = orbits[key]
    return path

total = 0
for key in orbits.keys():
    total += orbit_length(key)

print(f'There are a total of {total} orbits.')

path_you = orbit_path_to_com("YOU")
path_san = orbit_path_to_com("SAN")

print(path_you)
print(path_san)

# From the top, find the first path in me that is also in SAN
for location in path_you:
    if location in path_san:
        break

print(f"Intersection at {location}")
print(f"{location} is at {path_you.index(location)} on your path")
print(f"{location} is at {path_san.index(location)} on Santa's path")
print(f"You require {path_you.index(location) + path_san.index(location)} transfers.")