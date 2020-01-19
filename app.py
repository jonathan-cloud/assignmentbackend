import psycopg2
from flask import Flask, render_template, url_for, request
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


url = 'ec2-174-129-33-139.compute-1.amazonaws.com'
dbname = "d1fi060c8m01ph"
user = "wudajiqzsdyqti"
password = "88976a0de94126f5c6e76e6b901644388173151098beb352f11ba4f9ced7f6e6"
host = "ec2-174-129-33-139.compute-1.amazonaws.com"
port = 5432

conn = None

# POST REQUESTS
@app.route('/edit/<studentId>', methods=['POST'])
@cross_origin()
def editStudent(studentId):
    magicToAdd = request.get_json()

    cur = conn.cursor()
    print(magicToAdd['skill'])
    if magicToAdd['skill'] == '0':
        query = "delete from magics where student_id=" + \
            studentId+" and magic_id="+magicToAdd['id']
        cur.execute(query)
        return 'deleted'

    query = "select * from magics where student_id=" + \
        studentId+" and magic_id="+magicToAdd['id']

    cur.execute(query)

    print(cur.fetchall())

    if cur.rowcount == 0:
        print("he don't got it")
        query = "insert into magics(student_id, magic_id ,skill_level) values (" + \
            studentId+","+magicToAdd['id']+","+magicToAdd['skill']+")"

        print(query)
        cur.execute(query)

        # conn.commit()

    else:
        print("he got it")
        query = "update magics set skill_level=" + \
            magicToAdd['skill']+" where magic_id=" + \
                magicToAdd['id']+" and student_id="+studentId

        cur.execute(query)

    # conn.commit()
    query="""update students
set last_update=CURRENT_TIMESTAMP
where id="""+studentId
    cur.execute(query)
    return 'asdf'


@app.route('/addstudent', methods=['POST'])
@cross_origin()
def addStudent():

    test = request.get_json()

    print(test)

    print(test['first'])
    print(test['last'])
    cur = conn.cursor()
    query = "insert into students (first_name,last_name,create_time,last_update) values ('" + \
        test['first']+"','"+test['last'] + \
            "',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"

    cur.execute(query)
    # conn.commit()

    return "good job"


@app.route('/editdesired/<studentId>', methods=['POST'])
@cross_origin()
def editDesired(studentId):
    magicToAdd = request.get_json()

    cur = conn.cursor()

    print(magicToAdd['skill'])
    if magicToAdd['skill'] == '0':
        query = "delete from desired_magics where student_id=" + \
            studentId+" and magic_id="+magicToAdd['id']
        cur.execute(query)
        return 'deleted'

    query = "select * from desired_magics where student_id=" + \
        studentId+" and magic_id="+magicToAdd['id']

    cur.execute(query)

    print(cur.fetchall())

    if cur.rowcount == 0 and cur.rowcount < 5:
        print("he don't got it")
        query = "insert into desired_magics(student_id, magic_id ,skill_level) values (" + \
            studentId+","+magicToAdd['id']+","+magicToAdd['skill']+")"

        print(query)
        cur.execute(query)

        # conn.commit()

    else:
        print("he got it")
        query = "update desired_magics set skill_level=" + \
            magicToAdd['skill']+" where magic_id=" + \
                magicToAdd['id']+" and student_id="+studentId

        cur.execute(query)
    query="""update students
set last_update=CURRENT_TIMESTAMP
where id=1"""
    cur.execute(query)
    return 'asdf'


@app.route('/editcourse/<studentId>', methods=['POST'])
@cross_origin()
def add_crouse(studentId):
    courseToAdd = request.get_json()
    cur = conn.cursor()

    query = "select * from courses where student_id=" + \
        studentId+" and course_id="+courseToAdd['id']

    cur.execute(query)

    if cur.rowcount == 0 and cur.rowcount < 5:

        query = "insert into courses(student_id, course_id ) values (" + \
            studentId+","+courseToAdd['id']+")"

        cur.execute(query)
    else:
        print('he got it')
    query="""update students
set last_update=CURRENT_TIMESTAMP
where id=1"""
    cur.execute(query)
    return 'yes'

# END POSTS
@app.route('/dailyenroll', methods=['GET'])
@cross_origin()
def daily():
  cur = conn.cursor()
  query = """select DATE(create_time), count(DATE(create_time)) from students
group by DATE(create_time); """

  cur.execute(query)
  ret = []
  rows = cur.fetchall()
  
  for result in rows:
        ret.append({
            'label': result[0].isoformat(),
            'count': result[1]

        })

  ret = json.dumps(ret)

  print(ret)
  return ret
@app.route('/monthlyenroll', methods=['GET'])
@cross_origin()
def enroll():
    cur = conn.cursor()
    query = """select 

extract (month from create_time)::int as month,
count(extract (month from create_time))
from students

group by extract (month from create_time)"""

    cur.execute(query)
    ret = []
    rows = cur.fetchall()

    for result in rows:
        ret.append({
            'label': result[0],
            'count': result[1]

        })

    ret = json.dumps(ret)

    print(ret)
    return ret

@app.route('/magicchart', methods=['GET'])
@cross_origin()
def magicChart():
    cur = conn.cursor()
    query = """SELECT magic_list.name,
   COUNT (magic_list.name)
FROM
   magics, magic_list
where magics.magic_id=magic_list.id
GROUP BY
magic_list.name"""

    cur.execute(query)
    ret = []
    rows = cur.fetchall()

    for result in rows:
        ret.append({
            'name': result[0],
            'count': result[1]

        })

    ret = json.dumps(ret)

    print(ret)
    return ret


@app.route('/desiredchart', methods=['GET'])
@cross_origin()
def desiredChart():
    cur = conn.cursor()
    query = """SELECT magic_list.name,
   COUNT (magic_list.name)
    FROM
   desired_magics, magic_list
  where desired_magics.magic_id=magic_list.id
  GROUP BY
    magic_list.name"""

    cur.execute(query)
    ret = []
    rows = cur.fetchall()

    for result in rows:
        ret.append({
            'name': result[0],
            'count': result[1]

        })

    ret = json.dumps(ret)

    print(ret)
    return ret


@app.route('/courses', methods=['GET'])
@cross_origin()
def get_courses():
    cur = conn.cursor()
    query = "select * from course_list"

    cur.execute(query)
    course_list = []
    rows = cur.fetchall()

    for course in rows:
        print(course)
        course_list.append({
            "id": course[0],
            "name": course[1]
        })

    print(course_list)
    ret = json.dumps(course_list)
    return ret


@app.route('/desired', methods=['GET'])
@cross_origin()
def get_desired():
    cur = conn.cursor()
    query = "select * from desired_magics"

    cur.execute(query)
    course_list = []
    rows = cur.fetchall()

    for course in rows:
        print(course)
        course_list.append({
            "id": course[1],
            "name": course[2]
        })

    print(course_list)
    ret = json.dumps(course_list)
    return ret


@app.route('/magics', methods=['GET'])
@cross_origin()
def getMagics():
    cur = conn.cursor()
    query = "select * from magic_list"

    cur.execute(query)
    magics = []
    rows = cur.fetchall()
    for magic in rows:
        print(magic)
        magics.append({
            'id': magic[0],
            'name': magic[1]
        })

    ret = json.dumps(magics)

    print(ret)

    return ret


@app.route('/desiredMagics/<studentId>', methods=['GET'])
@cross_origin()
def getTheDesire(studentId):

    # get_desired = request.get_json()
    cur = conn.cursor()
    query = "select magic_list.name, desired_magics.skill_level, desired_magics.id from magic_list, desired_magics where desired_magics.magic_id=magic_list.id and desired_magics.student_id="+studentId+""
    cur.execute(query)

    # rows = cur.fetchall()
    # desired = []
    # for i in rows:
    #   print(i)
    return 'what'


@app.route('/students')
@cross_origin()
def getStudents():
    cur = conn.cursor()
    cur.execute("""
  select * from students;
  """)

    rows = cur.fetchall()
    students = []

    for student in rows:
        print(student)
        students.append({
            'id': student[0],
            'first': student[1],
            'last': student[2],
            'created': student[3].isoformat(),
            'updated': student[4].isoformat(),
        })

    ret = json.dumps(students)

    print(ret)

    return ret

    # return render_template('index.html', students=students)


@app.route('/students/<studentId>')
@cross_origin()
def getStudent(studentId):
    cur = conn.cursor()

    query = "select * from students where students.id="+studentId+";"
    cur.execute(query)

    rows = cur.fetchall()
    students = []

    for student in rows:
        # print(student)

        students.append({
            'id': student[0],
            'first': student[1],
            'last': student[2],
            'created': student[3].isoformat(),
            'updated': student[4].isoformat(),
        })

        students[0]['magics'] = []

        query = "select magic_list.name, skill_level from magic_list, magics where magics.student_id=" + \
            studentId+" and magics.magic_id=magic_list.id;"

        cur.execute(query)

        magics = cur.fetchall()

        for magic in magics:
            print(magic)

            students[0]['magics'].append({
                'name': magic[0],
                'skill': magic[1]
            })

        students[0]['desired'] = []

        query = "select magic_list.name, desired_magics.skill_level from magic_list, desired_magics where desired_magics.magic_id=magic_list.id and desired_magics.student_id="+studentId

        cur.execute(query)
        desired = cur.fetchall()

        for magic in desired:
            print(magic)
            students[0]['desired'].append({
                'name': magic[0],
                'skill': magic[1]
            })

        students[0]['courses'] = []
        query = "select course_list.name from courses, course_list where courses.student_id=" + \
            studentId+" and course_list.id=courses.course_id;"

        cur.execute(query)

        courses = cur.fetchall()

        for course in courses:
            print(course)
            students[0]['courses'].append(course[0])

        # print(magics)

    ret = json.dumps(students)

    print(ret)

    return ret


# DELETES

@app.route('/deletemagic/<studentId>', methods=['POST'])
@cross_origin()
def delete_magic(studentId):
    courseToDelete = request.get_json()

    cur = conn.cursor()
    print(courseToDelete)
    query = "delete from magics where student_id=" + \
        studentId + "and magic_id="+courseToDelete['id']+";"

    cur.execute(query)

    return json.dumps(courseToDelete)


@app.route('/deletedesired/<studentId>', methods=['POST'])
@cross_origin()
def delete_desired(studentId):
    magicToDelete = request.get_json()

    cur = conn.cursor()
    print(magicToDelete)
    query = "delete from desired_magics where student_id=" + \
        studentId + "and magic_id="+magicToDelete['id']+";"

    cur.execute(query)

    return json.dumps(magicToDelete)


if __name__ == '__main__':
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True
    except:
        print("wtf just happened")
    app.run(debug=True)
