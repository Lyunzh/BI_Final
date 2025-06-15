import pexpect

def ask_openmanus(user_input: str) -> str:
    # 启动 OpenManus CLI
    child = pexpect.spawn('python OpenManus/main.py', encoding='utf-8', timeout=30)

    # 等待它的输入提示（取决于 OpenManus 的实际提示）
    child.expect('Enter your prompt:')  # 

    # 发送输入
    child.sendline(user_input)

    # 等待输出完成，可以改成 EOF 或提示符
    child.expect(pexpect.EOF, timeout=300)  # ⚠️ 替换为 CLI 输出完的标志，例如 >>> 或空行
    output = child.before  # 获取输出内容

    child.close()

    return output.strip()

# 示例调用
if __name__ == "__main__":
    response = ask_openmanus("请写一个天气爬虫")
    print("OpenManus 返回：\n", response)
