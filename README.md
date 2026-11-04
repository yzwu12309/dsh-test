# dsh-test

dsh-test 是一个面向 DeepSeek Harness（DSH）Superagent 的集成测试仓库，用于验证代理从接收飞书或 GitHub 需求、创建工单、修改代码，到提交 Pull Request 并在原会话中回报结果的完整协作流程。本仓库不承载生产业务代码，主要用于功能演示、流程演练与回归测试。

## 最简 Python Web 示例

仓库内含一个仅使用 Python 标准库的 Hello World Web 项目，无需安装第三方依赖，要求 Python 3.10 及以上版本。

### 运行

```bash
python3 app.py
```

服务默认监听 `http://127.0.0.1:8000/`，按 `Ctrl+C` 停止。

### 接口

`GET /`：返回 JSON 格式的 Hello World。

```bash
curl http://127.0.0.1:8000/
```

响应：

```json
{"message": "Hello, World!"}
```

`POST /tickets/<ticket_id>/cancel`：取消工单 mock 接口，不修改任何真实数据，直接返回取消成功。

```bash
curl -X POST http://127.0.0.1:8000/tickets/T-1001/cancel
```

响应：

```json
{"ticket_id": "T-1001", "status": "cancelled"}
```

### 测试

```bash
python3 -m unittest discover -v
```
