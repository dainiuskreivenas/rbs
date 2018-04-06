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
