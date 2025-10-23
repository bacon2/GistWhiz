from answer_checker.compare import answers_match

# print(answers_match("5 g", "0.005 kg"))  # True
print(answers_match(input("Enter original answer: "), input("Enter something close enough: ")))