# Makefile

# 定义 Python 测试命令
PYTHON_TEST_CMD = python -m unittest

# 定义测试目录
TEST_DIR = app

# 定义测试文件模式
TEST_FILE_PATTERN = *_test.py

# 定义测试目标
test:
	find $(TEST_DIR) -name $(TEST_FILE_PATTERN) | xargs $(PYTHON_TEST_CMD)

.PHONY: test