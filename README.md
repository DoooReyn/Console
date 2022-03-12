# Console Logger for Cocos2d-x

## 一、介绍

**Console** 是为 Cocos2d-x 制作的日志控制台，通过 WebSocket 来转发日志。

### 特性

- 支持日志等级分类控制
- 支持 WebSocket 断线重连
- 支持给 Cocos2d-x 客户端发消息，可以用来**自定义指令**，控制客户端行为

## 二、设计架构

### 工作流

- 在 Cocos2d-x 创建 websocket server
- 在 Console GUI 创建 websocket client
- Lua 层格式化日志消息，通过 websocket 转发给 Console
- Console 收到消息后打印出来

### 依赖项

- Cocos2d-x
    - [cocos2d-x-lws](https://github.com/DoooReyn/cocos2d-x-lws)
    - [lua_format_log](https://github.com/DoooReyn/lua_format_log)
- Console GUI
    - [PyQt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
    - [websocket-client](https://github.com/websocket-client/websocket-client)

## 三、截图

![](./screenshot/log.png)

