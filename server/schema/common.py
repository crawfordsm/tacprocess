import graphene as g
from graphene import relay as r
import pandas as pd
from ..data import conn

import datetime
import warnings
from dateutil.relativedelta import relativedelta


class Semester(g.ObjectType):
    class Meta:
        interfaces = (r.Node,)

    semester_id = g.ID()
    semester = g.String()
    start_semester = g.String()
    end_semester = g.String()

    def get_semester(self, id_only=False, active=False, semester_id=None, semester_code=None, all_data=False):
        """
        :return: 
        """
        sql = 'SELECT  Semester_Id, CONCAT(Year,"_", Semester) as SemesterCode, StartSemester, EndSemester FROM  Semester '

        if all_data:
            data = pd.read_sql(sql, conn)

            li = [self._make_semester(d) for i, d in data.iterrows()]
            return li

        date = datetime.datetime.now().date()
        date_3 = date + relativedelta(months=3)

        if active:
            if semester_id is not None or semester_code is not None:
                warnings.warn("Semester id or Semester code is provided and active=True, active semester is returned. "
                              "Set active=False if you need none active semester if you query for none active semester."
                              "Returned is active Semester")

            sql = sql + ' where StartSemester <= "{date_}" and "{date_}" < EndSemester;'.format(date_=date_3)
        else:
            if semester_id is not None:
                sql = sql + ' where Semester_Id = {semester_id};'.format(semester_id=semester_id)
            elif semester_code is not None:

                if "-" in semester_code:
                    sql = sql + ' where CONCAT(Year, "-", Semester) = "{semester_code}";' \
                        .format(semester_code=semester_code)
                else:
                    sql = sql + ' where CONCAT(Year, "_", Semester) = "{semester_code}";' \
                        .format(semester_code=semester_code)
            else:
                raise ValueError(
                    "Set active=True for active semester, or provide semester_id or semester like '2017_1'  "
                    "or '2017-1'")

        data = pd.read_sql(sql, conn)
        try:
            semester = [self._make_semester(s) for i, s in data.iterrows()][0]
        except IndexError:
            semester = None

        if id_only:
            return self.semester_id
        return semester

    @staticmethod
    def _make_semester(data):
        # Todo This method is called only by get semester it is suppose to be a private method for semester
        """
         make a data received a 
        :param data: 
        :return: 
        """
        semest = Semester()
        semest.semester_id = data['Semester_Id']
        semest.semester = data['SemesterCode']
        semest.start_semester = data['StartSemester']
        semest.end_semester = data['EndSemester']
        return semest


class UserRole(g.Enum):
    VISITOR = 1
    INVESTIGATOR = 2
    TAC_MEMBER = 3
    TAC_CHAIR = 4
    SALT_ASTRONOMER = 5
    ADMINISTRATOR = 6


class User(g.ObjectType):
    class Meta:
        interfaces = (r.Node,)

    user_id = g.ID()
    lastname = g.String()
    firstname = g.String()
    email = g.String()
    # roles = graphene.Field(UserRole, description="A user role object")  # ** was a list **
    pipt_user_id = g.Int()
    phone = g.String()
    institute_id = g.Int()


class TimeDistributions(g.ObjectType):  # todo this name must have a proper meaning
    class Meta:
        interfaces = (r.Node,)

    semester = g.String()
    p0_and_p1 = g.Float() # allocated_
    p2 = g.Float()
    p3 = g.Float()
    # leave out below
    # used_p0_and_p1 = g.Float()
    # used_p2 = g.Float()
    # used_p3 = g.Float()





class ObservingConditions(g.ObjectType):
    class Meta:
        interfaces = (r.Node,)

    max_seeing = g.Float()
    transparency = g.String() # be enum
    description = g.String()


class Thesis(g.ObjectType): # was p1thesis
    class Meta:
        interfaces = (r.Node,)
    thesis_type = g.String()  # be Enum
    thesis_description = g.String()
    student = g.Field(User)
    # todo add year of completion



