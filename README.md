# Kin Voice Project - Django Framework API for Generating Synthesised Speech Audio

This is made as part of a project to investigate the "cloning" of voices of friends/relatives to use with voice interfaces in potentially useful applications such as issuing reminders in your friends/relatives ('kin'). Inspired from the idea that we could feel more receptive and comforted when hearing close friends/relatives' voices.

This API is meant to work with a custom-made Amazon Alexa Skill (a third-party feature that can be installed and accessed via Amazon Echo devices). This Skill enables users to set reminders, issues the reminders to users and plays the reminder audio in the voice of the user’s kin. 
1. Whenever a reminder is set through the Skill, it retrieves information on the reminder message, day, and time from the user. 
2. The reminder data is posted to this API that is hosted on a Google Cloud server. 
3. The API generates the reminder message as an audio file in a kin voice based on a speech recording sample of the user’s kin using the Real-Time Voice Cloning (RTVC) tool developed by Jemine et al. (https://github.com/CorentinJ/Real-Time-Voice-Cloning) and uploads the file to an Amazon S3 bucket database.
5. Due to a security safeguard for Alexa development, the Echo does not allow the synthesised audio file to be played when the reminder is issued. Thus, when the reminder is issued, the Echo Dot announces there is a reminder for them and asks the user to play the reminder message. 
6. Finally, the Echo plays the reminder audio file from the S3 database when the user asks and could be played at any time after the reminder is issued, until the next reminder is issued.

