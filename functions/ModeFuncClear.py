from functions.setGUI import setGUI
from functions.common import Record_to_CSV
from functions.DesignLayout import make_4choice_layout


# 処理の辞書割り当て ======================================================
def updateDictProc_Clear(dictProc):
	dictProc_this = {
		"CLEAR1"			: procClear1,
		"CLEAR2"			: procClear2,
	}
	return dict(dictProc, **dictProc_this)


# レイアウト設定・辞書割り当て =============================================
def updateDictWindow_Clear(dictWindow):
	layoutClear1 = make_4choice_layout("png/clear1.png", ["", "", "", "次へ"])
	layoutClear2 = make_4choice_layout("png/clear2.png", ["", "", "終了", "答える"])

	dictLayout = {
		"CLEAR1"			: layoutClear1,
		"CLEAR2"			: layoutClear2,
	}
	dictWindow_this = setGUI(dictLayout)
	
	return dict(dictWindow, **dictWindow_this)


# clear1モード処理 ======================================================
def procClear1(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]

	if event == "次へ":
		sStartTime = cState.updateState("CLEAR2")
		dictArgument["Start time"] = sStartTime


# clear2モード処理 ======================================================
def procClear2(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]

	if event == "終了":
		sStartTime = cState.updateState("END_A")
		dictArgument["Start time"] = sStartTime
		Record_to_CSV(dictArgument)  # アンケート結果をcsvファイルに保存
	if event == "答える":
		sStartTime = cState.updateState("SURVEY1")
		dictArgument["Start time"] = sStartTime