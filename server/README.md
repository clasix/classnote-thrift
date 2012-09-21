#User 
    {
        id,
        username,
        password,
        salt,
        email,
        activate,
        created
    }

#Class 
    {
        id,
        school,
        dept,
        year  #入学年份
    }

#Course(教程)
    {
        id,
        name,
        tearcher,
        book,
        for_class, # 为哪一个班级设计的教程
        for_semester # 为哪一届设计的教程
    }

#LessonInfo(课节信息)
    {
        id,
        course_id, # -->Course.id
        weekday, #星期几上课
        start, # 第几节课
        duration # 课时
    }

#LessonTable(课表)
    {
        id,
        user_id, # --> User.id, 谁拥有这个课表，TODO公共课表 for class_id
        semester # 第几学期
    }

#LessonTableItem(课表项) 
由课表和LessonInfo的关联组成，将LessonInfo添加(选)进课表，即产生关联
当用户添加课程表的时候，如果已有相同的课程表，如何保证唯一性 ???
但是，当合并后，一个学生改了课节信息，另外一个学生的课节信息也会变化，是否是用户想要的效果？hash = hash(course_id, weekday, start, duration), 
    {
        id,
        table_id, # --> LessonTable.id
        lesson_info_id --> LessonInfo.id
    }

#AuthToken，用来权限认证, cookies(expiretime, 记住登录状态)
    {
        id,
        user_id, # --> User.id
        auth_token
    }
