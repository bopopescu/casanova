threshold = 0.5
learning_rate = 0.1
weights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

import random
training_set = [((1, 0, 0), 1), ((1, 0, 1), 1), ((1, 1, 0), 1), ((1, 1, 1), 0)]
test_set = [((0, 0, 0), 1), ((0, 0, 1), 1), ((0, 1, 0), 1), ((0, 1, 1), 0)]

# training_set = [(tuple([int(round(random.random())) for i in range(5)]),int(round(random.random()))) for j in range(8)]
# test_set = [(tuple([int(round(random.random())) for i in range(5)]),int(round(random.random()))) for j in range(2)]
 
def sum_function(values):
    s = sum(value * weights[index] for index, value in enumerate(values))
    return 1 if s > threshold else 0
    

import time
tempo = time.time() + 60
 
while True:
    error_count = 0
    for input_vector, desired_output in training_set:
        # print weights
        result = sum_function(input_vector)
        error = desired_output - result
        # print error
        if error != 0:
            error_count += 1
            for index, value in enumerate(input_vector):
                weights[index] += learning_rate * error * value
    if error_count == 0 or tempo <= time.time():
        break
    # print tempo -time.time()

error_count = 0
for input_vector, desired_output in test_set:
    result = sum_function(input_vector)
    if desired_output != result:
        error_count+=1
        
print "Acurracy =>%s" % ((len(test_set)-error_count)*1.0/len(test_set))
