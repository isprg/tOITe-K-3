# ライブラリ等のインポート ==============================================
import pyautogui
import yaml
import os

from functions.ModeFuncBase import *
from functions.ModeFuncMinappa import *
from functions.ModeFuncPose import *
from functions.CardFunc import *
from functions.common import getDictFlag
from Classes.ClsCtrlStateAndWindow import ClsCtrlStateAndWindow

if os.name == 'nt':
	from Classes.ClsCtrlCardDummy import ClsCtrlCard
else:
	from Classes.ClsCtrlCard import ClsCtrlCard
	from functions.AdminMode import AdminMode

import sys
sys.path.append("./Classes")
from ClsImageProcessPose import ClsImageProcessPose


# 環境設定 =============================================================
def setEnvironment():
	if os.name == 'nt':
		strPlatform = "WIN"
	else:
		strPlatform = "JETSON"

	sCameraNumber = 0
	sSensorWidth = 640
	sSensorHeight = 360
	sMonitorWidth = 1024
	sMonitorHeight = 600
	tplWindowName = ("full",)
	sFlipMode = 2

	proc = ClsImageProcessPose(
		strPlatform,
		sCameraNumber,
		sSensorWidth,
		sSensorHeight,
		sMonitorWidth,
		sMonitorHeight,
		tplWindowName,
		sFlipMode,
	)

	return proc


# モード別設定 =============================================================
def setModeFuncsAndLayouts(blDebug):
	dictWindow = createDictWindow()
	dictWindow = updateDictWindow_Minappa(dictWindow)
	dictWindow = updateDictWindow_Pose(dictWindow)

	if blDebug == False:
		for sKey in dictWindow:
			window = dictWindow[sKey]
			if window != "None":
				window.set_cursor("none")

	cState = ClsCtrlStateAndWindow("STANDBY", "BACKGROUND", dictWindow)

	dictProc = createDictProc()
	dictProc = updateDictProc_Minappa(dictProc)
	dictProc = updateDictProc_Pose(dictProc)

	dictFlag = getDictFlag()

	return cState, dictProc, dictFlag


# メインスレッド =======================================================
def mainThread():
	blDebug = True
	proc = setEnvironment()
	cState, dictProc, dictFlag = setModeFuncsAndLayouts(blDebug)
	cCtrlCard = ClsCtrlCard(dictFlag)

	listFlags = list(dictFlag.keys())
	print(listFlags[0])
	

	# 管理者カードの一覧を取得
	with open("files/Admin_CardID_list.yaml", "r") as f:
		card_ID_list = yaml.safe_load(f)["card_ID"]

	dictArgument = {
		"State"			: cState,
		"CtrlCard"		: cCtrlCard,
		"ImageProc"		: proc,
		"Event"			: None,
		"Values"		: None,
		"Frame"			: 0,
		"Start time"	: 0,
		"Return state"	: None,  # カードエラーからの復帰位置
		"Option"		: [0, 0, 0, 0, 0],
		"Complete"		: 0,
	}

	# 無限ループ ----------------------------------------
	while True:
		if dictArgument["Complete"] == 1:
			break

		# フレームを記録
		dictArgument["Frame"] = (dictArgument["Frame"] + 1) % 1000

		# 現在のステートを確認
		currentState = cState.getState()

		if cState.dictWindow[currentState] != "None":
			# ウィンドウからイベントを受信
			event, values = cState.readEvent()
			dictArgument["Event"] = event
			dictArgument["Values"] = values
			
			if event != "-timeout-":
				print(event)

			if blDebug == False:
				pyautogui.moveTo(1, 1)

		if currentState != "CARD_ERROR" and currentState != "STANDBY":
			# カードの状態をチェック
			currentState = CheckCard(dictArgument)  # カードの存在と同一性をチェック
			admin_mode_flag, Admin_CardID = AdminFlag_fromCard(
				cCtrlCard, card_ID_list
			)  # ゲーム終了用のカードかをチェック

			if admin_mode_flag:
				print("Enter to Admin Mode")
				break

		dictProc[currentState](dictArgument)

	cCtrlCard.Finalize()
	proc.Finalize()
	cState.Finalize()

	return Admin_CardID


# メイン関数 =================================================
if __name__ == "__main__":
	while True:
		Admin_CardID = mainThread()
		#adminCommand = AdminMode(Admin_CardID)

		if os.name == 'nt':
			adminCommand = "end"

		if adminCommand == "end":
			break
