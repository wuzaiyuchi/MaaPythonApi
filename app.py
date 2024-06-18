from flask import Flask, request, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
from maafw import maafw

# python -m pip install maafw
from maa.resource import Resource
from maa.controller import AdbController
from maa.instance import Instance
from maa.toolkit import Toolkit
from pathlib import Path

maa_inst = Instance()
import asyncio


async def maaInit():
    user_path = "./"
    Toolkit.init_option(user_path)

    resource = Resource()
    await resource.load(r"./resource")

    device_list = await Toolkit.adb_devices()
    if not device_list:
        print("No ADB device found.")
        exit()

    # for demo, we just use the first device
    device = device_list[0]
    controller = AdbController(
        adb_path=device.adb_path,
        address=device.address,
    )

    await controller.connect()
    global maa_inst
    maa_inst.bind(resource, controller)

    # maa_inst.register_action("MyAct", my_act)

    if not maa_inst.inited:
        print("Failed to init MAA.")
        exit()
    test1 = await maa_inst.run_task("初始化点击")
    print(test1)

    test2 = await maa_inst.run_recognition("初始化点击")
    print(test2)
    # return test2
    return str(test2.detail)

    # maa_inst.register_recognizer("MyRec", my_rec)


@app.route('/test', methods=["POST"])
def test():
    return asyncio.run(maaInit())


# 暂停接口运行
@app.route('/stopTask', methods=["POST"])
def stop():
    asyncio.run(runStop())
    return 'ok'


async def runStop():
    await maafw.stop_task()


@app.route('/runTask', methods=["POST"])
def runTask():
    q_data = request.get_data()  # 接收json数据
    data = json.loads(q_data)  # json数据解析
    taskId = data["taskId"]

    # target = data["param"]

    # resp= asyncio.run(run_task(taskId,target))
    resp = asyncio.run(run_task(taskId))

    # if resp is None:
    #     return str(resp)
    # else:
    #     if (taskId == '幅度'):
    #         return resp.node_details[0].recognition.detail
    #     else:
    return str(resp)




async def run_task(taskId):
    return await maafw.run_task(taskId)


 #加载 resource 目录下面的资源
@app.route('/loadResource', methods=["POST"])
def loadResource():
    q_data = request.get_data()  # 接收json数据
    data = json.loads(q_data)  # json数据解析
    resourcePath = data["resourcePath"]
    # resourcePath="D://dev//leisuonasi//maa-api//resource"
    # print(resourcePath)
    # print(resourcePath)
    # respMsg= asyncio.run(load_resource(resourcePath))
    respMsg = asyncio.run(load_resource(resourcePath))
    return str(respMsg)


async def load_resource(resourcePath):
    return await maafw.load_resource(Path(resourcePath))


# 查询当前电脑 连接的模拟器
@app.route('/queryAppHost', methods=["POST"])
def queryAppHost():
    options = asyncio.run(all_adb_detect())
    # /返回数据 需要 重新 JSON.parse(JSON.stringify(response.data));
    return options


async def all_adb_detect():
    devices = await maafw.detect_adb()
    options = []
    # 不满意格式 可以自己处理
    for d in devices:
        # v = (d.adb_path, d.address)
        # l = d.name + " " + d.address
        options.append({"adbPath": str(d.adb_path), "host": d.address})

    return options


# 连接需要端口和路径
@app.route('/connectApp', methods=["POST"])
def connectApp():
    # asyncio.run(maaInit())
    q_data = request.get_data()  # 接收json数据
    data = json.loads(q_data)  # json数据解析
    adbPath = data["adbPath"]
    adbIpHost = data["adbIpHost"]
    respMsg = asyncio.run(connect_adb(adbPath, adbIpHost))

    asyncio.run(load_resource(r"./resource"))

    # resource = Resource()
    # await resource.load(r"./resource")
    return jsonify(respMsg)


async def connect_adb(adbPath, adbIpHost):
    return await maafw.connect_adb(Path(adbPath), adbIpHost)


if __name__ == '__main__':
    app.run(port=5000)
