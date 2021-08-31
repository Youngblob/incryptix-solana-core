

studentName = "\"Akshay\""

template_file = open("./degree_template.c", "r", encoding="utf-8")

template = template_file.read()

template = template.replace("STUDENTNAME", studentName)

file = open('./helloworld/helloworld.c', 'w')
file.write(template)
file.close()


import os

os.system("npm run build:program-c & ls & solana program deploy /media/New_Volume_D/workspaces/workspace-ethereum/solana-dapps/youngblob-solana-core/dist/program/helloworld.so")
