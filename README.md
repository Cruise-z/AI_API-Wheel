# GPT_API-Wheel
My wheel of GPT_API



构造过程：

> 参考：https://zhuanlan.zhihu.com/p/510038317



## 使用方式

### 配置参数文件

- 参数文件后缀应为`.ini`

- 文件内容：

  ```ini
  [DEFAULT]
  api_key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  base_url=https://api.chatanywhere.tech/v1
  
  [free]
  api_key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  base_url=https://api.chatanywhere.tech/v1
  
  [paid]
  api_key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  base_url=https://api.chatanywhere.tech/v1
  ```

  ==注==：这里的`api_key`以及`base_url`不需要加引号

### 调库使用

#### 示例

```python
client_free = Client("./config.ini", "free")
client_paid = Client("./config.ini", "paid")

messages = ["你是谁？"]
chat_stream(client_paid, Model.gpt4o, messages)
```

