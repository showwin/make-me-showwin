# make-me-showwin
Create showwin icon that is your face.  
This is a Slack bot.

# Example

<img width="743" alt="screen shot 2018-10-08 at 15 27 38" src="https://user-images.githubusercontent.com/1732016/46596034-f7fb6680-cb15-11e8-8670-69105dec1c20.png">


# Usage

```bash
$ aws configre  # require S3(write) and Rekognition(face detection) authority.
$ export SLACK_TOKEN_MAKE_ME_SHOWWIN=xoxb-****  # [Slack Token]
$ nohup python run.py &
```

and, upload image with `@mention` to this bot.

# ToDo
* [ ] run command as a command line tool (not as Slack bot)
