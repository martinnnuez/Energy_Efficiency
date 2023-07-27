import predict

input_example = {
    "X1": 0.68,
    "X2": 423.40,
    "X3": 205.00,
    "X4": 115.55,
    "X5": 6.00,
    "X6": 1,
    "X7": 0.00,
    "X8": 0,
}

features = predict.preprocess(input_example)
pred = predict.predict(features)

print(pred)
