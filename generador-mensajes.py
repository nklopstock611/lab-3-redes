
# 1MB para UDP

file = open("mensajes/1MB.txt", "w")
texto = 'a' * (100 * 1024 * 10)
file.write(texto)
file.close()

# 100MB para UDP

file = open("mensajes/100MB.txt", "w")
texto = 'a' * (100 * 1024 * 1000)
file.write(texto)
file.close()

# 250MB para UDP

file = open("mensajes/250MB.txt", "w")
texto = 'a' * (250 * 1024 * 1000)
file.write(texto)
file.close()
