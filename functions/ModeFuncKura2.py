import os
import pyautogui
import cv2
from functions.setGUI import setGUI
from functions.common import PlaySound, CheckTappedArea, CheckComplete
from functions.DesignLayout import make_fullimage_layout
from ModeFuncBase import getDefaultAreaDefinition


def updateDictProc_Kura2(dictProc):
	dictProc_this = {
		"KURA2_Q"			: procKura2_Q,
		"KURA2_MOVIE_PROC"	: procKura2_Movie,
		"KURA2_POSE_PROC"	: procKura2_ImageProc,
		"KURA2_CORRECT"      : procKura2_correct,
		"KURA2_CLEAR"        : procKura2_clear
	}
	return dict(dictProc, **dictProc_this)

# レイアウト設定・辞書割り当て =============================================
def updateDictWindow_Labo(dictWindow):
	layoutKura2_Q = make_fullimage_layout('png/lab_q.png',"KURA2_Q")
	layoutKura2_Correct = make_fullimage_layout('png/lab_a.png',"KURA2_CORRECT")
	layoutLabo_Clear = make_fullimage_layout('png/lab_i.png',)

	dictLayout = {
		"KURA2_Q"			: layoutKura2_Q,
		"KURA2_MOVIE_PROC"	: 'None',
		"KURA2_POSE_PROC"	: 'None',
		"KURA2_CORRECT"      : layoutKura2_Correct,
		"LABO_CLEAR"        : layoutLabo_Clear
	}
	dictWindow_this = setGUI(dictLayout)

	return dict(dictWindow, **dictWindow_this)

def procKura2_Q(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]

	if event == "次へ":
		sStartTime = cState.updateState("KURA2_POSE_PROC")
		dictArgument["Start time"] = sStartTime

def procKura2_Movie(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	proc = dictArgument["ImageProc"]

	# if os.name != 'nt':
	# 	result = subprocess.call(['mplayer', '-fs', './suitoOsaka_ver4.mp4'])

	proc.createWindows()
	proc.defineCorrectPose()
	sStartTime = cState.updateState("KURA2_POSE_PROC")
	dictArgument["Start time"] = sStartTime

def procKura2_ImageProc(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]
	proc = dictArgument["ImageProc"]

	if event == "KURA2_Q":
		vPosition = pyautogui.position()
		listArea = getDefaultAreaDefinition()
		sTappedArea = CheckTappedArea(vPosition, listArea)

		if sTappedArea == 0:
			isFound = proc.execute()
			cv2.waitKey(1)

			print("isFound",isFound)

			if isFound is True:
				PlaySound("sound/correct.wav")

				cCtrlCard.write_result("pose", "T")

				sStartTime = cState.updateState("KURA2_CORRECT")
				dictArgument["Start time"] = sStartTime

				proc.closeWindows()

def procKura2_correct(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]

	# if CheckComplete(cCtrlCard):
	# 	#sStartTime = cState.updateState("CLEAR1")
	# 	cCtrlCard.write_result("clear_game", "T")  # ゲームクリア済みであることを記録

	if event == "次へ":
		sStartTime = cState.updateState("LABO_CLEAR")
		dictArgument["Start time"] = sStartTime

def procKura2_clear(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]

	if event == "次へ":
		sStartTime = cState.updateState("SELECT_GAME")

		dictArgument["Start time"] = sStartTime

		# # ラボをクリアしたのでプレイできないように設定
		# cState.dictWindow["SELECT_GAME"]["ラボ"].update(disabled=True)
