from dataclasses import dataclass

with open('input/test.txt') as f:
    lines = [line.rstrip() for line in f]

@dataclass
class Seed:
    seed_number: int
    soil: int = None
    fertilizer: int = None
    water: int = None
    light: int = None
    temperature: int = None
    humidity: int = None
    location: int = None

@dataclass
class AlmanacMap:
    destination: int = None
    source: int = None
    range_length: int = None

    def in_range(self, this_source):
        if this_source in range(self.source, self.source + self.range_length):
            return True
        else:
            return False


input_section = 0
seed_list = dict()
seed_to_soil = []
soil_to_fert = []
fert_to_water = []
water_to_light = []
light_to_temp = []
temp_to_humid = []
humid_to_loc = []


for this_line in lines:
    if this_line == '':
        input_section += 1
    elif "map" in this_line:
        pass
    elif input_section == 0:  # Seed list
        temp_seeds = [int(f) for f in this_line[7:].split()]
        for this_seed in temp_seeds:
            seed_list[this_seed] = Seed(this_seed)
    else:
        d, s, r = [int(f) for f in this_line.split()]  # Destination, Source, and Range Length
        if input_section == 1:  # Seed-to-soil
            seed_to_soil.append(AlmanacMap(d, s, r))
        elif input_section == 2:  # Soil-to-fertilizer
            soil_to_fert.append(AlmanacMap(d, s, r))
        elif input_section == 3:  # Fertilizer-to-water
            fert_to_water.append(AlmanacMap(d, s, r))
        elif input_section == 4:  # Water-to-light
            water_to_light.append(AlmanacMap(d, s, r))
        elif input_section == 5:  # Light-to-temp
            light_to_temp.append(AlmanacMap(d, s, r))
        elif input_section == 6:  # Temp-to-humidity
            temp_to_humid.append(AlmanacMap(d, s, r))
        elif input_section == 7:  # Humidity-to-location
            humid_to_loc.append(AlmanacMap(d, s, r))
        else:
            print(f'Unexpected input section {input_section}')

for this_seed in seed_list.values():
    for map_entry in seed_to_soil:
        if map_entry.in_range(this_seed.seed_number):
            offset = this_seed.seed_number - map_entry.source
            this_seed.soil = map_entry.destination + offset
            break
    if this_seed.soil is None:
        this_seed.soil = this_seed.seed_number

    for map_entry in soil_to_fert:
        if map_entry.in_range(this_seed.soil):
            offset = this_seed.soil - map_entry.source
            this_seed.fertilizer = map_entry.destination + offset
    if this_seed.fertilizer is None:
        this_seed.fertilizer = this_seed.soil

    for map_entry in fert_to_water:
        if map_entry.in_range(this_seed.fertilizer):
            offset = this_seed.fertilizer - map_entry.source
            this_seed.water = map_entry.destination + offset
    if this_seed.water is None:
        this_seed.water = this_seed.fertilizer

    for map_entry in water_to_light:
        if map_entry.in_range(this_seed.water):
            offset = this_seed.water - map_entry.source
            this_seed.light = map_entry.destination + offset
    if this_seed.light is None:
        this_seed.light = this_seed.water

    for map_entry in light_to_temp:
        if map_entry.in_range(this_seed.light):
            offset = this_seed.light - map_entry.source
            this_seed.temperature = map_entry.destination + offset
    if this_seed.temperature is None:
        this_seed.temperature = this_seed.light

    for map_entry in temp_to_humid:
        if map_entry.in_range(this_seed.temperature):
            offset = this_seed.temperature - map_entry.source
            this_seed.humidity = map_entry.destination + offset
    if this_seed.humidity is None:
        this_seed.humidity = this_seed.temperature

    lowest_location = None
    for map_entry in humid_to_loc:
        if map_entry.in_range(this_seed.humidity):
            offset = this_seed.humidity - map_entry.source
            this_seed.location = map_entry.destination + offset
    if this_seed.location is None:
        this_seed.location = this_seed.humidity
    if lowest_location is None:
        lowest_location = this_seed.location
    if this_seed.location < lowest_location:
        lowest_location = this_seed.location

    print(f'Seed {this_seed.seed_number}, soil {this_seed.soil}, fertilizer {this_seed.fertilizer}, '
          f'water {this_seed.water}, light {this_seed.light}, temperature {this_seed.temperature}, '
          f'humidity {this_seed.humidity}, location {this_seed.location}')

print()
print(f'Part 1: {lowest_location}')


"""
Part 1
2505903167 is too high
"""