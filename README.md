# QQ-_MealAlter_Bot
A bot to forward the QQ message to user,then send it to your bot.

Meal_Alter_Bot 项目是基于 [https://github.com/Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 项目进行开发的QQ机器人，通过监控聊天信息，获取干饭通知，通过 ESP32 Wi-Fi 通信功能，控制设备进行蜂鸣器提醒。

其主要的功能实现来源于 [https://github.com/Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 项目所开发的机器人，该程序能够通过模拟登录自己的 QQ 帐号，将其作为机器人，对 QQ 的各种消息和提醒进行监控于处理，还能将其给进一步发送出去，实现了 QQ 不开源，不开放 API 状态下的开放功能。（当然，此项目可能违反 Tencent 相关用户协议，存在封号可能，不建议将大号作为机器人）

在将 QQ 所获取的消息进行监控后，通过 Python 功能便携 Flask 应用，实现对于 QQ 消息的实时监控，并二次筛选处自己所需要的内容，进而通过 MQTT 协议，发送的执行器，进行设备的控制。

## 所需环境：Python3

## 机器人搭建

指的是将自己的 QQ 作为机器人部署在服务器或个人电脑上

（支持 Win/Linux ）

这里采用的框架和应用是 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)，是当下为数不多可供使用的 QQ 机器人（Tencent封杀使其越来越封闭）

### 新建文件夹，并进入对应目录

### 下载相应文件：

Linux 下通过命令行，下载合适的安装包到自己的机器上

`wget https://github.com.cnpmjs.org/Mrs4s/go-cqhttp/releases/download/v1.0.0-beta4/go-cqhttp_linux_amd64.tar.gz`

而 Windows 用户可以直接在浏览器上进行下载，[下载地址](https://github.com/Mrs4s/go-cqhttp/releases/tag/v1.0.0-rc1) 

注意区分不同版本（Linux 也可以由用户下载好之后，直接上传到服务器上）

### 解压文件

Linux 下命令如下

`tar -zxvf go-cqhttp_linux_amd64.tar.gz`

Win 下请按照自己的解压工具进行解压

### 授权

Linux 下命令如下

`chmod +x go-cqhttp`

Win 下建议使用管理员权限 打开 go-cqhttp

### 初始化程序

当然，现在还不需要去打开运行，我们可以先打开 config.yml 文件，进行配置

如果没有运行过 go-cqhttp 是没有此文件的，可采用本 Github 所提供的文件进行配置。

需要配置的内容不多，本项目只更改了

- 第四五行的QQ帐号（纯数字即可），密码（注意单引号）
- 倒数第八行的 URL 地址，将端口发送到 127.0.0.1:10001 进行通信

用户可以直接第一次运行程序后，自行进行修改上述内容进行应用。

如果不添加QQ帐号和密码到 config.yml 文件中，第一次登录后 会使用扫码登录，但是我使用此选项失败了~

接下来就是第一次运行程序，进行初始化了

Linux 下通过该命令打开

`./go-cqhttp`

如果是第一次打开，会让你选择采用什么方式运行，这里选择 http 也就是 1 即可

等待其配置完成

就会自动转发 信息到接口处

此时使用 Ctrl + c 便可以关闭程序。

### 运行 Python程序

Python 的环境要求是 Python3

首先，打开 app.py ，进行修改

这里需要修改的也就是自己的 MQTT 服务器地址和所需要修改的关键词，过滤的群号，详见文件内注释说明。

在运行之前，我们还需要安装 Python 的相关库，这里用到了 paho.mqtt 和 flask 

首先采用 

```bash
pip3 install paho.mqtt 
```

```bash
pip3 install flask
```

配置完成后，可以使用 python3 app.py 即可运行，该程序便会将需要的转发的内容发送到MQTT服务器的对应主题上。

在服务器上，我们往往采用 SSH 的方式进行连接，为避免关闭界面后，运行停止，我们可以采用命令nohup ~ &将其挂起,

即使用 

```bash
nohup ./go-cqhttp &
nohup python3 app.py &
```

 其对应的终端输入日志将保存在.out文件中

### 配置 ESP32

准备一个 ESP32 开发板，正常的型号就可以，这里仅仅采用了 WiFi，运用了 MQTT 的库文件，详细代码参考 本项目中的 ESP32_Meal_Alter_Bot 文件夹中的内容即可。

本 ESP32 项目采用 Vscode +platformio 进行开发

用户可以自行将 ESP32_Meal_Alter_Bot/src 中的主程序复制到 Arduino 程序中进行开发，对于 ESP32 的相关环境配置，网络中已经有很多，不再赘述，请善用百度。

对于 ESP32 的功能和代码修改介绍：
该开发板所控制的外部设备有且仅有一个，就是蜂鸣器，通过及其简单的高低电平使其发声，预警提醒。
在代码中，首先修改前面的 Wi-Fi 帐号密码，其次是 MQTT 服务器的地址，需要与上述一致。
在本代码中，用户可以进一步的通过 ESP32 的代码修改，进行二次过滤关键词，也可以修改不同的 MQTT 主题，进行应用。

将ESP32 代码进行编译烧录后进行上传，在测试成功后，即可正常使用。