import logging
from enum import Enum

class ColumnsCourseField(Enum):
    CODE = 1
    NAME = 2
    CREDIT = 3
    RECOMMENDED_SEMESTER = 4
    SAMPLE_CURRICULUM = 5
    COURSE_GROUP_CODE = 6
    COURSE_GROUP_NAME = 7
    COURSE_TYPE = 8
    RESULT = 9
    COURSE_ENROLLMENT_TIMES = 10


class Course:
    _parent_row_id = ""
    _row_id = ""

    def __init__(
            self, 
            code: str, name: str, credit: str, recommended_semester: str,
            sample_curriculum: str, course_group_code: str, course_group_name: str,
            course_type: str, result: str, course_enrollment_times: str
            ) -> None:
        self._code = code
        self._name = name
        self._credit = credit
        self._recommended_semester = recommended_semester
        self._sample_curriculum = sample_curriculum
        self._course_group_code = course_group_code
        self._course_group_name = course_group_name
        self._course_type = course_type
        self._result = result
        self._course_enrollment_times = course_enrollment_times

    @staticmethod
    def create_course_from_columns(columns: any, parent_row_id: str = '', row_id: str = '') -> 'Course':
        c = Course(
            Course._get_data_from_column(columns, ColumnsCourseField.CODE),
            Course._get_data_from_column(columns, ColumnsCourseField.NAME),
            Course._get_data_from_column(columns, ColumnsCourseField.CREDIT),
            Course._get_data_from_column(columns, ColumnsCourseField.RECOMMENDED_SEMESTER),
            Course._get_data_from_column(columns, ColumnsCourseField.SAMPLE_CURRICULUM),
            Course._get_data_from_column(columns, ColumnsCourseField.COURSE_GROUP_CODE),
            Course._get_data_from_column(columns, ColumnsCourseField.COURSE_GROUP_NAME),
            Course._get_data_from_column(columns, ColumnsCourseField.COURSE_TYPE),
            Course._get_data_from_column(columns, ColumnsCourseField.RESULT),
            Course._get_data_from_column(columns, ColumnsCourseField.COURSE_ENROLLMENT_TIMES),
        )
        c._parent_row_id = parent_row_id
        c._row_id = row_id
        return c

    @staticmethod
    def _get_data_from_column(columns: any, type: ColumnsCourseField) -> str:
        if len(columns) == 0 or len(columns) < type.value:
            logging.warn(f"course {type.name} value is set to empty because of column short length")
            return ""
        return columns[type.value].text

    @property
    def parent_row_id(self) -> str:
        return self._parent_row_id
    
    @parent_row_id.setter 
    def parent_row_id(self, parent_row_id: str): 
        self._parent_row_id = parent_row_id

    @property
    def row_id(self) -> str:
        return self._row_id
    
    @row_id.setter 
    def row_id(self, row_id: str): 
        self._row_id = row_id     


    def __str__(self):
        return f'code: {self._code}, name: {self._name}, credit: {self._credit}, recommended_semester: {self._recommended_semester}, sample_curriculum: {self._sample_curriculum}, course_group_code: {self._course_group_code}, course_group_name: {self._course_group_name}, course_type: {self._course_type}, outcome: {self._result}, course_enrollment_times: {self._course_enrollment_times}'