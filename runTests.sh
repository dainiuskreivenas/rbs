mkdir -p tests/results

python tests/Operators_Numerics_Test.py > ./tests/results/Operators_Numerics_Tests.sp

python tests/Test_Decrement_Numerics.py > ./tests/results/Test_Decrement_Numerics.sp

python tests/Test_Increment_Numerics.py > ./tests/results/Test_Increment_Numerics.sp

python tests/Test_Multiply_Numerics.py > ./tests/results/Test_Multiply_Numerics.sp

python tests/Test_Divide_Numerics.py > ./tests/results/Test_Divide_Numerics.sp

python tests/Assert_Decrement_Numerics.py > ./tests/results/Assert_Decrement_Numerics.sp

python tests/Assert_Increment_Numerics.py > ./tests/results/Assert_Increment_Numerics.sp

python tests/Assert_Multiply_Numerics.py > ./tests/results/Assert_Multiply_Numerics.sp

python tests/Assert_Divide_Numerics.py > ./tests/results/Assert_Divide_Numerics.sp

python tests/fsaTests.py > ./tests/results/FsaTests.sp