# 怪物火车2存档上传同步工具

## 项目简介
本项目是一个基于Python和Tkinter开发的图形化工具，用于在本地与远程服务器之间同步《怪物火车2》的存档文件。支持一键上传和下载，便于在多台设备间共享游戏进度。
## 实际上只要有个地方能存metagameSave.json文件就行。

## 主要功能
- 一键上传本地存档到远程服务器
- 一键从远程服务器下载存档到本地
- 自动备份本地旧存档，防止数据丢失
- 简单易用的图形界面

## 使用方法

### 1. 环境依赖
- Python 3.7 及以上
- 依赖库：
  - paramiko
  - tkinter（标准库自带）

安装依赖（推荐使用pip）：
```bash
pip install paramiko
```

### 2. 配置说明
首次运行会自动生成 `config.ini` 配置文件，请填写远程服务器的SSH信息：
```
[Server]
hostname = 服务器IP或域名
username = 用户名
password = 密码
port = 22
```

### 3. 运行方式
在Windows下，直接双击或命令行运行：
```bash
python 脚本同步.py
```

### 4. 存档路径说明
- 本地存档路径：
  `C:\Users\你的用户名\AppData\LocalLow\Shiny Shoe\MonsterTrain2\metagameSave.json`
- 远程存档路径：
  `/home/metagameSave.json`

## 注意事项
- 请确保远程服务器已开启SSH服务，且账号有读写 `/home/metagameSave.json` 的权限。
- 上传/下载过程中请勿手动修改存档文件，避免数据损坏。
- 下载时会自动备份本地旧存档，备份文件名格式为 `metagameSave_时间戳.json.bak`。

## 常见问题与解决方案
- **Q: 连接失败/认证失败？**
  - 检查 `config.ini` 配置是否正确，服务器是否可达，账号密码是否正确。
- **Q: 本地找不到存档？**
  - 确认游戏已正常运行并生成存档。
- **Q: 上传/下载失败？**
  - 检查网络连接，服务器磁盘空间，或查看 `sync.log` 日志获取详细错误信息。

## 跨平台说明
- 本工具主运行环境为Windows，因存档路径为Windows格式。
- 若需在Linux（如CentOS 7）运行，请确保Tkinter和paramiko可用，并手动调整本地存档路径为Linux下的实际路径。

## 日志
- 所有同步操作会记录在 `sync.log` 文件中，便于排查问题。

---

如有更多问题或建议，欢迎反馈与交流。 
