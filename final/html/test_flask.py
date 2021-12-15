from flask import Flask, flash, redirect, render_template, request, session, abort

flask_app = Flask(__name__)

class TabletApp(object):
    def __init__(self):
        super(TabletApp, self).__init__()

    @flask_app.route('/')
    def home():
		#if not session.get('logged_in'):
		#    return render_template('login.html')
		#else:
        return render_template('welcome.html')
    
    @flask_app.route('/start')
    def start():
        return render_template('choice2.html', text = "Hi, I am Pepper, what's your name?", choice1 = "speak", choice2 = "write",
                               choice1_template = '/speak', choice2_template = '/write')
    
    @flask_app.route('/write')
    def write():
        return render_template('write.html')
    
    @flask_app.route('/speak')
    def speak():
        return render_template('choice2.html', text = "Press REC to record, then press STOP to finish recording", choice1 = "REC", choice2 = "STOP")
    
    @flask_app.route('/inst', methods=['GET', 'POST'])
    def inst():
        print(request.method)
        if request.method == "POST":
            username = request.form['uname']
            TEXT = "Nice to meet you " + username +", do you want to hear the instructions?"
        return render_template('/choice2.html', text = TEXT, choice1 = "YES", choice2 = "NO")
    

    def run(self):
        flask_app.run(debug=True)

if __name__=="__main__":
    
    tablet_app = TabletApp()
    tablet_app.run()