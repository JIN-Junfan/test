
import os
import time
import threading
import subprocess

from DToolslib import *

from system.Struct_Pyinstaller import *
from const.Const_Parameter import *
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, QTimer, QThreadPool


class ExecutorInfoStruct(QObject):
    """ 
    执行器信息结构体, 执行器包括 python.exe 和 pyinstaller.exe

    参数: 
        name (str): 执行器名称
        path (str, optional): 执行器环境路径 默认: ''
        python_path (str, optional): python路径 默认: ''
        python_version (str, optional): python版本 默认: ''
        pyinstaller_path (str, optional): pyinstaller路径 默认: ''
        pyinstaller_version (str, optional): pyinstaller版本 默认: ''

    信号: 
        signal_update_data (pyqtSignal(dict)): 更新数据信号, 如果数据更改, 则将通过信号通知其他组件

    方法: 
        set_name(name: str): 设置执行器名称
        set_path(path: str): 设置执行器环境路径
        set_python_path(python_path: str): 设置python路径
        set_python_version(python_version: str): 设置python版本
        set_pyinstaller_path(pyinstaller_path: str): 设置pyinstaller路径
        set_pyinstaller_version(pyinstaller_version: str): 设置pyinstaller版本
        clear(): 清除所有数据
        clear_pyinstaller(): 清除pyinstaller数据
    """
    signal_update_data = pyqtSignal()

    def __init__(self, name: str, path: str = '', python_path: str = '', python_version: str = '', pyinstaller_path: str = '', pyinstaller_version: str = ''):
        super().__init__()
        self.__name: str = name
        self.__path: str = path
        self.__python_path: str = python_path
        self.__python_version: str = python_version
        self.__pyinstaller_path: str = pyinstaller_path
        self.__pyinstaller_version: str = pyinstaller_version

    @property
    def name(self) -> str:
        return self.__name

    @property
    def path(self) -> str:
        return self.__path

    @property
    def python_path(self) -> str:
        return self.__python_path

    @property
    def python_version(self) -> str:
        return self.__python_version

    @property
    def pyinstaller_path(self) -> str:
        return self.__pyinstaller_path

    @property
    def pyinstaller_version(self) -> str:
        return self.__pyinstaller_version

    @property
    def info_list(self) -> list:
        return [self.__name, self.__python_path, self.__python_version, self.__pyinstaller_path, self.__pyinstaller_version]

    def __str__(self) -> str:
        return str(self.info_list)

    def set_name(self, name) -> None:
        if name == self.__name:
            return
        self.__name = name
        self.signal_update_data.emit()

    def set_path(self, path) -> None:
        if path == self.__path:
            return
        self.__path = path
        self.signal_update_data.emit()

    def set_python_path(self, python_path) -> None:
        if python_path == self.__python_path:
            return
        self.__python_path = python_path
        self.signal_update_data.emit()

    def set_python_version(self, python_version) -> None:
        if python_version == self.__python_version:
            return
        self.__python_version = python_version
        self.signal_update_data.emit()

    def set_pyinstaller_path(self, pyinstaller_path) -> None:
        if pyinstaller_path == self.__pyinstaller_path:
            return
        self.__pyinstaller_path = pyinstaller_path
        self.signal_update_data.emit()

    def set_pyinstaller_version(self, pyinstaller_version) -> None:
        if pyinstaller_version == self.__pyinstaller_version:
            return
        self.__pyinstaller_version = pyinstaller_version
        self.signal_update_data.emit()

    def clear(self) -> None:
        if self.__path == '' and self.__python_path == '' and self.__python_version == '' and self.__pyinstaller_path == '' and self.__pyinstaller_version == '':
            return
        self.__path = ''
        self.__python_path = ''
        self.__python_version = ''
        self.__pyinstaller_path = ''
        self.__pyinstaller_version = ''
        self.signal_update_data.emit()

    def clear_pyinstaller(self) -> None:
        if self.__pyinstaller_path == '' and self.__pyinstaller_version == '':
            return
        self.__pyinstaller_path = ''
        self.__pyinstaller_version = ''
        self.signal_update_data.emit()


class TaskRunner(QRunnable):
    def __init__(self, call_back_func, *args, **kwargs):
        super().__init__()
        self.__args = args
        self.__kwargs = kwargs
        self.__call_back_func = call_back_func

    def run(self):
        self.__call_back_func(*self.__args, **self.__kwargs)


class ExecutorInfoManager(QObject):
    """
    执行器信息管理类

    运行逻辑: 

    初始化时, 将获取 本地python 的信息, 包括pyinstaller, 同时获取 conda 环境列表, 并获取每个环境中的pyinstaller信息

    此后将只循环获取 conda 环境列表, 如果列表与原来的相同, 则不更新 self.__conda_struct_dict ,并获取每个环境中的pyinstaller信息

    同时对所有的 pyinstaller 进行检查, 如果存在则初始化的一段时间进行更新, 但之后的version检查则按照一段时间间隔进行

    指定的环境则通过外部调用检查, 这个部分放在UI中, 如果选定了指定的环境, 则每隔一段时间调用检查一次

    - 信号发射有节流机制，或时间大于指定时间，或请求发送次数超过最大次数，才会发送信号

    参数: 
        executor_struct_dict: 执行器信息字典

    信号: 
        signal_update_GUI: 更新GUI信号

    方法：
        set_special_env: 设置指定的环境

    """
    signal_update_GUI = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__conda_struct_dict = {}
        self.__conda_env_compare_list = ''
        self.__init_end_time = time.time()+6
        self.__pyinstaller_version_detection_interval = 10
        self.__emit_signal_interval = 1
        """ 信号发射最小时间间隔, 阻止信号高频发射 """
        self.__emit_signal_index = 0
        self.__emit_signal_index_max = 30
        """ 信号发射最小次数间隔, 阻止信号高频发射 """

        self.__local_struct = ExecutorInfoStruct(name='local')
        self.__special_struct = ExecutorInfoStruct(name='special')
        self.__thread_pool_conda = QThreadPool()
        """ 检测 conda 环境中的 pyinstaller, 由于conda环境较多, 所以单独使用线程池 """
        self.__thread_pool_conda.setMaxThreadCount(4)
        self.__thread_pool_conda.setExpiryTimeout(5000)
        self.__thread_pool_normal = QThreadPool()
        self.__thread_pool_normal.setMaxThreadCount(3)
        self.__thread_pool_normal.setExpiryTimeout(10000)
        self.__create_tast_detect_local_env()
        self.__create_tast_detect_conda_env()
        self.__timer_polling_conda = QTimer()
        self.__timer_polling_conda.timeout.connect(self.__create_task_detect_conda_polling)
        self.__timer_polling_conda.start(2000)
        self.__timer_emit_signal = threading.Timer(self.__emit_signal_interval, self.__emit_signal_update_GUI)

    @property
    def executor_struct_dict(self):
        temp = {
            'local': self.__local_struct,
            'special': self.__special_struct,
            **self.__conda_struct_dict
        }
        return temp

    def set_special_env(self, python_path: str, pyinstaller_path: str = '') -> None:
        if not os.path.exists(python_path):
            self.__special_struct.clear()
            return
        self.__create_tast_detect_special_env(python_path, pyinstaller_path)

    # @Inner_Decorators.time_counter
    def __detect_special_env(self, python_path: str, pyinstaller_path: str) -> None:
        if python_path != self.__special_struct.python_path:
            self.__special_struct.clear()
            cmdline: str = f'{python_path} --version'
            python_version_process = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            python_version: str = python_version_process.stdout.read().strip().lower().replace('python ', '')
            self.__special_struct.set_path(os.path.dirname(python_path))
            self.__special_struct.set_python_path(python_path)
            self.__special_struct.set_python_version(python_version)
        self.__detect_pyinstaller(self.__special_struct, pyinstaller_path)

    # @Inner_Decorators.time_counter
    def __detect_local_python(self) -> None:
        """
        用于获取本地 python 路径和版本

        self.__local_struct 将会自动更新, 更新内容为 `path`, `python_path`, `python_version`
        """
        cmdline: str = f'where python'
        python_path_process = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        python_path: str = python_path_process.stdout.read().strip().split('\n')[0]
        cmdline: str = f'{python_path} --version'
        python_version_process = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        python_version: str = python_version_process.stdout.read().strip().lower().replace('python ', '')
        python_folder_path: str = os.path.dirname(python_path)
        self.__local_struct.clear()
        self.__local_struct.set_path(python_folder_path)
        self.__local_struct.set_python_path(python_path)
        self.__local_struct.set_python_version(python_version)
        self.__detect_pyinstaller(self.__local_struct)
        return

    # @Inner_Decorators.time_counter
    def __detect_conda_env(self) -> None:
        """
        用于检测当前conda环境列表, 包含对python路径的检测

        self.__conda_struct_dict 将会自动更新, 其内元素 struct 赋值内容为 `path`, `python_path`, `python_version`
        """
        cmdline: str = f'conda env list'
        conda_env_list_process = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        conda_env_list: list = conda_env_list_process.stdout.read().strip().replace('*', '').split('\n')
        if conda_env_list == self.__conda_env_compare_list:
            # 如果没有变化, 则直接返回, 避免重复检测
            return
        add_list, del_list = self.__compare_list(self.__conda_env_compare_list, conda_env_list)
        self.__conda_env_compare_list: list = conda_env_list
        flag_del = False
        flag_add = False

        # 删除环境
        for env in del_list:
            env: str
            if env.startswith('#'):
                continue
            env_name, env_path = env.split()
            if env_name in self.__conda_struct_dict:
                del self.__conda_struct_dict[env_name]
                flag_del = True

        # 添加环境
        for env in add_list:
            env: str
            if env.startswith('#'):
                continue
            env_name, env_path = env.split()
            struct = ExecutorInfoStruct(name=env_name, path=env_path)
            struct.signal_update_data.connect(self.__schedule_signal_update_GUI)
            self.__conda_struct_dict[env_name] = struct
            flag_add = True
            self.__detect_conda_python_path(struct)

        # 通知外部更新
        if flag_add or flag_del:
            self.__schedule_signal_update_GUI()

        return

    # @Inner_Decorators.time_counter
    def __detect_conda_python_path(self, struct: ExecutorInfoStruct) -> None:
        """
        检测conda环境下的python路径, 并设置到 struct 中. 修改值 `python_path`, `python_version`
        """
        python_path = ''
        if App.OS == OsType.WINDOWS:
            python_path = os.path.join(struct.path, 'python.exe')
        elif App.OS == OsType.LINUX or App.OS == OsType.MACOS:
            python_path = os.path.join(struct.path, 'python.exe')
        if not python_path:
            return
        cmdline: str = f'{python_path} --version'
        python_version_process = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        python_version: str = python_version_process.stdout.read().strip().lower().replace('python ', '')
        struct.set_python_path(python_path)
        struct.set_python_version(python_version)
        return

    # @Inner_Decorators.time_counter
    def __detect_pyinstaller(self, struct: ExecutorInfoStruct, pyinstaller_path: str = '') -> None:
        """
        检查 pyinstaller 是否存在, 如果存在则设置路径和版本, 项目修改值 `pyinstaller_path`, `pyinstaller_version`

        参数:
            struct: ExecutorInfoStruct 对象
            pyinstaller_path: pyinstaller 可执行文件路径, 改参数主要是给 special_struct 用的
        """
        if not struct.python_path:
            struct.clear()
            return
        current = os.path.dirname(struct.python_path)
        current_path = os.path.join(current, 'pyinstaller.exe')
        current_bin_path = os.path.join(current, 'bin', 'pyinstaller.exe')
        current_script_path = os.path.join(current, 'Scripts', 'pyinstaller.exe')
        parent = os.path.dirname(current)
        parent_path = os.path.join(parent, 'pyinstaller.exe')
        parent_bin_path = os.path.join(parent, 'bin', 'pyinstaller.exe')
        parent_script_path = os.path.join(parent, 'Scripts', 'pyinstaller.exe')
        if (
            pyinstaller_path and isinstance(pyinstaller_path, str) and
            os.path.exists(pyinstaller_path)
        ):
            pyinstaller_path = pyinstaller_path
        elif os.path.exists(current_path):
            pyinstaller_path = current_path
        elif os.path.exists(current_bin_path):
            pyinstaller_path = current_bin_path
        elif os.path.exists(current_script_path):
            pyinstaller_path = current_script_path
        elif os.path.exists(parent_path):
            pyinstaller_path = parent_path
        elif os.path.exists(parent_bin_path):
            pyinstaller_path = parent_bin_path
        elif os.path.exists(parent_script_path):
            pyinstaller_path = parent_script_path
        current_time = int(time.time())
        if pyinstaller_path == '':
            struct.clear_pyinstaller()
            return
        if current_time % self.__pyinstaller_version_detection_interval != 0 and current_time > self.__init_end_time:
            return
        cmdline: str = f'{struct.python_path} -m PyInstaller --version'
        pyinstaller_version_process = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        pyinstaller_version: str = pyinstaller_version_process.stdout.read().strip()
        if 'No module' in pyinstaller_version:
            pyinstaller_version = ''
        struct.set_pyinstaller_path(pyinstaller_path)
        struct.set_pyinstaller_version(pyinstaller_version)

    def __create_tast_detect_local_env(self) -> None:
        """
        用于检测本地 python 环境, 任务在线程池中执行 self.__thread_pool_normal
        """
        task = TaskRunner(self.__detect_local_python)
        self.__thread_pool_normal.start(task)

    def __create_tast_detect_special_env(self, python_path: str, pyinstaller_path: str) -> None:
        """
        用于检测指定 python 环境, 任务在线程池中执行 self.__thread_pool_normal
        """
        task = TaskRunner(self.__detect_special_env, python_path, pyinstaller_path)
        self.__thread_pool_normal.start(task)

    def __create_tast_detect_conda_env(self) -> None:
        """
        用于创建检查 conda 环境任务, 任务在线程池中运行 self.__thread_pool_normal
        """
        task = TaskRunner(self.__detect_conda_env)
        self.__thread_pool_normal.start(task)

    def __create_task_detect_conda_pyinstaller(self) -> None:
        """
        用于创建检查 conda 中 pyinstaller 的任务, 任务在线程池中运行 self.__thread_pool_conda
        """
        task_list = [TaskRunner(self.__detect_pyinstaller, struct) for struct in self.__conda_struct_dict.values()]
        for task in task_list:
            self.__thread_pool_conda.start(task)

    def __create_task_detect_pyinstaller_polling(self) -> None:
        """
        用于创建检查所有环境中 pyinstaller 的任务, 任务在线程池中运行 self.__thread_pool_normal
        """
        task_list = [TaskRunner(self.__detect_pyinstaller, struct) for struct in self.executor_struct_dict.values()]
        for task in task_list:
            self.__thread_pool_conda.start(task)

    def __create_task_detect_conda_polling(self) -> None:
        """
        用于创建conda检查路径任务, 任务在线程池中运行 self.__thread_pool_conda
        """
        self.__create_tast_detect_conda_env()
        self.__create_task_detect_pyinstaller_polling()

    def __compare_list(self, list_old, list_new) -> tuple:
        """
        比较两个列表, 返回新增和删减的元素

        参数:
            list_old(list): 旧列表
            list_new(list): 新列表

        返回:
            add_list(list): 新增的元素
            del_list(list): 删减的元素
        """
        old_set = set(list_old)
        new_set = set(list_new)
        del_list = [item for item in list_old if item not in new_set]
        add_list = [item for item in list_new if item not in old_set]
        return add_list, del_list

    def __schedule_signal_update_GUI(self):
        if self.__timer_emit_signal.is_alive() or self.__emit_signal_index < self.__emit_signal_index_max:
            self.__timer_emit_signal.cancel()
            self.__emit_signal_index += 1
        if self.__emit_signal_index >= self.__emit_signal_index_max:
            self.__emit_signal_update_GUI()
        self.__timer_emit_signal = threading.Timer(self.__emit_signal_interval, self.__emit_signal_update_GUI)
        self.__timer_emit_signal.start()

    def __emit_signal_update_GUI(self):
        self.__emit_signal_index = 0
        self.__timer_emit_signal.cancel()
        self.signal_update_GUI.emit()
