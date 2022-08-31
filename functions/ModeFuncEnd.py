import time
from functions.setGUI import setGUI
from functions.common import Reset_Game
from functions.DesignLayout import make_4choice_layout


# 処理の辞書割り当て ======================================================
def updateDictProc_End(dictProc):
	dictProc_this = {
		"END_A"				: procEnd_A,
		"END_B"				: procEnd_B,
		"END_C"				: procEnd_C,
	}
	return dict(dictProc, **dictProc_this)


# レイアウト設定・辞書割り当て =============================================
def updateDictWindow_End(dictWindow):
	layoutEnd_A = make_4choice_layout("png/end_a.png", ["", "", "", ""])
	layoutEnd_B = make_4choice_layout("png/end_b.png", ["", "", "", ""])
	layoutEnd_C = make_4choice_layout("png/clear1.png", ["", "", "", ""])

	dictLayout = {
		"END_A"				: layoutEnd_A,
		"END_B"				: layoutEnd_B,
		"END_C"				: layoutEnd_C,
	}
	dictWindow_this = setGUI(dictLayout)

	return dict(dictWindow, **dictWindow_this)


# end_aモード処理 ======================================================
def procEnd_A(dictArgument):
	if time.time() - dictArgument["Start time"] > 20:
		Reset_Game(dictArgument)


# end_bモード処理 ======================================================
def procEnd_B(dictArgument):
	if time.time() - dictArgument["Start time"] > 20:
		Reset_Game(dictArgument)


# end_cモード処理 ======================================================
def procEnd_C(dictArgument):
	if time.time() - dictArgument["Start time"] > 20:
		Reset_Game(dictArgument)