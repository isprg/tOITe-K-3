import cv2
import pyautogui
import subprocess
import os
from functions.setGUI import setGUI
from functions.common import *
from functions.DesignLayout import *


# 処理の辞書割り当て ======================================================
def updateDictProc_Pose(dictProc):
    dictProc_this = {
        "POSE_Q"			: procPose_Q,
        "POSE_PROC"			: procPose_ImageProc,
        "POSE_CORRECT": procPose_correct,
        "POSE_CLEAR": procPose_clear
    }
    return dict(dictProc, **dictProc_this)


# レイアウト設定・辞書割り当て =============================================
def updateDictWindow_Pose(dictWindow):
    layoutPose_Q = make_fullimage_layout("images/k-3_8.png", "POSE_Q")
    layoutPose_Correct = make_fullimage_layout(
        "images/k-3_9.png", "POSE_CORRECT")
    layoutPose_Clear = make_fullimage_layout("images/k-3_10.png", "POSE_CLEAR")

    dictLayout = {
        "POSE_Q"			: layoutPose_Q,
        "POSE_PROC"			: 'None',
        "POSE_CORRECT": layoutPose_Correct,
        "POSE_CLEAR": layoutPose_Clear
    }
    dictWindow_this = setGUI(dictLayout)

    return dict(dictWindow, **dictWindow_this)


def getDefaultAreaDefinition():
    vArea0 = [260, 520, 520, 60]
    listArea = [vArea0, ]

    return listArea

# labo_Qモード処理 ======================================================


def procPose_Q(dictArgument):
    event = dictArgument["Event"]
    cState = dictArgument["State"]
    proc = dictArgument["ImageProc"]

    if event == "POSE_Q":
        vPosition = pyautogui.position()
        listArea = getDefaultAreaDefinition()
        sTappedArea = CheckTappedArea(vPosition, listArea)

        if sTappedArea == 0:  # 次へをタップ
            proc.createWindows()
            proc.defineCorrectPose("")
            sStartTime = cState.updateState("POSE_PROC")
            dictArgument["Start time"] = sStartTime


# labo_ImageProcモード処理 ======================================================
def procPose_ImageProc(dictArgument):
    cState = dictArgument["State"]
    sFrame = dictArgument["Frame"]
    proc = dictArgument["ImageProc"]
    cCtrlCard = dictArgument["CtrlCard"]

    isFound = proc.execute()
    cv2.waitKey(1)

    print("isFound", isFound)
    # print("sCountFound",sCountFound)
    # print("sFrame",sFrame)

    if isFound is True:
        PlaySound("sound/correct.wav")
        sStartTime = cState.updateState("POSE_CORRECT")
        dictArgument["Start time"] = sStartTime
        # print(dictArgument["Event"])

        proc.closeWindows()


# labo_correctモード処理　======================================================
def procPose_correct(dictArgument):
    event = dictArgument["Event"]
    cState = dictArgument["State"]
    # cCtrlCard = dictArgument["CtrlCard"]

    # print(event)
    if event == "POSE_CORRECT":
        vPosition = pyautogui.position()
        listArea = getDefaultAreaDefinition()
        sTappedArea = CheckTappedArea(vPosition, listArea)

        if sTappedArea == 0:
            sStartTime = cState.updateState("POSE_CLEAR")
            dictArgument["Start time"] = sStartTime


# labo_clearモード処理　======================================================
def procPose_clear(dictArgument):
    event = dictArgument["Event"]
    cState = dictArgument["State"]
    cCtrlCard = dictArgument["CtrlCard"]

    if event == "POSE_CLEAR":
        vPosition = pyautogui.position()
        listArea = getDefaultAreaDefinition()
        sTappedArea = CheckTappedArea(vPosition, listArea)

        if sTappedArea == 0:
            sStartTime = cState.updateState("SELECT_GAME")
            dictArgument["Start time"] = sStartTime
            cCtrlCard.write_result("pose", "T")
            cState.dictWindow["SELECT_GAME"]["くらわんか舟２"].update(disabled=True)
