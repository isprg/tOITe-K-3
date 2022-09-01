import time
import PySimpleGUI as sg

from functions.setGUI import setGUI
from functions.common import Reset_Game, PlaySound
from functions.CardFunc import SetGame_FromCard
from functions.DesignLayout import *


# 処理の辞書割り当て ======================================================
def createDictProc():
	dictProc = {
		"STANDBY"				: StandbyModeProc,
		"SELECT_GAME"		: select_game_ModeProc,
		"CARD_ERROR"		: card_error_ModeProc,
		"GO_TUTORIAL"	: go_tutorial_ModeProc,
	}
	return dictProc


# レイアウト設定・辞書割り当て =============================================
def createDictWindow():
	layoutBackGround = [[sg.Text()]]
	layoutStandby = make_fullimage_layout("png/standby01.png", "STANDBY")
	layoutSelect_Game = make_4choice_layout("png/select01.png", ["", "くらわんか船1", "くらわんか船2", ""])
	layoutGo_Tutorial = make_fullimage_layout("png/ending.png", "GO_TUTORIAL")
	layoutCard_Error = make_fullimage_layout("png/card_alert.png", "CARD_ERROR")


	dictLayout = {
		"BACKGROUND"    : layoutBackGround,
		"STANDBY"     : layoutStandby,
		"SELECT_GAME"   : layoutSelect_Game,
		"GO_TUTORIAL": layoutGo_Tutorial,
		"CARD_ERROR"    : layoutCard_Error
	}
	dictWindow = setGUI(dictLayout)

	return dictWindow

# 標準タップ座標設定 ================================================
def getDefaultAreaDefinition():
    vArea0 = [260, 520, 520, 60]
    listArea = [vArea0, ]

    return listArea

# # TITLEモード処理 ======================================================
# def titleModeProc(dictArgument):
# 	event = dictArgument["Event"]

# 	if event == "TITLE":
# 		# カードのデータからゲームの状態を設定
# 		SetGame_FromCard(dictArgument)


# STANDBYモード処理 ======================================================
def StandbyModeProc(dictArgument):
	cCtrlCard = dictArgument["CtrlCard"]
	cState = dictArgument["State"]

	setFlag = cCtrlCard.setCard()

	if setFlag:
		PlaySound("sound/card_set.wav")
		sStartTime = cState.updateState("SELECT_GAME")
		SetGame_FromCard(dictArgument)
		dictArgument["Start time"] = sStartTime


# SELECT_GAMEモード処理 =================================================
def select_game_ModeProc(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]

	if event == "くらわんか船1":
		sStartTime = cState.updateState("KURA1_Q")
		dictArgument["Start time"] = sStartTime
	elif event == "くらわんか船2":
		sStartTime = cState.updateState("KURA2_Q")
		dictArgument["Start time"] = sStartTime


# card_errorモード処理 ======================================================
def card_error_ModeProc(dictArgument):
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]
	proc = dictArgument["ImageProc"]

	exist = cCtrlCard.check_exist()  # カードが存在するかをチェック
	identical = cCtrlCard.check_identity()  # カードが同一かをチェック
	if exist is True and identical is True:
		ReturnState, ImageProc_Flag = dictArgument["Return state"]

		if ImageProc_Flag:
			proc.createWindows()

		sStartTime = cState.updateState(ReturnState)
		dictArgument["Return state"] = None
		# sStartTime = cState.updateState("STANDBY")
		dictArgument["Start time"] = sStartTime
		# Reset_Game(dictArgument)

	elif identical is False or time.time() - dictArgument["Start time"] > 10:
		Reset_Game(dictArgument)


# go_to_tutorialモード処理 ======================================================
def go_tutorial_ModeProc(dictArgument):
    if time.time() - dictArgument["Start time"] > 20:
        Reset_Game(dictArgument)
