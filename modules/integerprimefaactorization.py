#here is sample private key for rsa incryption: http://ospkibook.sourceforge.net/docs/OSPKI-2.4.7/OSPKI-html/sample-key-components.htm
#can be used to compute the prime factors of an integer, was designed for RSA, but would take around a decade
import time

rsa = int(input("Enter the value for brute force factorization here. Only decimal digits: "))

print("This is going to take a while.")
start = time.time()

counter = 2
i = 2
numb = []
while counter < rsa:
    if counter == i:
        numb.append(counter)
        i = 2
        counter = counter + 1
    while counter > i:
        if counter % i == 0:
            counter = counter + 1
            i = 2
        else:
            i = i + 1

j = 0
k = 0
while numb[j] * numb[k] != rsa:
    if numb[j] < numb[-1]:
        j = j + 1
    else:
        j = 0
        k = k + 1
print("Here are your two prime values")
print(numb[j])
print(numb[k])

end = time.time()
print(end - start)
