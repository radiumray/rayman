```py


# 语音播报模块
import pyttsx3 
    
# 模块初始化
engine = pyttsx3.init() 

volume = engine.getProperty('volume')
# voices = engine.getProperty('voices')

# 标准的粤语发音
# voices = engine.setProperty('voice', "com.apple.speech.synthesis.voice.sin-ji")
# print('voices', voices)

# 普通话发音
# voices = engine.setProperty(
#     'voice', "com.apple.speech.synthesis.voice.ting-ting.premium")

# 台湾甜美女生普通话发音
# voices = engine.setProperty(  
#     'voice', "com.apple.speech.synthesis.voice.mei-jia")

# engine.setProperty('volume', 0.7)

print('准备开始语音播报...')
engine.say('我高冷，我并不想说话，犇，羴，鱻')
# 等待语音播报完毕 
engine.runAndWait()
engine.stop()


```
