from StudentManagement import app, db, admin
from StudentManagement.models import *
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose


class StaticticsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/statistic.html')


admin.add_view(ModelView(Account, db.session))
admin.add_view(ModelView(Classes, db.session))
admin.add_view(ModelView(Students, db.session))
admin.add_view(ModelView(Grade, db.session))
admin.add_view(ModelView(Regulations, db.session))
admin.add_view(ModelView(Teachers, db.session))
admin.add_view(ModelView(Subjects, db.session))
# admin.add_view(ModelView(Semesters, db.session))
# admin.add_view(ModelView(School_year, db.session))
admin.add_view(StaticticsView(name='Statistic',endpoint='statistic'))
admin.add_view(ModelView(Ftm_scores, db.session))
admin.add_view(ModelView(Stm_scores, db.session))
admin.add_view(ModelView(Scores, db.session))

