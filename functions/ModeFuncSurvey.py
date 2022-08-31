from functions.setGUI import setGUI
# from functions.common import Record_to_CSV
from functions.DesignLayout import make_4choice_layout


# 処理の辞書割り当て ======================================================
def updateDictProc_Survey(dictProc):
	dictProc_this = {
		"SURVEY1"			: procSurvey,
		"SURVEY2"			: procSurvey,
		"SURVEY3"			: procSurvey,
		"SURVEY4"			: procSurvey,
		"SURVEY5"			: procSurvey,
	}
	return dict(dictProc, **dictProc_this)


# レイアウト設定・辞書割り当て =============================================
def updateDictWindow_Survey(dictWindow):
	layoutSurvey1 = make_4choice_layout("png/quest1.png", ["A", "B", "C", "D"])
	layoutSurvey2 = make_4choice_layout("png/quest2.png", ["A", "B", "C", "D"])
	layoutSurvey3 = make_4choice_layout("png/quest3.png", ["A", "B", "C", "D"])
	layoutSurvey4 = make_4choice_layout("png/quest4.png", ["A", "B", "C", "D"])
	layoutSurvey5 = make_4choice_layout("png/quest5.png", ["A", "B", "C", "D"])

	dictLayout = {
		"SURVEY1"			: layoutSurvey1,
		"SURVEY2"			: layoutSurvey2,
		"SURVEY3"			: layoutSurvey3,
		"SURVEY4"			: layoutSurvey4,
		"SURVEY5"			: layoutSurvey5,
	}
	dictWindow_this = setGUI(dictLayout)

	return dict(dictWindow, **dictWindow_this)


# surveyモード処理 ======================================================
def procSurvey(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]
	strNumSurvey = cState.getState()
	sNumSurvey = int(strNumSurvey[-1])

	if event != "-timeout-":
		# アンケート結果を記録
		cCtrlCard.write_result("survey" + str(sNumSurvey), event)

		if sNumSurvey == 5:
			sStartTime = cState.updateState("END_B")
			dictArgument["Start time"] = sStartTime
			# Record_to_CSV(dictArgument)  # アンケート結果をcsvファイルに保存
		else:
			sStartTime = cState.updateState("SURVEY" + str(sNumSurvey + 1))
			dictArgument["Start time"] = sStartTime
