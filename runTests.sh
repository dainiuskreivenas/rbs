mkdir -p tests/results

python tests/Operators_Numerics_Test.py > ./tests/results/Operators_Numerics_Tests.sp

python tests/Test_Decrement_Numerics.py > ./tests/results/Test_Decrement_Numerics.sp

python tests/Test_Increment_Numerics.py > ./tests/results/Test_Increment_Numerics.sp

python -m rbs.tests.run > ./rbs/tests/results.sp