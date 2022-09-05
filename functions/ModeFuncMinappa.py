import pyautogui
from functions.setGUI import setGUI
from functions.common import PlaySound, CheckTappedArea, CheckComplete
from functions.DesignLayout import make_fullimage_layout

listFound = [1, 0, 0]

# 処理の辞書割り当て ======================================================
def updateDictProc_Minappa(dictProc):
	dictProc_this = {
		"MINAPPA_Q1"		: procMinappa_Q1,
		"MINAPPA_Q2"		: procMinappa_Q2,
		"MINAPPA_CORRECT1"	: procMinappa_Correct1,
		"MINAPPA_CORRECT2"	: procMinappa_Correct2,
		"MINAPPA_CORRECT3"	: procMinappa_Correct3,
		"MINAPPA_CLEAR"		: procMinappa_Clear,
	}
	return dict(dictProc, **dictProc_this)


# レイアウト設定・辞書割り当て =============================================
def updateDictWindow_Minappa(dictWindow):
	layoutMinappa_Q1 = make_fullimage_layout("images/kurawanka1-01.png", "MINAPPA_Q1")
	layoutMinappa_Q2 = make_fullimage_layout("images/kurawanka1-02.png", "MINAPPA_Q2")
	layoutMinappa_Correct1 = make_fullimage_layout("images/kurawanka1-03.png", "MINAPPA_CORRECT1")
	layoutMinappa_Correct2 = make_fullimage_layout("images/kurawanka1-04.png", "MINAPPA_CORRECT2")
	layoutMinappa_Correct3 = make_fullimage_layout("images/kurawanka1-05.png", "MINAPPA_CORRECT3")
	layoutMinappa_Clear = make_fullimage_layout("images/kurawanka1-06.png", "MINAPPA_CLEAR")

	dictLayout = {
		"MINAPPA_Q1"		: layoutMinappa_Q1,
		"MINAPPA_Q2"		: layoutMinappa_Q2,
		"MINAPPA_CORRECT1"	: layoutMinappa_Correct1,
		"MINAPPA_CORRECT2"	: layoutMinappa_Correct2,
		"MINAPPA_CORRECT3"	: layoutMinappa_Correct3,
		"MINAPPA_CLEAR"		: layoutMinappa_Clear,
	}
	dictWindow_this = setGUI(dictLayout)

	return dict(dictWindow, **dictWindow_this)


# Minappa_Q2モードタッチ座標設定 ========================================
def getAreaDefinition_Q2():
	vArea0 = [70, 250, 130, 100]
	vArea1 = [545, 345, 70, 60]
	vArea2 = [605, 200, 110, 95]
	listArea = [vArea0, vArea1, vArea2]

	return listArea


# 「次へ」ボタンタッチ座標設定 =========================================
def getDefaultAreaDefinition():
	vArea0 = [260, 520, 520, 60]
	listArea = [vArea0,]

	return listArea


# Minappa_Q1モード処理 =================================================
def procMinappa_Q1(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]
	vPosition = pyautogui.position()
	listArea = getDefaultAreaDefinition()
	sTappedArea = CheckTappedArea(vPosition, listArea)

	if  event == "MINAPPA_Q1":
		if sTappedArea == 0:
			sStartTime = cState.updateState("MINAPPA_Q2")
			dictArgument["Start time"] = sStartTime


# Minappa_Q2モード処理 =================================================
def procMinappa_Q2(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]

	if event == "MINAPPA_Q2":
		vPosition = pyautogui.position()
		listArea = getAreaDefinition_Q2()
		sTappedArea = CheckTappedArea(vPosition, listArea)
		print(sTappedArea)
		print(listFound)

		if sTappedArea == 0:
			PlaySound("sound/correct.wav")
			listFound[0] = 1
			sStartTime = cState.updateState("MINAPPA_CORRECT1")
			dictArgument["Start time"] = sStartTime
		elif sTappedArea == 1:
			PlaySound("sound/correct.wav")
			listFound[1] = 1
			sStartTime = cState.updateState("MINAPPA_CORRECT2")
			dictArgument["Start time"] = sStartTime
		elif sTappedArea == 2:
			PlaySound("sound/correct.wav")
			listFound[2] = 1
			sStartTime = cState.updateState("MINAPPA_CORRECT3")
			dictArgument["Start time"] = sStartTime
		else:
			PlaySound("sound/wrong.wav")


# Minappa_correct1モード処理 ======================================================
def procMinappa_Correct1(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]

	if event == "MINAPPA_CORRECT1":
		vPosition = pyautogui.position()
		listArea = getDefaultAreaDefinition()
		sTappedArea = CheckTappedArea(vPosition, listArea)

		if sTappedArea == 0:
			if listFound == [1, 1, 1]:
				sStartTime = cState.updateState("MINAPPA_CLEAR")
				dictArgument["Start time"] = sStartTime
			else:
				sStartTime = cState.updateState("MINAPPA_Q2")
				dictArgument["Start time"] = sStartTime


# Minappa_correct2モード処理 ======================================================
def procMinappa_Correct2(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]

	if event == "MINAPPA_CORRECT2":
		vPosition = pyautogui.position()
		listArea = getDefaultAreaDefinition()
		sTappedArea = CheckTappedArea(vPosition, listArea)

		if sTappedArea == 0:
			if listFound == [1, 1, 1]:
				sStartTime = cState.updateState("MINAPPA_CLEAR")
				dictArgument["Start time"] = sStartTime
			else:
				sStartTime = cState.updateState("MINAPPA_Q2")
				dictArgument["Start time"] = sStartTime


# Minappa_correct3モード処理 ======================================================
def procMinappa_Correct3(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]

	if event == "MINAPPA_CORRECT3":
		vPosition = pyautogui.position()
		listArea = getDefaultAreaDefinition()
		sTappedArea = CheckTappedArea(vPosition, listArea)

		if sTappedArea == 0:
			if listFound == [1, 1, 1]:
				sStartTime = cState.updateState("MINAPPA_CLEAR")
				dictArgument["Start time"] = sStartTime
			else:
				sStartTime = cState.updateState("MINAPPA_Q2")
				dictArgument["Start time"] = sStartTime


# Minappa_clearモード処理 ========================================================
def procMinappa_Clear(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]

	if event == "MINAPPA_CLEAR":
		vPosition = pyautogui.position()
		listArea = getDefaultAreaDefinition()
		sTappedArea = CheckTappedArea(vPosition, listArea)

		if sTappedArea == 0:
			sStartTime = cState.updateState("SELECT_GAME")
			dictArgument["Start time"] = sStartTime
			cState.dictWindow["SELECT_GAME"]["くらわんか舟１"].update(disabled=True)
			cCtrlCard.write_result("minappa", "T")
