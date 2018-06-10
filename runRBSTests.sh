mkdir results

python tests/Monkey_SingleFruit.py
python printPklFile.py pkls/Monkey_SingleFruit > ./results/Monkey_SingleFruit.sp

python tests/Monkey_SingleWithChair.py
python printPklFile.py pkls/Monkey_SingleWithChair > ./results/Monkey_SingleWithChair.sp

python tests/Monkey_TwoFruits.py
python printPklFile.py pkls/Monkey_TwoFruits > ./results/Monkey_TwoFruits.sp

python tests/Monkey_TwoPlaceFruits.py
python printPklFile.py pkls/Monkey_TwoPlaceFruits > ./results/Monkey_TwoPlaceFruits.sp

python tests/Monkey_TwoSameFruits.py
python printPklFile.py pkls/Monkey_TwoSameFruits > ./results/Monkey_TwoSameFruits.sp

python tests/Monkey_TwoSamePlaceFruits.py
python printPklFile.py pkls/Monkey_TwoSamePlaceFruits > ./results/Monkey_TwoSamePlaceFruits.sp

python tests/Operators_Test.py
python printPklFile.py pkls/Operators_Numerics_Tests > ./results/Operators_Numerics_Tests.sp

python tests/Test_Decrement_Numerics.py
python printPklFile.py pkls/Test_Decrement_Numerics > ./results/Test_Decrement_Numerics.sp

python tests/Test_Increment_Numerics.py
python printPklFile.py pkls/Test_Increment_Numerics > ./results/Test_Increment_Numerics.sp

python tests/Test_Multiply_Numerics.py
python printPklFile.py pkls/Test_Multiply_Numerics > ./results/Test_Multiply_Numerics.sp

python tests/Test_Divide_Numerics.py
python printPklFile.py pkls/Test_Divide_Numerics > ./results/Test_Divide_Numerics.sp
