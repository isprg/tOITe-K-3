

# ゲームの状態をカードに保存されているデータから設定
def SetGame_FromCard(dictArgument):
	cCtrlCard = dictArgument["CtrlCard"]
	cState = dictArgument["State"]

	dictSaveData = cCtrlCard.read_result()
	print("Save Data:", dictSaveData)

	# 全問正解の場合
	if dictSaveData is None or dictSaveData["complete"] == "T":
		print("game complete")

	# チュートリアルをやってない場合
	elif dictSaveData is None or dictSaveData["tutorial"] != "T":
		sStartTime = cState.updateState("GO_TUTORIAL")
		dictArgument["Start time"] = sStartTime

	# みなっぱをクリアしている場合
	elif dictSaveData["minappa"] == "T":
		cState.dictWindow["SELECT_GAME"]["くらわんか舟１"].update(disabled=True)

	# ポーズをクリアしている場合
	elif dictSaveData["pose"] == "T":
			cState.dictWindow["SELECT_GAME"]["くらわんか舟２"].update(disabled=True)

	elif dictSaveData["complete"] == "T":
			cState.dictWindow["SELECT_GAME"]["電話"].update(disabled=True)

	else:
		# カードを初期化
		print("InitCard")
		cCtrlCard.initCard()
		sStartTime = cState.updateState("SELECT_GAME")
		dictArgument["Start time"] = sStartTime


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
