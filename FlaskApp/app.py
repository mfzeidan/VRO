



from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("lineup2.html")

@app.route('/', methods=['POST'])
def my_form_post():

    #### names

    n1 = request.form['name_1']
    n2 = request.form['name_2']
    n3 = request.form['name_3']
    n4 = request.form['name_4']
    n5 = request.form['name_5']
    n6 = request.form['name_6']

    ##### FR Skills per player

    fr_1 = request.form['FR_1']
    fr_2 = request.form['FR_2']
    fr_3 = request.form['FR_3']
    fr_4 = request.form['FR_4']
    fr_5 = request.form['FR_5']
    fr_6 = request.form['FR_6']

    ##### BR Skills per player

    br_1 = request.form['BR_1']
    br_2 = request.form['BR_2']
    br_3 = request.form['BR_3']
    br_4 = request.form['BR_4']
    br_5 = request.form['BR_5']
    br_6 = request.form['BR_6']

    print "---- player 1 stats ----"
    print n1
    print "FR: " + str(fr_1)
    print "BR: " + str(br_1)

    print "---- player 2 stats ----"
    print n2
    print "FR: " + str(fr_2)
    print "BR: " + str(br_2)

    print "---- player 3 stats ----"
    print n3
    print "FR: " + str(fr_3)
    print "BR: " + str(br_3)

    print "---- player 4 stats ----"
    print n4
    print "FR: " + str(fr_4)
    print "BR: " + str(br_4)

    print "---- player 5 stats ----"
    print n5
    print "FR: " + str(fr_5)
    print "BR: " + str(br_5)

    print "---- player 6 stats ----"
    print n6
    print "FR: " + str(fr_6)
    print "BR: " + str(br_6)


    return n1



if __name__ == '__main__':
    app.run(host='0.0.0.0')




def build_player_skills_df():
	pass