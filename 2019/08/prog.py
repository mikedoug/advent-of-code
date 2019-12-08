class LayeredImage(object):
    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns

    def parse_raw_data(self, data):
        chunk_size = self._rows * self._columns
        self.layers = [ data[i:i+chunk_size] for i in range(0, len(data), chunk_size) ]

    def get_flattened_image(self):
        picture = []
        for i in range(self._rows * self._columns):
            for layer in self.layers:
                if layer[i] != '2':
                    picture.append( {'0': ' ', '1': 'X'}[layer[i]] )
                    break

        picture = "".join(picture)

        return [ picture[i:i+self._columns] for i in range(0, self._rows * self._columns, self._columns) ]

        
with open("input.txt", "r") as f:
    raw_image_data = f.readline().rstrip()

image = LayeredImage(6,25)
image.parse_raw_data(raw_image_data)

min_n0_layer = min(image.layers, key = lambda x: x.count('0'))

print(f'Winning Layer: {min_n0_layer}')
print(f'count("1") * count("2") = {min_n0_layer.count("1") * min_n0_layer.count("2")}')
print()

picture = image.get_flattened_image()
for row in picture:
    print (row)
