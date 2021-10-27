# Create your views here.
import os
import time

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import Question, Choice


def get_wsl_ip():
    try:
        with open('/etc/resolv.conf') as f:
            for line in f.readlines():
                item = line.split(' ')
                if item[0] == 'nameserver':
                    return item[1].strip()
    except FileNotFoundError:
        pass


class IndexView(generic.ListView):
    template_name = 'bbs/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):

        print(os.getpid(), "myapp.views.py: " + os.getcwd())
        if os.getenv("PYTHONPATH"):
            print(os.getpid(), "myapp:", os.getenv("PYTHONPATH"))

        return Question.objects.order_by('-pub_date')[:5]


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'bbs/index.html', context)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'bbs/detail.html'


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("{0} Question does not exist".format(question_id))
    return render(request, 'bbs/detail.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'bbs/detail.html', {'question': question})

    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('bbs:results', args=(question_id,)))


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'bbs/results.html'


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'bbs/results.html', {'question': question})


def parent(request):
    time.sleep(5)
    return render(request, 'bbs/base.html')


def child(request):
    time.sleep(60)
    return render(request, 'bbs/child.html')


def sqlite3test(request):
    import sqlite3

    con = sqlite3.connect('./my_test.db')
    cursor = con.cursor()

    query = "CREATE TABLE IF NOT EXISTS member(ID int primary key not null, Name text, Age int);"
    cursor.execute(query)

    query = "DELETE FROM member"
    cursor.execute(query)

    for idx in range(1, 5):
        query = "INSERT OR REPLACE INTO member VALUES({0}, 'tester{1}', {2})".format(idx, idx, idx * 10)
        cursor.execute(query)

    con.commit()

    query = "SELECT * FROM member"
    cursor.execute(query)
    query_result = str(cursor.fetchall())
    con.close()

    return render(request, 'bbs/sqlite3test.html', {'result_set': query_result})


def mysqlclient_raw(request):
    from MySQLdb import _mysql

    mysql_ip = get_wsl_ip()
    if mysql_ip is None:
        mysql_ip = "127.0.0.1"

    con = _mysql.connect(mysql_ip, "testusr", "testusr@100420", "test")
    # con = _mysql.connect(host="localhost", user="testusr", passwd="testusr@100420", db="test", charset='utf8mb4')

    con.query("INSERT INTO test(name, age, enable) VALUES('테스터', 23, 1)")

    con.query("SELECT * FROM test;")

    r = con.store_result()
    record_text = ""

    while True:
        record = r.fetch_row()
        # record = r.fetchone()
        if not record:
            break

        name_value = record[0]
        record_text += str(name_value) + "\n"
        print(record)

    con.query("DELETE FROM test WHERE enable=1 AND age=23")

    con.close()

    return render(request, 'bbs/mysqlclient_raw.html', {'result_set': record_text})


def mysqlclient_wrapper(request):
    import MySQLdb

    mysql_ip = get_wsl_ip()
    if mysql_ip is None:
        mysql_ip = "127.0.0.1"

    con = MySQLdb.connect(mysql_ip, "testusr", "testusr@100420", "test", charset='utf8')
    con.encoding = 'utf8'

    # cursor = con.cursor(dictionary=True)
    # cursor = con.cursor()
    cursor = con.cursor(MySQLdb.cursors.DictCursor)

    query = "DELETE FROM test"
    cursor.execute(query)

    for idx in range(1, 5):
        query = "INSERT INTO test(name, age, enable) VALUES('테스터{0}', {1}, {2});".format(idx, idx, idx * 10)
        cursor.execute(query)

    con.commit()

    query = "SELECT * FROM test"
    cursor.execute(query)

    record_text = ""

    all_rows = cursor.fetchall()
    for row in all_rows:
        record_text += str(row)
        # field_name = row[0]
        # field_age = row[1]
        # field_enable = row[2]

        # field_name = row['name']
        field_age = row['age']
        field_enable = row['enable']

    # while True:
    #     record = cursor.fetchone()
    #     if not record:
    #         break
    #
    #     record_text += str(record)

    cursor.close()

    return render(request, 'bbs/mysqlclient_wrapper.html', {'result_set': record_text})


def pymysqltest(request):
    import pymysql

    mysql_ip = get_wsl_ip()
    if mysql_ip is None:
        mysql_ip = "127.0.0.1"

    con = pymysql.connect(host=mysql_ip, user="testusr", password="testusr@100420", db="test", charset='utf8')

    # cursor = con.cursor(dictionary=True)
    # cursor = con.cursor()
    cursor = con.cursor(pymysql.cursors.DictCursor)

    query = "DELETE FROM test"
    cursor.execute(query)

    for idx in range(1, 5):
        query = "INSERT INTO test(name, age, enable) VALUES('테스터{0}', {1}, {2});".format(idx, idx, idx * 10)
        cursor.execute(query)

    con.commit()

    query = "SELECT * FROM test"
    cursor.execute(query)

    record_text = ""

    all_rows = cursor.fetchall()
    for row in all_rows:
        record_text += str(row)
        field_name = row['name']
        field_age = row['age']
        field_enable = row['enable']

    # while True:
    #     record = cursor.fetchone()
    #     if not record:
    #         break
    #
    #     record_text += str(record)

    cursor.close()

    return render(request, 'bbs/pymysqltest.html', {'result_set': record_text})

