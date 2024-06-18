from cx_Freeze import setup, Executable

# 创建可执行文件的配置
executableApp = Executable(
    script="app.py",
    target_name="leiSuoNaSiAService",
)
include_files = [r"./resource"]
# 打包的参数配置
options = {
    "build_exe": {
        "packages": ["maafw", "flask", "nicegui"],
        "build_exe": "./dist/",
        "excludes": [],
        "include_files": include_files,
        "optimize": 2,
    }
}

setup(
    name="leiSuoNaSiAService",
    version="1.0",
    description="MaaPythonApi",
    options=options,
    executables=[executableApp]
)
