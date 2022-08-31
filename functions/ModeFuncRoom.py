from functions.setGUI import setGUI
from functions.common import Check_Clear, PlaySound
from functions.DesignLayout import make_4choice_layout


# 処理の辞書割り当て ======================================================
def updateDictProc_Room(dictProc):
	dictProc_this = {
		"ROOM_PRE"			: procRoom_pre,
		"ROOM_HINT"	        : procRoom_hint,
		"ROOM_Q"	        : procRoom_Q,
		"ROOM_CORRECT"      : procRoom_correct,
		"ROOM_CLEAR"        : procRoom_clear
	}
	return dict(dictProc, **dictProc_this)


# レイアウト設定・辞書割り当て =============================================
def updateDictWindow_Room(dictWindow):
	layoutRoom_Pre = make_4choice_layout('png/roo_q1.png',["", "", "ヒント", "次へ"])
	layoutRoom_Hint = make_4choice_layout('png/roo_h.png',["", "", "", "次へ"])
	layoutRoom_Q = make_4choice_layout('png/roo_q2.png',["A", "B", "C", "D"])
	layoutRoom_Correct = make_4choice_layout('png/roo_a.png',["", "", "", "次へ"])
	layoutRoom_Clear = make_4choice_layout('png/roo_i.png',["", "", "", "次へ"])

	dictLayout = {
		"ROOM_PRE"		: layoutRoom_Pre,
		"ROOM_HINT"		: layoutRoom_Hint,
		"ROOM_Q"		: layoutRoom_Q,
		"ROOM_CORRECT"	: layoutRoom_Correct,
		"ROOM_CLEAR"	: layoutRoom_Clear,
	}
	dictWindow_this = setGUI(dictLayout)

	return dict(dictWindow, **dictWindow_this)


# room_preモード処理 ======================================================
def procRoom_pre(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]

	if event == "次へ":
		sStartTime = cState.updateState("ROOM_Q")
		dictArgument["Start time"] = sStartTime
	elif event == "ヒント":
		sStartTime = cState.updateState("ROOM_HINT")
		dictArgument["Start time"] = sStartTime


# room_hintモード処理 ======================================================
def procRoom_hint(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]

	if event == "次へ":
		sStartTime = cState.updateState("ROOM_Q")
		dictArgument["Start time"] = sStartTime


# room_Qモード処理 ======================================================
def procRoom_Q(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]

	if event == "D":
		PlaySound("sound/correct.wav")

		cCtrlCard.write_result("room", "T")

		sStartTime = cState.updateState("ROOM_CORRECT")
		dictArgument["Start time"] = sStartTime
	elif event != "-timeout-":
		PlaySound("sound/wrong.wav")


# room_correctモード処理 ======================================================
def procRoom_correct(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]

	if Check_Clear(cCtrlCard):
		#sStartTime = cState.updateState("CLEAR1")
		cCtrlCard.write_result("clear_game", "T")  # ゲームクリア済みであることを記録

	if event == "次へ":
		sStartTime = cState.updateState("ROOM_CLEAR")
		dictArgument["Start time"] = sStartTime


# room_clearモード処理 ======================================================
def procRoom_clear(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]

	if event == "次へ":
		if Check_Clear(cCtrlCard):
			sStartTime = cState.updateState("CLEAR1")
			#cCtrlCard.write_result("clear_game", "T")  # ゲームクリア済みであることを記録
		else:
			sStartTime = cState.updateState("SELECT_GAME")

		dictArgument["Start time"] = sStartTime

		# ホンダナをクリアしたのでプレイできないように設定
		cState.dictWindow["SELECT_GAME"]["ルーム"].update(disabled=True)



