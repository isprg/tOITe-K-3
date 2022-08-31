import cv2
import subprocess
import os
from functions.setGUI import setGUI
from functions.common import Check_Clear, PlaySound
from functions.DesignLayout import make_4choice_layout


# 処理の辞書割り当て ======================================================
def updateDictProc_Labo(dictProc):
	dictProc_this = {
		"LABO_Q"			: procLabo_Q,
		"LABO_MOVIE_PROC"	: procLabo_Movie,
		"LABO_POSE_PROC"	: procLabo_ImageProc,
		"LABO_CORRECT"      : procLabo_correct,
		"LABO_CLEAR"        : procLabo_clear
	}
	return dict(dictProc, **dictProc_this)


# レイアウト設定・辞書割り当て =============================================
def updateDictWindow_Labo(dictWindow):
	layoutLabo_Q = make_4choice_layout('png/lab_q.png',["", "", "", "次へ"])
	layoutLabo_Correct = make_4choice_layout('png/lab_a.png',["", "", "", "次へ"])
	layoutLabo_Clear = make_4choice_layout('png/lab_i.png',["", "", "", "次へ"])

	dictLayout = {
		"LABO_Q"			: layoutLabo_Q,
		"LABO_MOVIE_PROC"	: 'None',
		"LABO_POSE_PROC"	: 'None',
		"LABO_CORRECT"      : layoutLabo_Correct,
		"LABO_CLEAR"        : layoutLabo_Clear
	}
	dictWindow_this = setGUI(dictLayout)

	return dict(dictWindow, **dictWindow_this)


# labo_Qモード処理 ======================================================
def procLabo_Q(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]

	if event == "次へ":
		sStartTime = cState.updateState("LABO_MOVIE_PROC")
		dictArgument["Start time"] = sStartTime


def procLabo_Movie(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	proc = dictArgument["ImageProc"]
	
	if os.name != 'nt':
		result = subprocess.call(['mplayer', '-fs', './suitoOsaka_ver4.mp4'])

	proc.createWindows()
	proc.defineCorrectPose("result_pose/guriko_pose.jpg")
	sStartTime = cState.updateState("LABO_POSE_PROC")
	dictArgument["Start time"] = sStartTime


# labo_ImageProcモード処理 ======================================================
def procLabo_ImageProc(dictArgument):
	cState = dictArgument["State"]
	sFrame = dictArgument["Frame"]
	proc = dictArgument["ImageProc"]
	cCtrlCard = dictArgument["CtrlCard"]

	isFound = proc.execute()
	cv2.waitKey(1)

	print("isFound",isFound)
	# print("sCountFound",sCountFound)
	# print("sFrame",sFrame)

	if isFound is True:
		PlaySound("sound/correct.wav")

		cCtrlCard.write_result("labo", "T")

		sStartTime = cState.updateState("LABO_CORRECT")
		dictArgument["Start time"] = sStartTime

		proc.closeWindows()


# labo_correctモード処理　======================================================
def procLabo_correct(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]
	
	if Check_Clear(cCtrlCard):
		#sStartTime = cState.updateState("CLEAR1")
		cCtrlCard.write_result("clear_game", "T")  # ゲームクリア済みであることを記録

	if event == "次へ":
		sStartTime = cState.updateState("LABO_CLEAR")
		dictArgument["Start time"] = sStartTime

# labo_clearモード処理　======================================================
def procLabo_clear(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]

	if event == "次へ":
		if Check_Clear(cCtrlCard):
			sStartTime = cState.updateState("CLEAR1")
		#   cCtrlCard.write_result("clear_game", "T")  # ゲームクリア済みであることを記録
		else:
			sStartTime = cState.updateState("SELECT_GAME")

		dictArgument["Start time"] = sStartTime

		# ラボをクリアしたのでプレイできないように設定
		cState.dictWindow["SELECT_GAME"]["ラボ"].update(disabled=True)
