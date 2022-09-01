

# ゲームの状態をカードに保存されているデータから設定
def SetGame_FromCard(dictArgument):
	cCtrlCard = dictArgument["CtrlCard"]
	cState = dictArgument["State"]

	dictSaveData = cCtrlCard.read_result()
	print("Save Data:", dictSaveData)

	# 全問正解の場合
	if dictSaveData is not None and dictSaveData["complete"] == "T":
		print("already clear game")
		# if dictSaveData["finish_survey"] == "T":
		# 	# アンケート回答済みの場合
		# 	sStartTime = cState.updateState("END_C")
		# else:
		# 	sStartTime = cState.updateState("CLEAR2")

		dictArgument["Start time"] = sStartTime

	elif dictSaveData["tutorial"] != "T":
		sStartTime = cState.updateState("GO_TURORIAL")
		dictArgument["Start time"] = sStartTime

	# チュートリアルをクリアしている場合
	elif dictSaveData is not None and dictSaveData["tutorial"] == "T":
		print("already clear tutorial")
		sStartTime = cState.updateState("SELECT_GAME")
		dictArgument["Start time"] = sStartTime

		# みなっぱをすべてクリアしている場合
		if dictSaveData["minappa"] == "T":
			cState.dictWindow["SELECT_GAME"]["くらわんか船1"].update(disabled=True)

		# ポーズ推定をすべてクリアしている場合
		if dictSaveData["pose"] == "T":
			cState.dictWindow["SELECT_GAME"]["くらわんか船2"].update(disabled=True)


# カードの状態をチェック
def CheckCard(dictArgument):
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]
	proc = dictArgument["ImageProc"]

	# カードが存在するかをチェック
	result = cCtrlCard.check_exist()
	if result is False:
		print("Card Error")
		if cState.dictWindow[cState.strState] == "None":
			dictArgument["Return state"] = (cState.strState, True)
			proc.closeWindows()
		else:
			dictArgument["Return state"] = (cState.strState, False)

		sStartTime = cState.updateState("CARD_ERROR")
		dictArgument["Start time"] = sStartTime

		return "CARD_ERROR"

	return cState.strState


# ゲーム終了用のカードかどうかを判定
def AdminFlag_fromCard(cCtrlCard, card_ID_list):
	ID = cCtrlCard.getID()
	if ID in card_ID_list:
		return True, ID

	return False, None
