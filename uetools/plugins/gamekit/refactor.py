

import os


path = "E:/Examples/GKStarterGame/Plugins/GKUI"
# out = "out/"
# os.makedirs(out)


def rename_file(root, file):
    fullpath = os.path.join(root, file)
    newname = fullpath.replace('Lyra', 'GKUI')

    if fullpath != newname:
        os.rename(fullpath, newname)


def rename_content(root, file):
    fullpath = os.path.join(root, file)

    with open(fullpath, "r") as fp:
        content = fp.read()

    x = (content
         .replace("LYRAGAME_API", "GKUI_API")
         .replace("Lyra", "GKUI")
         .replace("GKUIUI", "GKUI")
         .replace("UI/", "")
         .replace("// Copyright Epic Games, Inc. All Rights Reserved.", "// Copyright 2024 Mischievous Game, Inc. All Rights Reserved.")
    )

    with open(fullpath, "w") as fp:
        fp.write(x)

for root, dirs, files in os.walk(path):
    for f in files:
        rename_file(root, f)

for root, dirs, files in os.walk(path):
    for f in files:
        if f.endswith(".h") or f.endswith(".cpp") or f.endswith(".cs"):
            rename_content(root, f)
