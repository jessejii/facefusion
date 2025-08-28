import os
import gradio
from typing import List, Optional
from facefusion import state_manager, wording
from facefusion.uis.core import register_ui_component

TMP_FILES_LIST: Optional[gradio.Files] = None
REFRESH_BUTTON: Optional[gradio.Button] = None  # 添加全局变量


def get_tmp_files() -> List[str]:
	tmp_path = state_manager.get_item('temp_path')
	out_path = os.path.join(tmp_path, 'out')  # 获取out文件夹的路径
	files = []

	# 确保out文件夹存在，如果不存在则创建
	if not os.path.exists(out_path):
		os.makedirs(out_path)  # 创建out文件夹

	# 遍历out文件夹中的所有文件
	for root, dirs, filenames in os.walk(out_path):
		for filename in filenames:
			# 确保返回完整路径
			full_path = os.path.join(root, filename)
			if os.path.isfile(full_path):  # 确保是文件
				files.append(full_path)

	return files




def render() -> None:
	global TMP_FILES_LIST, REFRESH_BUTTON

	# 初始化时获取文件列表
	files = get_tmp_files()

	# 添加刷新按钮
	REFRESH_BUTTON = gradio.Button("刷新临时文件")

	TMP_FILES_LIST = gradio.File(
		label="临时文件列表",
		value=files,
		file_count="multiple",
		interactive=True,
		visible=True
	)

	register_ui_component('tmp_files_list', TMP_FILES_LIST)
	register_ui_component('refresh_button', REFRESH_BUTTON)


def listen() -> None:
	def refresh_files():
		files = get_tmp_files()
		# 返回文件列表而不是直接更新
		return files

	REFRESH_BUTTON.click(
		fn=refresh_files,  # 使用新的刷新函数
		inputs=None,
		outputs=[TMP_FILES_LIST]
	)
