import pytest



# yield fixture
@pytest.fixture
def yield_fixture():
	print("Start Test Phase")
	yield 6
	print("End Test Phase")



# example using yield fixture
def test_example(yield_fixture):
	print("run-example-1")
	assert yield_fixture == 6

# function run once per function
# module run once per module
# session run once per session


# creating fixtures
# @pytest.fixture(scope="session")
# def my_fixture():
# 	print("fixture-1")
# 	return 1

# # using fixture
# def test_example3(my_fixture):
# 	print("example 3")
# 	num = my_fixture
# 	assert num == 1



# # @pytest.mark.skip
# # @pytest.mark.xfail
# @pytest.mark.slow
# def test_example():
# 	assert 1 == 1


# def test_example2():
# 	assert 1 == 1


# def test_example4(my_fixture):
# 	print("example 4")
# 	num = my_fixture
# 	assert num == 1



