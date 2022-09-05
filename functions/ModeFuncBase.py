import time
import PySimpleGUI as sg
import pyautogui

from functions.setGUI import setGUI
from functions.common import Reset_Game, PlaySound, CheckTappedArea
from functions.CardFunc import SetGame_FromCard
from functions.DesignLayout import *


# 処理の辞書割り当て ======================================================
def createDictProc():
	dictProc = {
		"STANDBY"			: standbyModeProc,
		"SELECT_GAME"		: select_game_ModeProc,
		"CARD_ERROR"		: card_error_ModeProc,
		"GO_TUTORIAL"	: go_tutorial_ModeProc,
	}
	return dictProc


# レイアウト設定・辞書割り当て =============================================
def createDictWindow():
	layoutBackGround = [[sg.Text()]]
	layoutStandby = make_fullimage_layout("images/standby.png", "STANDBY")
	layoutSelect_Game = make_4choice_layout("images/select.png", ["くらわんか舟１", "くらわんか舟２", "" , ""])
	layoutCard_Error = make_fullimage_layout("images/card_alert.png", "CARD_ERROR")
	layoutGo_Tutorial = make_fullimage_layout("images/go_tutorial.png", "GO_TUTORIAL")

	dictLayout = {
		"BACKGROUND"  : layoutBackGround,
		"STANDBY"     : layoutStandby,
		"SELECT_GAME" : layoutSelect_Game,
		"CARD_ERROR"  : layoutCard_Error,
		"GO_TUTORIAL": layoutGo_Tutorial,
    }
	dictWindow = setGUI(dictLayout)

	return dictWindow


# STANDBYモード処理 ======================================================
def standbyModeProc(dictArgument):
	cCtrlCard = dictArgument["CtrlCard"]
	cState = dictArgument["State"]

	setFlag = cCtrlCard.setCard()

	if setFlag:
		PlaySound("sound/card_set.wav")
		SetGame_FromCard(dictArgument)
		sStartTime = cState.updateState("SELECT_GAME")
		dictArgument["Start time"] = sStartTime


# SELECT_GAMEモード処理 =================================================
def select_game_ModeProc(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	proc = dictArgument["ImageProc"]

	cCtrlCard = dictArgument["CtrlCard"]
	dictSaveData = cCtrlCard.read_result()

	if event == "くらわんか舟１":
		sStartTime = cState.updateState("MINAPPA_Q1")
		dictArgument["Start time"] = sStartTime
	elif event == "くらわんか舟２":
		sStartTime = cState.updateState("POSE_Q")
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
		dictArgument["Start time"] = sStartTime

	elif identical is False or time.time() - dictArgument["Start time"] > 10:
		Reset_Game(dictArgument)

# go_tutorialモード処理 ======================================================
def go_tutorial_ModeProc(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]

	if event == "GO_TUTORIAL":
		Reset_Game(dictArgument)
