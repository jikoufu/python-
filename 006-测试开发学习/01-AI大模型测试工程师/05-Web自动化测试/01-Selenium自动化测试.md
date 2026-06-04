# 01 Selenium 自动化测试学习过程

## 学习目标

这一模块学习 Web UI 自动化测试。

学完后你需要能够：

- 理解 Selenium 是什么。
- 使用 Selenium 打开浏览器。
- 定位页面元素。
- 模拟点击、输入、提交。
- 编写基础 UI 自动化测试用例。
- 使用 pytest 管理 Selenium 测试。
- 理解等待、断言、截图和失败排查。

## Selenium 是什么

Selenium 是一个浏览器自动化工具。

它可以像真实用户一样操作浏览器：

- 打开网页
- 点击按钮
- 输入文字
- 提交表单
- 获取页面文本
- 校验页面结果
- 截图

适合测试：

- 登录页面
- 表单提交
- 搜索功能
- 管理后台页面
- AI 聊天页面
- RAG 问答前端

## 阶段 1：准备环境

安装依赖：

```bash
pip install selenium pytest
```

如果使用 Chrome 浏览器，Selenium 4 通常可以自动管理驱动。

建议先确认本机安装了 Chrome。

## 阶段 2：第一个 Selenium 脚本

目标：打开一个网页并读取标题。

示例：

```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.baidu.com")

print(driver.title)

driver.quit()
```

重点：

- `webdriver.Chrome()` 创建浏览器对象。
- `driver.get()` 打开网页。
- `driver.title` 获取页面标题。
- `driver.quit()` 关闭浏览器。

## 阶段 3：元素定位

Selenium 常用定位方式：

```python
from selenium.webdriver.common.by import By

driver.find_element(By.ID, "kw")
driver.find_element(By.NAME, "wd")
driver.find_element(By.CLASS_NAME, "input")
driver.find_element(By.CSS_SELECTOR, "#kw")
driver.find_element(By.XPATH, "//input[@id='kw']")
```

推荐优先级：

1. `By.ID`
2. `By.CSS_SELECTOR`
3. `By.XPATH`

如果页面是自己开发的，建议给关键元素加稳定的测试属性：

```html
data-testid="login-button"
```

然后用 CSS 定位：

```python
driver.find_element(By.CSS_SELECTOR, "[data-testid='login-button']")
```

## 阶段 4：操作元素

常见操作：

```python
element.click()
element.send_keys("hello")
element.clear()
text = element.text
value = element.get_attribute("value")
```

示例：搜索关键词。

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://www.baidu.com")

search_input = driver.find_element(By.ID, "kw")
search_input.send_keys("FastAPI")
search_input.send_keys(Keys.ENTER)

driver.quit()
```

## 阶段 5：等待

UI 自动化最容易出问题的地方是页面加载时间。

不要大量使用：

```python
time.sleep(3)
```

更推荐显式等待：

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.presence_of_element_located((By.ID, "kw"))
)
```

常用等待条件：

- 元素出现
- 元素可点击
- 文本出现
- URL 变化
- 页面标题变化

## 阶段 6：结合 pytest

测试文件示例：

```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()


def test_page_title(driver):
    driver.get("https://www.baidu.com")
    assert "百度" in driver.title
```

运行：

```bash
pytest -q
```

## 阶段 7：页面对象模式

当测试用例变多后，不建议把定位器和操作都写在测试函数里。

可以使用 Page Object Model：

```text
pages/
├── login_page.py
tests/
└── test_login.py
```

页面类负责页面操作：

```python
class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        ...
```

测试用例只表达业务流程：

```python
def test_login_success(driver):
    page = LoginPage(driver)
    page.login("admin", "123456")
    assert page.is_login_success()
```

## 阶段 8：AI 应用中的 Selenium 测试

AI 应用常见前端测试场景：

- AI 聊天框能输入问题。
- 点击发送后页面出现回复。
- 回复内容不是空。
- 多轮对话上下文正常。
- 加载中状态出现并消失。
- 错误时有友好提示。
- 页面不会重复提交。

示例测试思路：

```text
打开 AI 聊天页面
输入问题
点击发送
等待回复出现
断言回复不为空
断言页面没有报错
截图保存结果
```

## 建议练习

1. 用 Selenium 打开百度并打印标题。
2. 定位搜索框并输入关键词。
3. 使用显式等待等待搜索结果。
4. 使用 pytest 改写脚本。
5. 给失败用例添加截图。
6. 尝试测试一个本地 FastAPI 或前端页面。
7. 为 AI 聊天页面写一个最小 UI 自动化用例。

## 本节重点

- Selenium 用来做浏览器 UI 自动化。
- 元素定位要尽量稳定。
- UI 自动化必须重视等待。
- pytest 可以管理 Selenium 测试。
- 页面对象模式可以让测试更清晰。
- AI 应用前端测试重点是交互流程和输出展示。
